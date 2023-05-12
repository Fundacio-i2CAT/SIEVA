# This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT)
import io
import AI_Engine.core.data_handler as data
import AI_Engine.core.utils as utils
import AI_Engine.core.model as model
import AI_Engine.core.mapping.mapping_techniques_data_sources as mapping
import pandas as pd
import spacy as sp

import logging
import os
import json
import sys
from logging.handlers import RotatingFileHandler


from fastapi.logger import logger
from typing import List
from fastapi import FastAPI, Request
from spacy import displacy
from tqdm import tqdm


from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Preguntar si els possibles origins d'acces a la API han de ser part d'un input/fitxer de config
origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:4200",
    "http://localhost:4201",
    "http://localhost:9000",
    "http://localhost:9001",
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:4200",
    "http://localhost:4201",
    "http://localhost:9000",
    "http://localhost:9001",

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = utils.load_config("AI_Engine/config_files/")
    
dataset_path = config.get("PATH", "DATASET_PATH")
model_path = config.get("PATH", "MODEL_PATH")
rawData_path = config.get("PATH", "RAW_PATH")
predictions_path = config.get("PATH", "PREDICTIONS_PATH")

elastic_host = config.get("ELASTIC", "CLIENT_HOST")

@app.get("/train")
async def train_model(
     train_pairs: str =
     """
     {"webserver" : ["webproxy-squid", "webserver-generic", "webserver-nginx"], 
      "dns" : ["dns-infoblox-nios", "dns-generic"],  
      "identity" : ["identity-service-cisco"], 
      "evtx" : ["microsoft-windows-evtx"], 
      "firewall" : ["firewall-fortigate","firewall-paloalto"]
      }
     """
    ): 

    """
    Endpoint to re-train the model selected through configuration file
    :param train_pairs: str that represents a mapping between each category and each index used to train
    """
    logging.basicConfig(level=logging.DEBUG, filename='logs/train', filemode='w')
    logger.addHandler(RotatingFileHandler("logs/train", maxBytes=1000,backupCount=0))

    retrieve = config.getboolean("OPTIONS", "RETRIEVE")
    prepare_data = config.getboolean("OPTIONS", "PREPARE_DATA")
    fasttext_flag = config.getboolean("OPTIONS", "FASTTEXT")
    False
    global dataset_path, model_path, rawData_path, elastic_host
    
    logger.debug(f'[PATH] Dataset Path:{dataset_path}')
    logger.debug(f'[PATH] Model Path:{model_path}')
    logger.debug(f'[PATH] RawData Path:{rawData_path}')
    logger.debug(f'[OPTIONS] FASTTEXT?:{fasttext_flag}')
    logger.debug(f'[HOST] ElasticSearch database host: {elastic_host}')
    logger.debug(f'[Model Type] Model used:{"fasttext multinomial logistic regression" if fasttext_flag else "XGBoost"}')

    train_pairs = json.loads(train_pairs)
    train_pairs = utils.exchange_key_value(train_pairs)

    
    if prepare_data:
        print('entro')
        if retrieve:
            utils.get_datasets_elastic(client_host = elastic_host, datasets_path = rawData_path, search_object={"query": {"match_all": {}}},  all_idx=False,
                                    idx_names = list(train_pairs.keys()))# list(train_pairs.values()))

        if fasttext_flag:
            train_path, _ = data.create_datasets(path_to_rawData = rawData_path, path_to_datasets = dataset_path+'fasttext_', 
                                    training_data=False, idx_pairs=train_pairs, predict = False)
    
    model_name = 'model.bin' 

    try:
        model.train_model(train_path, path_save_model = model_path+model_name, fasttext_flag = fasttext_flag)
       
        config.set("PATH", "MODEL_PATH", model_path+model_name)
        return {"model path" : model_path+model_name}
    
    except: 
        raise UnboundLocalError('Data is not saved, modify the config.ini: [PREPRARE_DATA]=True & [RETRIEVE]=True to retrieve the data')



    

