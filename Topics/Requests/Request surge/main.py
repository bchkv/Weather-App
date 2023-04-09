from flask import Flask, request, Response, make_response, jsonify

app = Flask('main')


@app.route('/')
def main_view():
    query_parameters = request.args
    result = [f"{name}: {value}" for name, value in query_parameters.items()]
    result_string = ', '.join(result)
    return f"Received beautiful parameters! {result_string}."
