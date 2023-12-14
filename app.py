from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Olá, mundo! Este é um servidor Flask.'

if __name__ == '__main__':
    app.run(debug=True)
