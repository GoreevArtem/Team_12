from flask import Flask, request
import simple_operations

app = Flask(__name__)


@app.route("/")
def main_page():
    return "<h1>App - works!</h1>"


@app.route("/fib", methods=['GET'])
def get_fib():
    return str(simple_operations.fib(5))


@app.route("/factorial", methods=['GET'])
def get_factorial():
    return str(simple_operations.factorial(5))


if __name__ == "__main__":
    app.run(debug=True)
