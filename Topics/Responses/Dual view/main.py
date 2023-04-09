from flask import Flask, make_response

app = Flask('main')


@app.route('/data/main_info')
def view_func1():
    return make_response("<h1>Hello there, it's me — my own worst enemy!</h1>", 200)


@app.route('/the_wall')
def view_func2():
    return make_response("<h1>Welkommen!</h1>", 200)
