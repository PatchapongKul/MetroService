from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello, this is the Metro Service'

if __name__ == '__main__':
    app.run()

