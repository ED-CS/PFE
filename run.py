import os
from flask import Flask, render_template, url_for, redirect, session, flash, request , Markup
from numpy.lib.function_base import append
from forms import GetTagsForm, LoginForm, RegistrationForm, SystemOptionForm, SystemWieght
from werkzeug.utils import secure_filename
import pandas as pd

from predection_final_version import list_tags, get_prediction_dic


app = Flask(__name__)

app.config['SECRET_KEY'] = '6ea28f4cb420aa71a93faf8acf4c37bd'
app.config['WAV_PATH'] = "wav_file/"
app.config['NPY_PATH'] = "npy_file/"
app.config['LABELS_PATH'] = 'C:/Users/mahrati_ed/Desktop/pfe_app/labels.csv'
app.config['CATEGORY_PATH'] = 'C:/Users/mahrati_ed/Desktop/pfe_app/category.csv'
app.config['LOAD_DIR_MODELS'] = ['C:/Users/mahrati_ed/Desktop/route predection backend/models/system 0/weight_epoch_320.pth',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system 1/weight_epoch_320.pth',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system 2/weight_epoch_512.pth',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system 3/weight_epoch_512.pth',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system 4/weight_epoch_512.pth']
app.config['SYSTEM_NAME'] = ["System 0","System 1","System 2","System 3","System 4"]
app.config['SYSTEM_WIEGHT'] = [320,320,512,512,512]


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

def get_category(tag_name):
    df_category = pd.read_csv(app.config['CATEGORY_PATH'])
    
    
    sub = tag_name
    cat = df_category.loc[df_category["labels"] == sub, "category"]
    return cat.values[0]

