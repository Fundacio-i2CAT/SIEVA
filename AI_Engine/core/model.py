# This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT)
import numpy as np
import pandas as pd
import AI_Engine.core.utils as utils
#import utils
import os
import joblib

from gensim.utils import simple_preprocess

from fasttext import train_supervised, load_model
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report

from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight 
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier


SS = StandardScaler()

def train_model(path_to_train_data: str = "data/datasets/train.txt", path_save_model: str = 'data/model/', fasttext_flag: bool = True):
    """
    Train a text classificator based on either the fasttext library or an own XGBoost from the library equally named. The frist model uses a bag of n-grams, with hashing to mantain fast and memory efficient mapping of the n-grams.
    The classification task is made with a multinomial logistic regression. Goes through a softmax to obtain a probability distribution over pre-defined classes.
    If the number of classes is large enough, Hierarchial Softmax is used, in which every node in a binary tree represents a probability, with the leafs of the tree representing the labels.
    This reduce the computational complexity, with k being the number of classes and h the dimension of the text representation, from O(kh) to O(h*log(k)).
    The second one, applies 3 folds of validation, generating a tree with at maximum depth = 12. It is executed concurrently among as much available threads possible.
    :param path_to_train_data: path to the preprocessed dataset to train 
    :param path_save_model: path to save the trained model that can be used to predict afterwards
    """
    if fasttext_flag:

        model = train_supervised(path_to_train_data) 
        
    model.save_model(path_save_model)
    return {'Model path:' : path_save_model}


def predict_fasttext(model, path_to_test_data: str = "data/datasets/test.txt", training_data: bool = False):
    """
    Make predictions with a presaved model from the fasttext library
    :param model: the model object to use to make the predictions
    :param path_to_test_data: the path to the data to make the predictions
    :param training_data: flag, make predictions over a training context or not
    """
    #If we are training the model, the data will include the log type values, otherwise we just get the lines and we put it through the simple preprocess
    test_df = pd.read_csv(path_to_test_data, sep = " ") if training_data else pd.Series(open(path_to_test_data, 'r').readlines()).astype(str).apply(lambda x: ' '.join(simple_preprocess(x)))
    
    if training_data: test_logs, test_labels = test_df.iloc[:,-1], test_df.iloc[:,0]
    else: test_logs = test_df

    predictions  = []
    for _, log in test_logs.astype(str).items():
        predicted_label = model.predict(log.replace("\n",''))[0][0].replace('__label__', '') 
        predictions.append([log,predicted_label])
                
            
    predictions = pd.DataFrame(predictions, columns = ['log_message', 'predicted_label'])
    if training_data: y_true = test_labels.apply(lambda label: label.replace('__label__',''))

    if training_data: return predictions, y_true
    else: return predictions


def predict(path_to_test_data: str = "data/datasets/test.txt", path_to_model: str = 'data/model/model_fast.bin', path_to_predictions: str = "data/datasets/predictions/", 
            fasttext_flag: bool = True, training_data: bool = False):
    """
    Use a pre-trained text classificator to make predictions on a new corpus
    :param path_to_test_data: path to the preprocessed dataset to test the model 
    :param path_to_model: path to acces the pre-trained model to make predictions
    :param path_to_predictions: path to save the predictions made by the model
    """
    #We load the model from the path with the saved model
    model = load_model(path_to_model)

    if training_data:
        y_pred, y_true = predict_fasttext(model, path_to_test_data, training_data)
    else:
        y_pred = predict_fasttext(model, path_to_test_data, training_data)

    file_name = 'predictions.txt' 
 
    y_pred.to_csv(path_to_predictions+file_name)
    

    if training_data:
        return { 
             'Path to predictions': path_to_predictions+file_name,
             'Accuracy' : accuracy_score(y_true.astype(str), y_pred.astype(str)),
             'Recall' : recall_score(y_true.astype(str), y_pred.astype(str), average='micro'),
             'F1 score' : f1_score(y_true.astype(str), y_pred.astype(str), average='micro'),
             '\nclassification report ' : classification_report(y_true.astype(str), y_pred.astype(str), output_dict = True)
            }
    else: return {'Path to predictions': path_to_predictions+file_name }


if __name__ == '__main__': 
    #This section is just used for testing purposes
    path_to_config = "AI_Engine/config_files"
    config = utils.load_config(os.path.abspath(path_to_config))
    dataset_path = config.get("PATH", "DATASET_PATH")
    model_path = config.get("PATH", "MODEL_PATH")
    predictions_path = config.get("PATH", "PREDICTIONS_PATH")
    
    fasttext_flag = False


    for fasttext_flag in [False, True]:
        train_path = 'fasttext_train_dataset.txt' if fasttext_flag else 'extracted_features_train.txt'#DEF-extracted_features_train.txt'
        test_path = 'fasttext_test_dataset.txt' if fasttext_flag else 'predict_extracted_features_test.txt'

        print('creuat path')
        # to use the full set is required to modify the dataset to not have the pcap data and in order to see if we can obtain
        # better predictions we must balance the quantity of the filebeat class
        model_name = 'model_fast.bin' if fasttext_flag else 'model_non_fast.plk'
        # print(train_model(dataset_path+train_path,model_path+model_name,fasttext_flag=fasttext_flag))
        print(f'-------END TRAIN-------{fasttext_flag}\n')
        # print(predict(dataset_path+test_path, model_path+model_name, predictions_path, fasttext_flag = fasttext_flag, training_data = False))
        cat_percent = utils.category_percent("data/predictions/fasttext_predictions.txt") if fasttext_flag else utils.category_percent("data/predictions/feature_extraction_predictions.txt")
        print(cat_percent)