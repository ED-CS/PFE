from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html', title='Home')

@app.route("/quick_test")
def quick_test():
    return render_template('quick_test_result.html', title='Quick Test Result')


if __name__ == '__main__':
    app.run(debug=True)