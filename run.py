from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html', title='Home')

@app.route("/page1")
def page1():
    return "page1"

@app.route("/about")
def home():
    return "about page"

if __name__ == '__main__':
    app.run(debug=True)