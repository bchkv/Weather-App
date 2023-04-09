from flask import Flask, make_response

app = Flask('main')


@app.route('/<argument>')
def main_view(argument):
    return make_response(argument, 204)