def get_dataChart(df_predict,sysname):
    colors = [
        "#808080","#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    val_tags = []
    tags = []
    clos = []
    for sys in sysname:
        j = 1          
        tags_val = 0 
        val = []
        tag = []
        col = []
        for i in range(79, 0, -1): # get all tag > 10% predection
            if df_predict.iloc[i][sys]*100 >= 10:             
                #----------------------------------------------------------------------------------------
                val.append(int(df_predict.iloc[i][sys]*100))
                tag_name = df_predict.iloc[i]['Dataset']
                tag.append(tag_name)

                col.append(colors[j])
                #----------------------------------------------------------------------------------------
                j+=1
                tags_val = tags_val + int(df_predict.iloc[i][sys]*100)
        # add somme value and tag name also tag color of tgs < 10% 
        other_val = 100 - tags_val
        val.append(other_val)
        tag.append("Other Tags")
        col.append(colors[0])
        #---------------------------------------------------------------------------------------- 
        val_tags.append(val) 
        tags.append(tag)  
        clos.append(col)  
    #----------------------------------------------------------------------------------------
    return val_tags, tags, clos

def processing(wav_file, LOAD_DIR_MODELS, nb_tags, systemsName):
            wavefile_name = SaveWavFile(wav_file)
            WavFile_path, NpyFile_path, filename = getFilePaths(wavefile_name=wavefile_name)
             # audio processing and get tags
            dic_predict, df_predict = list_tags(LOAD_DIR_MODELS=LOAD_DIR_MODELS, output_dir=NpyFile_path, 
                                            input_dir=WavFile_path, filename=filename, labels_path=app.config['LABELS_PATH'], 
                                            nb_tags=nb_tags, systemsName=systemsName)

            return dic_predict, df_predict, wavefile_name



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

        # audio processing and get tags
        dic_predict, df_predict, wavefile_name = processing(wav_file = request.files['audio'], 
                                                            LOAD_DIR_MODELS = app.config['LOAD_DIR_MODELS'],nb_tags=int(form.nb_tags.data),
                                                            systemsName = app.config['SYSTEM_NAME'])
        # lis.append(df_predict)
        # lis.append(dic_predict)
        # lis.append(wavefile_name)
        
        #----------------ensembling system ------------------------------------------------------------------
        df_predict["ensemble"] = df_predict.sum(axis=1)/5
        df_ensemble = pd.read_csv(app.config['LABELS_PATH'])
        df_ensemble["ensemble"] = df_predict["ensemble"]
        df_ensemble = df_ensemble.sort_values(by="ensemble", ascending=True)
       
        # get data chart for ensembling system
        val_esTags, esTags, esClos = get_dataChart(df_predict=df_ensemble, sysname=["ensemble"])
        # get data chart for ensembling system
        ensemble_dataDict = get_prediction_dic(df=df_ensemble, columnName="ensemble", nb_tags = int(form.nb_tags.data))
        #----------------------------------------------------------------------------------------------------
        dic_predict.append(ensemble_dataDict)
        lis.append(df_predict)
        print(df_predict)
        lis.append(dic_predict)
        lis.append(wavefile_name)
        # get data for chart all systems
        val_tags, tags, clos = get_dataChart(df_predict=df_predict, sysname=app.config['SYSTEM_NAME'])

        val_tags.append(val_esTags[0])
        tags.append(esTags[0]) 
        clos.append(esClos[0])
        # save data chart in session
        session["val_tags"] = val_tags
        session["tags"] = tags
        session["clos"] = clos
        session["systems"] = app.config['SYSTEM_NAME']
        session["file_name"] = wavefile_name
        session["systemWeight"] = app.config['SYSTEM_WIEGHT']
        
        redirect(url_for('quick_test_result'))

    # delete  wav and npy files
    # _ = DeleteFile(file_path=WavFile_path)
    # _ = DeleteFile(file_path=NpyFile_path)
    # get tags in this route 
    return render_template('quick_test_result.html', title='Quick Test Result', result=lis, form=form)

#--------------------------------FUll System - One System ROUTE-------------------------------------------------------------------

@app.route("/FUllSystem_oneSystem", methods=['GET', 'POST'])
def FUllSystem_oneSystem():
    # get tags of audio file using one system with specific wight
    # code for one system
    form = SystemOptionForm()
    if form.validate_on_submit():
        systemName = form.systemName.data
        systemWeight= int(form.systemWeight.data)
      
        systemPath = ['C:/Users/mahrati_ed/Desktop/route predection backend/models/{}/weight_epoch_{}.pth'.format(systemName, systemWeight)]
    
        dic_predict, df_predict, wavefile_name = processing(wav_file = request.files['audio'], 
                                                            LOAD_DIR_MODELS = systemPath,nb_tags=int(form.nb_tags.data), systemsName=[systemName])

        val_tags=[]
        tags = []
        clos = []
        # get data for chart
        val_tags, tags, clos = get_dataChart(df_predict=df_predict, sysname=[systemName])
        
        # save data chart in session
        session["val_tags"] = val_tags
        session["tags"] = tags
        session["clos"] = clos
        session["systems"] = [systemName]
        session["file_name"] = wavefile_name
        session["systemWeight"] = systemWeight
        
        return redirect(url_for('get_detail_result', systemType = 'One System Result'))

    return render_template('FUllSystem_oneSystem.html', form=form, title='One System', erreur= app.config['erreur'])

 #--------------------------------FUll System - All System ROUTE-------------------------------------------------------------------

@app.route("/FUllSystem_allSystem", methods=['GET', 'POST'])
def FUllSystem_allSystem():
    # get tags of audio file using all system with specific wights
    form = SystemWieght()
    app.config['erreur']='okay'
    sysWieght = [320, 320]
    if form.validate_on_submit():
        sysWieght.append(int(form.sys2.data))
        sysWieght.append(int(form.sys3.data))
        sysWieght.append(int(form.sys4.data))
        paths = []
        for i in range(5):
            paths.append('C:/Users/mahrati_ed/Desktop/route predection backend/models/system {}/weight_epoch_{}.pth'.format(i, sysWieght[i]))

        dic_predict, df_predict, wavefile_name = processing(wav_file = request.files['audio'], LOAD_DIR_MODELS = paths ,
                                                            nb_tags=int(form.nb_tags.data), systemsName=app.config['SYSTEM_NAME'])  
        # creat a ensemble column in df_predict
        df_predict["ensemble"] = df_predict.sum(axis=1)/5                                                  
        systemname = ["System 0","System 1","System 2","System 3","System 4", "ensemble"]
        # get data for chart
        val_tags, tags, clos = get_dataChart(df_predict=df_predict, sysname=systemname)
        # save data chart in session
        session["val_tags"] = val_tags
        session["tags"] = tags
        session["clos"] = clos
        session["systems"] = app.config['SYSTEM_NAME']
        session["file_name"] = wavefile_name
        session["systemWeight"] = sysWieght
        return redirect(url_for('get_detail_result', systemType = 'All System Result'))
        
    #  code for all system 
    return render_template('FUllSystem_allSystem.html', form=form, title='Full Systems')

#--------------------------------ADVENCED TEST ROUTE-------------------------------------------------------------------

@app.route("/get_detail_result/<string:systemType>", methods=['GET', 'POST'])
def get_detail_result(systemType):
    file_name = session["file_name"]
    val_tags = session["val_tags"] 
    tags = session["tags"] 
    clos = session["clos"]
    systems = session["systems"] 
    systemWeight = session["systemWeight"]
    return render_template('get_detail_result.html', title=systemType,
                            file_name=file_name, val_tags=val_tags, tags=tags,
                            clos=clos, systems=systems, systemWeight=systemWeight) 

"""
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
    return render_template('register.html', title='Register', form=form) """



# def sort_dataFrame_result(df):

#     return sorted_result


if __name__ == '__main__':
    app.run(debug=True)