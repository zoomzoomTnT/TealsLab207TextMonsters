from flask import Flask, render_template, redirect
from components.InputForm import InputForm
from components.GameAPI import display_commands, update_user_items, update_user_position, get_hint
from components.Config import init

# Flask Env Var
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

floors, visited, player, items, status, current_command = init()


# Controllers
@app.route('/gameover', methods=['GET'])
def game_over():
    return render_template('index.html', status=status)


@app.route('/', methods=['GET', 'POST'])
def game():
    form = InputForm()
    global floors, visited, player, items, status, current_command

    commands = display_commands(floors[player[0]][player[1]], current_command)
    if form.validate_on_submit():
        if form.reset.data:
            floors, visited, player, items, status, current_command = init()
            return redirect('/')

        current_command = form.command.data
        items, status, floors = update_user_items(floors[player[0]][player[1]],
                                                  current_command, commands, items, player, floors)
        if status == 'win' or status == 'loss':
            return redirect('/gameover')
        player = update_user_position(current_command, commands, player, floors)
        visited[player[0]][player[1]] = True
        return redirect('/')

    return render_template('form.html', form=form,
                           map=mask_map(floors, visited),
                           commands=commands,
                           status=status,
                           position=player,
                           items=items,
                           hint=get_hint())


def mask_map(floors, visited):
    ret = [["", "", "", "", ""],
           ["", "", "", "", ""],
           ["", "", "", "", ""]]
    for i in range(len(floors)):
        for j in range(len(floors[i])):
            if not visited[i][j]:
                ret[i][j] = ""
            else:
                ret[i][j] = floors[i][j]
    return ret


# todo reset

if __name__ == '__main__':
    app.run(host="localhost", port=8000)
