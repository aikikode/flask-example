from . import app


@app.route('/hello')
def hello():
    # a simple page that says hello
    return 'Hello, World!'
