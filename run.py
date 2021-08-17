import os
from flask import Flask, render_template, url_for, redirect, session, flash, request
from forms import GetTagsForm, LoginForm, RegistrationForm
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_PATH="uploade file/"

app.config['SECRET_KEY']='6ea28f4cb420aa71a93faf8acf4c37bd'
app.config['UPLOAD_PATH'] = UPLOAD_PATH


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = GetTagsForm()
    if request.method == 'POST':
        uploaded_file = request.files['audio']
        filename= secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        session['filename'] = filename
        session['file_path'] = file_path

        return redirect(url_for('quick_test_result', filename=filename))
        
    return render_template('index.html', title='Home', form=form)


'''
@app.route("/get_ClipPath", methods=['GET', 'POST'])
def quick_test():
    form = GetTagsForm()
    if form.validate_on_submit():
        clip_path = form.clip.data
        session['clip_path'] = clip_path
        return redirect(url_for('quick_test_result', title='Quick Test Result'))

    return render_template('index.html', title='Get Audio Path', form=form)
'''

@app.route("/quick_test_result" )
def quick_test_result():
    # audio processing and get tags in this route 
    file_path = session.get('file_path', None)
    return render_template('quick_test_result.html', title='Quick Test Result', file_path=file_path)

@app.route("/get_detail_result", methods=['GET', 'POST'])
def get_detail_result():
    #form = GetTagsForm()
    file_filename = session.get('filename', None)
    return render_template('get_detail_result.html', title='Detail Of Test Result', file_filename=file_filename)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)




if __name__ == '__main__':
    app.run(debug=True)