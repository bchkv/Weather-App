from flask import Flask, render_template

app = Flask('main')
app.app_context()

@app.route("/ref/")
@app.route("/link/")
def show_connect():
    return render_template('connect.html')

app.run()
