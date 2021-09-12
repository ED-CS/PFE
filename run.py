import os
from flask import Flask, render_template, url_for, redirect, session, flash, request , Markup
from numpy.lib.function_base import append
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






#--------------------------------HOME ROUTE-------------------------------------------------------------------------

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    return render_template('index.html', title='Home') 

#--------------------------------QUICK TEST ROUTE-------------------------------------------------------------------

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
                                            input_dir=WavFile_path, filename=filename, labels_path=labels_path, nb_tags=int(form.nb_tags.data))

        lis.append(df_predict)
        lis.append(dic_predict)
        lis.append(wavefile_name)
 
        listAllTuple = []
        sysname = ["System 0","System 1","System 2","System 3","System 4"]
        colors = [
        "#808080","#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        val_tags=[]
        tags = []
        clos = []
        print('-------------------------------------------------------------------------------')
        for sys in sysname:

            j = 1
            listTuple =[]
            tags_val = 0 
            val = []
            tag = []
            col = []
            for i in range(79, 0, -1):

                if df_predict.iloc[i][sys]*100 >= 10:
                                  
                    tup = (int(df_predict.iloc[i][sys]*100), df_predict.iloc[i]['Dataset'], colors[j], sys)
                    #----------------------------------------------------------------------------------------
                    val.append(int(df_predict.iloc[i][sys]*100))
                    tag.append(df_predict.iloc[i]['Dataset'])
                    col.append(colors[j])
                    #----------------------------------------------------------------------------------------
                    listTuple.append(tup)
                    j+=1
                    tags_val = tags_val + int(df_predict.iloc[i][sys]*100)

            other_val = 100 - tags_val
             #---------------------------------------------------------------------------------------- 
            val_tags.append(val) 
            tags.append(tag)  
            clos.append(col)   
             #----------------------------------------------------------------------------------------
            listTuple.append((other_val,"Other_Tags",colors[0],sys))
            listAllTuple.append(listTuple)

         #----------------------------------------------------------------------------------------
        print(val_tags)
        print(tags)
        print(clos)
         #----------------------------------------------------------------------------------------
        print('-------------------------------------------------------------------------------')
         #----------------------------------------------------------------------------------------
        session["val_tags"] = val_tags
        session["tags"] = tags
        session["clos"] = clos
        session["systems"] = sysname
         #----------------------------------------------------------------------------------------

        session["tupleTagsValue"] = listAllTuple
        session["file_name"] = wavefile_name
        redirect(url_for('quick_test_result'))

    # delete  wav and npy files
    # _ = DeleteFile(file_path=WavFile_path)
    # _ = DeleteFile(file_path=NpyFile_path)
    # get tags in this route 
    return render_template('quick_test_result.html', title='Quick Test Result', result=lis, form=form)

#--------------------------------ADVENCED TEST ROUTE-------------------------------------------------------------------

@app.route("/get_detail_result", methods=['GET', 'POST'])
def get_detail_result():
    file_name = session["file_name"]
    tupleTagsValue = session["tupleTagsValue"]

    #----------------------------------------------------------------------------------------
    val_tags = session["val_tags"] 
    tags = session["tags"] 
    clos = session["clos"]
    systems = session["systems"] 
    #----------------------------------------------------------------------------------------
  
    return render_template('get_detail_result.html', title='Detail Of Test Result', file_name=file_name, tupleTagsValue=tupleTagsValue, val_tags=val_tags,tags=tags,clos=clos,systems=systems)

#--------------------------------LOGIN ROUTE-------------------------------------------------------------------
@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You') # for later
    return render_template('login.html', title='Login', form=form)

#--------------------------------REGISTRATION ROUTE-------------------------------------------------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


# definition of function
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

# def sort_dataFrame_result(df):

#     return sorted_result


if __name__ == '__main__':
    app.run(debug=True)