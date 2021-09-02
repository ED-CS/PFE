import os
import sys
import numpy as np
import pandas as pd
import librosa


import torch
# import torch.nn as nn
# import torch.backends.cudnn as cudnn
# import torch.optim as optim
from torch.utils.data import DataLoader

from utils import  MelDataset
from models import ResNet

def convert(filename, input_dir, output_dir, SAMPLE_RATE, N_MELS, HOP_LENGTH, N_FFT, FMIN, FMAX):
        file_path = input_dir
        data, _ = librosa.core.load(file_path, sr=SAMPLE_RATE, res_type="kaiser_fast")
        data = librosa.feature.melspectrogram(
            data,
            sr=SAMPLE_RATE,
            n_mels=N_MELS,
            hop_length=HOP_LENGTH, # 1sec -> 128
            n_fft=N_FFT,
            fmin=FMIN,
            fmax=FMAX,
        ).astype(np.float32)
        np.save("{}/{}.npy".format(output_dir, filename), data)
        return data

def prediction(val_loader, model, NUM_CLASS, LOAD_DIR_MODELS, df_predict, labels_path, sysName, dic_predict, nb_tags):
    sigmoid = torch.nn.Sigmoid().cuda()

    # switch to eval mode
    model.eval()

    model.load_state_dict(torch.load("{}/weight_epoch_320.pth".format(LOAD_DIR_MODELS), map_location='cpu'))
    # validate
    preds = np.zeros([0, NUM_CLASS], np.float32)

    # 
    for i, (input, _) in enumerate(val_loader):
        # get batches
        input = torch.autograd.Variable(input.cpu())

    # compute output
    with torch.no_grad():
        output = model(input)
        pred = sigmoid(output)
        pred = pred.data.cpu().numpy()

    preds = np.concatenate([preds, pred])

    df_predict[sysName] = preds[0]
    
    dd = pd.read_csv(labels_path)
    dd[sysName] = preds[0]
    dd = dd.sort_values(by=sysName, ascending=True)

    systemPredection = get_prediction_dic(df=dd, columnName=sysName, nb_tags=nb_tags)
    dic_predict.append(systemPredection)


def load_data(path_npy, NUM_CLASS):
    paths = [path_npy,]
    y = [np.zeros([0, NUM_CLASS], np.float32),]

    dataset_valid = MelDataset(paths, y,)
    valid_loader = DataLoader(dataset_valid, batch_size=1,
                            shuffle=False, num_workers=1, pin_memory=True,
                            )
    return valid_loader 
    
def get_prediction_dic(df, columnName, nb_tags):
    listLabes = []
    listPredectionValue = []
    nb_tags = 79 - nb_tags
    for i in range(79, nb_tags,-1):
        listLabes.append(df.iloc[i]['Dataset'])
        listPredectionValue.append(df.iloc[i][columnName])
                    
    systemPredection =	{
        "systemName": columnName,
        "tagList": listLabes,
        "valueList": listPredectionValue
    }
    return systemPredection


def list_tags(LOAD_DIR_MODELS, output_dir, input_dir, filename, labels_path, nb_tags):

    # parameters
    SAMPLE_RATE = 44100
    N_MELS = 128
    HOP_LENGTH = 347
    N_FFT = 128*20
    FMIN = 20
    FMAX = SAMPLE_RATE//2
    NUM_CLASS = 80


    # convert wav file to npy
    _ = convert(filename=filename, input_dir=input_dir, output_dir=output_dir, 
                SAMPLE_RATE=SAMPLE_RATE, N_MELS=N_MELS, HOP_LENGTH=HOP_LENGTH, 
                N_FFT=N_FFT, FMIN=FMIN, FMAX=FMAX)

    # build model
    model = ResNet(NUM_CLASS) # in case where we using cPU

    # get labels for predect dataframe
    df_predict = pd.read_csv(labels_path)
    valid_loader = load_data(path_npy='{}/{}.npy'.format(output_dir, filename), NUM_CLASS=NUM_CLASS)

    # prediction processe 
    dic_predict = []
    
    for pat in range(5): 
        """ if pat <=2 : 
            sysName = 'System {}'.format(pat)
            prediction(val_loader=valid_loader, model=model, NUM_CLASS=NUM_CLASS,
                        LOAD_DIR_MODELS=LOAD_DIR_MODELS[pat], df_predict=df_predict, labels_path=labels_path, 
                        sysName=sysName, dic_predict=dic_predict, nb_tags=nb_tags)
        else: """
        sysName = 'System {}'.format(pat)
        prediction(val_loader=valid_loader, model=model, NUM_CLASS=NUM_CLASS,
                    LOAD_DIR_MODELS=LOAD_DIR_MODELS[pat], df_predict=df_predict, labels_path=labels_path, 
                    sysName=sysName, dic_predict=dic_predict,nb_tags=nb_tags)
      
    return dic_predict, df_predict

#-------------------------------------------------------------------------------------------------------------- 

#--------------------------------------------------------------------------------------------------------------
def main():

    LOAD_DIR_MODELS = ['C:/Users/mahrati_ed/Desktop/route predection backend/models/system_0',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_1',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_2mean',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_3',
                'C:/Users/mahrati_ed/Desktop/route predection backend/models/system_4']
   
    output_dir = 'C:/Users/mahrati_ed/Desktop/route predection backend/out'
    input_dir ='D:/pfe dataset/test/4c9d698d.wav'
    filename= '4c9d698d'
    labels_path = 'C:/Users/mahrati_ed/Desktop/route predection backend/labels.csv'
    dic_predict, df_predict = list_tags(LOAD_DIR_MODELS=LOAD_DIR_MODELS, output_dir=output_dir, 
                                        input_dir=input_dir, filename=filename, labels_path=labels_path)

    print(dic_predict)
    print(df_predict)

if __name__ == '__main__':
    main()