@app.get("/predict")
async def predict(predict_idxs: str = """["classification_validate_dataset","index1", "index2", "index3"]""", re_execution: str = "False"): 
    """
    Endpoint that allows to Load a pretrained model to make predictions over data.
    :param predict_idxs: str that represents a list of index names to extract the datsets to perform predictions on
    """
    logging.basicConfig(level=logging.DEBUG, filename='logs/predict', filemode='w')

    re_execution = re_execution == "True"
    model_path = config.get("PATH", "MODEL_PATH")


    if re_execution or len(os.listdir('results')) == 0:
        fasttext_flag = config.getboolean("OPTIONS", "FASTTEXT")
        prepare_data = config.getboolean("OPTIONS", "PREPARE_DATA" )
        retrieve = config.getboolean("OPTIONS", "RETRIEVE")

        global dataset_path, rawData_path, elastic_host

        predict_idxs =  json.loads(predict_idxs) 

        if not os.path.isfile(model_path): 
            model_path = model_path + 'model.bin' 
        
        if prepare_data:
            if retrieve: utils.get_datasets_elastic(elastic_host, datasets_path = rawData_path, search_object={"query": {"match_all": {}}}, idx_names = predict_idxs, all_idx=False)

            if fasttext_flag: 
                _ , test_path = data.create_datasets(path_to_rawData = rawData_path, path_to_datasets=dataset_path, training_data=False, 
                predict=True, predict_idx = predict_idxs, idx_pairs={})

        
        logger.debug(f'[PATH] Dataset Path:{dataset_path}')
        logger.debug(f'[PATH] Model Path:{model_path}')
        logger.debug(f'[PATH] Predictions Path:{predictions_path}')
        logger.debug(f'[OPTIONS] FASTTEXT?:{fasttext_flag}')

        output = {}

        for predict_index in predict_idxs:

            file_name = f'fasttext_test-{predict_index}.txt'

            results = model.predict(dataset_path+file_name, model_path, predictions_path, fasttext_flag = fasttext_flag)
            data_sources = utils.category_percent(results['Path to predictions'], data_sources = True).keys()
            
            output[predict_index] = {
                                        "Category Split: Data types" : utils.category_percent(results['Path to predictions'], data_sources = False),
                                        "Techniques" : mapping.dataSources2techniques(data_sources),
                                        "Predictions Results / Path to predictions" : results
                                    }
            
        
        output['MITRE'] = utils.technique_overlapping(output)
        output['log-entities'] = json.load(open("entities.json",))
        print(output)

        for key, _ in output.items():
            if key in predict_idxs:
                del output[key]["Techniques"]

        from datetime import datetime

        with open(f'results/{datetime.now()}.json', 'w') as results_file:
            json.dump(output, results_file, indent = 4)
    
    else: 
        file = r'results/'+ str(max(os.listdir('results')))
        output = json.load(open(file,))
        

    try:
        os.path.isfile(model_path)
        return output
    except FileNotFoundError as fnf:
        print(fnf)
        

@app.get("/get_results")
async def get_results():
        try:
            file = r'results/'+ str(max(os.listdir('results')))
            return json.load(open(file,))
        except:
            return "File not available"


@app.get("/assert_completeness")
async def predict_completeness(predict_idxs: str = """["webproxy-squid","webserver-nginx","webserver-generic"]"""):

    """
    Endpoint to assert the completeness over a set of given indexes
    :param predict_idxs: str that represents a list of index names to extract the datsets to perform predictions on 
    """

    model_path = config.get("PATH", "MODEL_PATH_COMPLETENESS")
    rawData_path = config.get("PATH", "RAW_PATH")
    retrieve = config.getboolean("OPTIONS", "RETRIEVE_COMPLETENESS")

    logging.basicConfig(level=logging.DEBUG, filename='logs/predict', filemode='w')
    logger.debug(f'[PATH] Model Path:{model_path}')
    logger.debug(f'[PATH] RawData Path:{rawData_path}')
    logger.debug(f'[OPTIONS] Data retrieved? :{retrieve}')

    predict_idxs = json.loads(predict_idxs)

    if retrieve: utils.get_datasets_elastic(elastic_host, datasets_path = rawData_path, search_object={"query": {"match_all": {}}}, idx_names = predict_idxs, all_idx=False)
    
    nlp_ner = sp.load(model_path)

    output_dict = {}
    named_entities = []

    for idx in predict_idxs:

        print('Extracting from ', idx)
        test_data = open(f"{rawData_path}/{idx}.txt")
        test_data_lines = test_data.read().splitlines()[0:100]
        test_data.close()

        for line in tqdm(test_data_lines):
            doc = nlp_ner(line)
            output_dict[line] = []
            for ent in doc.ents:
                 output_dict[line].append((ent.text, ent.start_char, ent.end_char, ent.label_))
                 if ent.label_ not in named_entities:
                     named_entities.append(ent.label_)
        
        return {"named_entities" : named_entities,
                "entities_by_point" : output_dict
                }

     

