import os
from flask import Flask, render_template, url_for, redirect, session, flash, request
from forms import GetTagsForm, LoginForm, RegistrationForm
from werkzeug.utils import secure_filename

from predection_final_version import list_tags


app = Flask(__name__)

WAV_PATH="wav_file/"
NPY_PATH = "npy_file/"
LABELS_PATH = 'C:/Users/mahrati_ed/Desktop/pfe_app/labels.csv'
LOAD_DIR_MODELS = ['C:/Users/mahrati_ed/Desktop/route predection backend/models/system_0',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_1',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_2mean',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_3',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_4']


app.config['SECRET_KEY']='6ea28f4cb420aa71a93faf8acf4c37bd'
app.config['WAV_PATH'] = WAV_PATH
app.config['NPY_PATH'] = NPY_PATH
app.config['LABELS_PATH'] = LABELS_PATH
app.config['LOAD_DIR_MODELS'] = LOAD_DIR_MODELS





@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    return render_template('index.html', title='Home') 

@app.route("/quick_test_result", methods=['GET', 'POST'])
def quick_test_result():
    lis=[]
    form = GetTagsForm()

    if form.validate_on_submit():
        
        wav_file = request.files['audio']
        wavefile_name = SaveWavFile(wav_file)
        WavFile_path, NpyFile_path, filename = getFilePaths(wavefile_name=wavefile_name)
        labels_path = app.config['LABELS_PATH']
        LOAD_DIR_MODELS = app.config['LOAD_DIR_MODELS']

        # audio processing and get tags
        dic_predict, df_predict = list_tags(LOAD_DIR_MODELS=LOAD_DIR_MODELS, output_dir=NpyFile_path, 
                                            input_dir=WavFile_path, filename=filename, labels_path=labels_path)
        lis.append(df_predict)
        lis.append(dic_predict)
        lis.append(wavefile_name)

        # print(dic_predict)
        # print(df_predict)
        
        redirect(url_for('quick_test_result'))

    # delete  wav and npy files
    # _ = DeleteFile(file_path=WavFile_path)
    # _ = DeleteFile(file_path=NpyFile_path)
    # get tags in this route 
    return render_template('quick_test_result.html', title='Quick Test Result', result=lis, form=form)

@app.route("/get_detail_result", methods=['GET', 'POST'])
def get_detail_result():
    #form = GetTagsForm()
    return render_template('get_detail_result.html', title='Detail Of Test Result')

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You') # for later
    return render_template('login.html', title='Login', form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)



def DeleteFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist") 

def SaveWavFile(wav_file):
    wavefile_name= secure_filename(wav_file.filename)
    wav_file.save(os.path.join(app.config['WAV_PATH'], wavefile_name))
    return wavefile_name

def getFilePaths(wavefile_name):
    wavfile_path = os.path.join(app.config['WAV_PATH'], wavefile_name)
    filename = wavefile_name[:-4]
    NpyFile_path = app.config['NPY_PATH']
    return wavfile_path, NpyFile_path, filename


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

if __name__ == '__main__':
    app.run(debug=True)