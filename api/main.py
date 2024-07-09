from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/2')
def hello_2():
    return 'Hello, World 2!'

if __name__ == "__main__":
    app.run(debug=True)