@app.get("/dummy")    
async def dummy_endpoint():
    idxs_sources =  [   {
                "index_1" :   
                        {
                            "Network Traffic Content (webserver)": "64.8824296805",
                            "Domain Name: Active DNS": "86.136300963",
                            "Network Traffic Content": "19.0061410207",
                            "Filebeat values are waiting...": "12.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "0.8545988715",
                            "User Account: User Account Creation": "0.8545988715",
                            "User Account: User Account Deletion": "0.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "0.3070510373",
                            "Process: Process Access": "0.3070510373",
                            "Process: Process Creation": "0.3070510373",
                            "Process: Process Metadata": "0.3070510373",
                            "Process: Process Modification": "0.3070510373",
                            "Process: Process Termination": "0.3070510373"
                        }
                },
                
                {           
                "index_2" :  
                        {
                            "Network Traffic Content (webserver)": "34.8824296805",
                            "Domain Name: Active DNS": "86.136300963",
                            "Network Traffic Content": "49.0061410207",
                            "Filebeat values are waiting...": "8.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "4.8545988715",
                            "User Account: User Account Creation": "4.8545988715",
                            "User Account: User Account Deletion": "4.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "0.3070510373",
                            "Process: Process Access": "0.3070510373",
                            "Process: Process Creation": "0.3070510373",
                            "Process: Process Metadata": "0.3070510373",
                            "Process: Process Modification": "0.3070510373",
                            "Process: Process Termination": "0.3070510373"
                        }
                },
                
                {           
                "index_3" :  
                        {
                            "Network Traffic Content (webserver)": "64.8824296805",
                            "Domain Name: Active DNS": "46.136300963",
                            "Network Traffic Content": "19.0061410207",
                            "Filebeat values are waiting...": "12.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "0.8545988715",
                            "User Account: User Account Creation": "0.8545988715",
                            "User Account: User Account Deletion": "0.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "20.3070510373",
                            "Process: Process Access": "20.3070510373",
                            "Process: Process Creation": "20.3070510373",
                            "Process: Process Metadata": "20.3070510373",
                            "Process: Process Modification": "20.3070510373",
                            "Process: Process Termination": "20.3070510373"
                        }
                }
            ]
    idxs_types = [   {
                "index_1" :   
                        {   "filebeat": "76.7458580307",
                            "evtx" : "12.5517246889",
                            "dns" : "9.4877857839",
                            "webserver" : "1.2146314965"
                        }
                },
                
                {           
                "index_2" :  
                        {   "filebeat": "66.7458580307",
                            "evtx" : "17.5517246889",
                            "dns" : "14.4877857839",
                            "webserver" : "1.2146314965"
                        }
                },
                
                {           
                "index_3" :  
                        {   "filebeat": "56.7458580307",
                            "evtx" : "22.5517246889",
                            "dns" : "19.4877857839",
                            "webserver" : "1.2146314965"
                        }
                }
            ]

    mitre = json.load(open('AI_Engine/production_src/dummy_techniques.json',))

    dummy_dict = {
        "MITRE" : mitre,
        "log-sources" : idxs_sources ,
        "log-types" :  idxs_types     
    }

    return(json.dumps(dummy_dict, indent=4))


