from flask import Flask, request


def fact(n):
    a = 1
    for i in range(1, n + 1):
        a *= i
    return a


app = Flask(__name__)


@app.route('/factorial', methods=['GET'])
def get_factorial():
    n = int(request.args['n'])
    return str(fact(n))


@app.route("/")
def main_page():
    return "<p>Welcome to Flask!</p>"


if __name__ == '__main__':
    app.run()
