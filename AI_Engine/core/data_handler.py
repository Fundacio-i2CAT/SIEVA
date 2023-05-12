# This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT)
import AI_Engine.core.utils as utils
#import utils as utils
import pandas as pd
import numpy as np
import os
import re
import threading 

from typing import Union
from tqdm import tqdm

from os.path import basename
from sklearn.model_selection import train_test_split

from gensim.utils import simple_preprocess

dataframe = pd.core.frame.DataFrame

TRAIN_idx_to_extract = ['dhcp-server-linux.txt', 'dns-generic.txt', 'dns-infoblox-nios.txt', 'firewall-fortigate.txt', 
                  'firewall-paloalto.txt', 'identity-service-cisco.txt', 'webproxy-squid.txt', 'webserver-generic.txt', 
                  'webserver-nginx.txt', 'microsoft-windows-evtx.txt', 'classification_validate_dataset.txt', 'index1.txt', 'index2.txt', 'index3.txt'] 


idx_pairs = {'webproxy-squid': 'webserver', 'webserver-generic': 'webserver', 'webserver-nginx': 'webserver', 'dns-infoblox-nios': 'dns', 'dns-generic': 'dns', 
                'identity-service-cisco': 'identity', 'microsoft-windows-evtx': 'evtx', 'firewall-fortigate': 'firewall', 'firewall-paloalto': 'firewall', 
                'dhcp-server-linux' : 'dhcp'}


def create_datasets(path_to_rawData : str = 'data/raw_data/',  path_to_datasets : str = 'data/datasets/', training_data: bool = False, 
    predict: bool = False, idx_pairs: dict = idx_pairs, predict_idx = ["classification_validate_dataset.txt", 'index1', 'index2', 'index3']):
    """
    Use the raw data retrieved from elastic to create usable datasets to train a model
    :param path_to_rawData: path to acces the raw data retrieved from elastic
    :param path_to_datasets: path to save the processed datasets
    :param fasttext: flag to whether use or not the fasttext library, thus processing the data in a way that fasttext can recognize
    :return: tuple with train and test data
    """
    data = pd.DataFrame()
    files = os.listdir(path_to_rawData) if os.path.isdir(path_to_rawData) else [path_to_rawData]

    files = list(filter(lambda file: file.replace('.txt','') in idx_pairs.keys(), files)) if not predict else [pred_idx+'.txt' for pred_idx in predict_idx]

    for file in files:
        file_idx = file.replace('.txt','')
        if file_idx in idx_pairs.keys() or file_idx in predict_idx and os.path.isfile(path_to_rawData+file):
            # Obtaining the message column and the category in which belongs 
            x_data = pd.read_table(path_to_rawData+file, header = None, lineterminator='\n', on_bad_lines='skip')
            y_data = idx_pairs[file_idx] if file_idx in idx_pairs.keys() else file_idx
                
            current = pd.concat([x_data,pd.Series(np.repeat(y_data,x_data.shape[0]))], axis=1, ignore_index=True)
        
            data = pd.concat([data,current],ignore_index=True)
    
    data.columns=['log', 'target: log-type']
    data.applymap(str)

    if training_data:
        data = train_test_split(data,test_size = 0.24, random_state = 24, stratify = data.iloc[:,-1])
        train, test = data[0],[1]
        
        train_path = fasttext_format(train, training_data=training_data, predict=False)
        test_path = fasttext_format(test, training_data=training_data, predict=False)

        return train_path, test_path

    else:
        if not predict:
            data =  data.loc[~data['target: log-type'].isin(predict_idx)]
            train_path = fasttext_format(data, path_to_datasets, predict=predict)

            return train_path, None

        else:
            test_paths = []
            for idx in predict_idx:
                data_idx = data.loc[data['target: log-type'] == idx]
                test_path = fasttext_format(data_idx, path_to_datasets, predict=predict,idx_name=idx)
                test_paths.append(test_path)
            
            return None, test_paths


def fasttext_format(data, path_to_datasets: str = "data/datasets/", training_data: bool = False, predict: bool = False, idx_name: str = 'classification_validate_dataset'):
    """
    Format the data in a way that the fasttext library can use
    :param data: tuple of all the data retrieved, already splitted in train and test 
    :param path_to_datasets: path to save the processed datasets
    """
    
    X, y = data.iloc[:,0], data.iloc[:,-1]

    dataset = pd.DataFrame(list(zip(y,X)))
    dataset.iloc[:,1] = dataset.iloc[:, 1].astype(str).apply(lambda x: ' '.join(simple_preprocess(x)))
    dataset.iloc[:,0] = dataset.iloc[:,0].apply(lambda x: '__label__' + x) if not predict or training_data else None

    data_path = path_to_datasets + "fasttext_train.txt" if not predict else path_to_datasets + f"fasttext_test-{idx_name}.txt"

    dataset.to_csv(data_path, sep = " ", header = False, index = False)
        
    return data_path
    



if __name__ == '__main__': 

    """
    Only used for testing purposes, do not rely on the following code to extract information about the execution
    """
    config = utils.load_config("../config_files")
    rawData_path = "data/raw_data/"
    dataset_path = "data/datasets/"

    db_host = "127.0.0.1" 

    fasttext = True 
    
    print(os.path.exists("../../data/"))
    # utils.get_datasets_elastic(client_host = db_host, datasets_path = rawData_path, all_idx=False)
    
    data = create_datasets(path_to_rawData = f"{rawData_path}", path_to_datasets = f"{dataset_path}", fasttext = fasttext) 
    #predict_index = 'classification_validate_dataset.txt'

    print(data[0], data[1])
    test_data = pd.read_csv(data[0])
    train_data = pd.read_csv(data[1])

    print(train_data)
    print(test_data)
    




    #