@app.get("/dummy__")    
async def dummy_endpoint__():

    idxs_sources =  [   {
                "index_1" :   
                        {
                            "Network Traffic Content (webserver)": "64.8824296805",
                            "Domain Name: Active DNS": "86.136300963",
                            "Network Traffic Content": "19.0061410207",
                            "Filebeat values are waiting...": "12.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "0.8545988715",
                            "User Account: User Account Creation": "0.8545988715",
                            "User Account: User Account Deletion": "0.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "0.3070510373",
                            "Process: Process Access": "0.3070510373",
                            "Process: Process Creation": "0.3070510373",
                            "Process: Process Metadata": "0.3070510373",
                            "Process: Process Modification": "0.3070510373",
                            "Process: Process Termination": "0.3070510373"
                        }
                },
                
                {           
                "index_2" :  
                        {
                            "Network Traffic Content (webserver)": "34.8824296805",
                            "Domain Name: Active DNS": "86.136300963",
                            "Network Traffic Content": "49.0061410207",
                            "Filebeat values are waiting...": "8.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "4.8545988715",
                            "User Account: User Account Creation": "4.8545988715",
                            "User Account: User Account Deletion": "4.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "0.3070510373",
                            "Process: Process Access": "0.3070510373",
                            "Process: Process Creation": "0.3070510373",
                            "Process: Process Metadata": "0.3070510373",
                            "Process: Process Modification": "0.3070510373",
                            "Process: Process Termination": "0.3070510373"
                        }
                },
                
                {           
                "index_3" :  
                        {
                            "Network Traffic Content (webserver)": "64.8824296805",
                            "Domain Name: Active DNS": "46.136300963",
                            "Network Traffic Content": "19.0061410207",
                            "Filebeat values are waiting...": "12.7020491282",
                            "Network Traffic Content (DHCP)": "2.2477302618",
                            "User Account: User Account Authentication": "0.8545988715",
                            "User Account: User Account Creation": "0.8545988715",
                            "User Account: User Account Deletion": "0.8545988715",
                            "User Account: User Account Modification": "1.709197743",
                            "User Account: User Account Metadata": "0.8545988715",
                            "Process: OS API Execution": "20.3070510373",
                            "Process: Process Access": "20.3070510373",
                            "Process: Process Creation": "20.3070510373",
                            "Process: Process Metadata": "20.3070510373",
                            "Process: Process Modification": "20.3070510373",
                            "Process: Process Termination": "20.3070510373"
                        }
                }
            ]
    idxs_types = [   {
                "index_1" :   
                        {   "filebeat": "76.7458580307",
                            "evtx" : "12.5517246889",
                            "dns" : "9.4877857839",
                            "webserver" : "1.2146314965"
                        }
                },
                
                {           
                "index_2" :  
                        {   "filebeat": "66.7458580307",
                            "evtx" : "17.5517246889",
                            "dns" : "14.4877857839",
                            "webserver" : "1.2146314965"
                        }
                },
                
                {           
                "index_3" :  
                        {   "filebeat": "56.7458580307",
                            "evtx" : "22.5517246889",
                            "dns" : "19.4877857839",
                            "webserver" : "1.2146314965"
                        }
                }
            ]
    entities =  [ { 
                    "index_1" : 
                              { 
                                "firewall": ["FILENAME", "PACKETS-SENT", "URL", "SORUCE", "APPLICATION", "PACKETS-RECEIVED", "BYTES-SENT", "BYTES-RECEIVED"],
                                "dns" : ["IP", "PROTOCOL", "CODE", "BYTES-SENT", "URL", "USER_AGENT"],
                                "webserver" : ["IP", "URL", "HTTP-CODE", "HTTP-METHOD"],
                                "evtx" : [],
                                "filebeat" : []
                              }
                  },
                  { 
                    "index_2" : 
                              {   
                                "firewall": ["FILENAME", "URL", "SORUCE", "APPLICATION", "BYTES-SENT", "BYTES-RECEIVED"],
                                "dns" : ["IP", "PROTOCOL", "CODE", "URL"],
                                "webserver" : ["IP", "URL", "HTTP-CODE", "HTTP-METHOD"],
                                "evtx" : [],
                                "filebeat" : []
                              }
                  },  
                  { 
                    "index_3" : 
                              { 
                                "firewall": ["FILENAME", "PACKETS-SENT", "URL", "SORUCE", "APPLICATION", "PACKETS-RECEIVED"],
                                "dns" : ["IP", "PROTOCOL", "CODE", "BYTES-SENT", "URL"],
                                "webserver" : ["IP", "URL", "HTTP-METHOD"],
                                "evtx" : [],
                                "filebeat" : []
                              }
                  }
                ]
                

    mitre = json.load(open('AI_Engine/production_src/dummy_techniques.json',))

    dummy_out_full = {
        "MITRE" : mitre,
        "log-sources" : idxs_sources ,
        "log-types" :  idxs_types,
        "log-entities" : entities     
    }

    dummy_out_complete = [{'techniqueID' : technique, 'color': color} for technique, color in mitre.items() if color == "#8cdd69"]
    dummy_out_partial = [{'techniqueID' : technique, 'color': color} for technique, color in mitre.items() if color == "#ffd966"] 
    dummy_out_missing = [{'techniqueID' : technique, 'color': color} for technique, color in mitre.items() if color == "#ed4f4f"] 

    saving_path = "data/api_out/"
    files_paths = list(map(lambda file: saving_path+file, ['dummy_out_full.txt', 'dummy_out_complete.txt', 'dummy_out_partial.txt', 'dummy_out_missing.txt']))

    outputs = [dummy_out_full, dummy_out_complete, dummy_out_partial, dummy_out_missing]

    for path, output in zip(files_paths, outputs):
        with open(path, 'w') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

    return dummy_out_full
    
               

@app.get("/loadConfig")    
async def loadConfig():

    with open("data/api_out/MatrixConfigurationFinal.json", "rb") as _fh:
        return StreamingResponse(io.BytesIO(_fh.read()), media_type="application/json; charset=utf8")

@app.post("/uploadConfig")    
async def uploadConfig(data: Request):

    conf = await data.json()
    try:
        with open('data/api_out/MatrixConfigurationFinal.json', 'w', encoding='utf-8') as outfile:
            json.dump(conf, outfile, ensure_ascii=True, indent=4)
        return "OK"
    except IOError as e:
        return e