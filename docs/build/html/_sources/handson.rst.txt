=================================
5. Hands-on
=================================

0. Configuration File
=====================

Located in:

.. code-block:: bash
    
    src/config_files/config.ini

Only the ``OPTIONS`` section may be modified. The options are:

.. code-block:: bash
    
    FASTTEXT = False # Choose whether use the fasttext model or not
    SUBSET = 0.001 # Choose the proportion of elements of each class to perform the feature
    RETRIEVE = False # Choose whether retrieve the datasets from elastic before training or not
    PREPARE_DATA = True # Choose whether extract and prepare the data for predicting before doing it
    CREATE = True # Choose whether create the datasets from the raw data or not



1. Start the API
==================

To use the software provided, it is necessary to open a server. Execute the following CLI commands 
to start. 

.. code-block:: bash

   $ cd sieva/
   $ pip install -r requirements.txt
   $ uvicorn AI_Engine.main:app --reload --port 8081 --reload

In the following sections the other endpoints can be explored.



2. Endpoint 1/2: Predict
=========================

Using an already trained and saved model, this endpoint allows you to make predictions over new traffic logs data.
This endpoint gets the data from /data/datasets/predict_set*.txt, with * in [0,...], added as a parameter. We can decide as part
of the initial configuration whether the predictions we are about to perform are bounded in the context of training the model, or we are making actual predictions over 
new data.
In order to perform a prediction over the data already saved in the previous path, acces the endpoint following the next example:

.. code-block:: bash

    $ curl http://127.0.0.1:8081/predict

This call, made in the context of training the model, returns: 

.. code-block:: json

    {
        "Predictions Results" : 
                         
                        {
                            
                            "Accuracy": "0.9978469305502524", 
                            "Recall": "0.9978469305502524", 
                            "F1 score": "0.9978469305502524"

                        },
                    
        "Path to predictions" : "data/datasets/predictions.csv"

    }

In case we are applying the model over new data, instead of the output above, we will receive which portion in % exists of each category 
in the data predicted. To chose the data , we must give as an argument (``predict_index={idx-name}``) the name of the elastic database index:

.. code-block:: bash

    $ curl http://127.0.0.1:8081/predict?predict_index=classification_validate_dataset

This call, made in the context of training the model, returns, for each index provided as parameter: 

.. code-block:: json
    
    "classification_validate_dataset": {
        "Category Split: Data types" : "\"{\\\"dns\\\":25.4433544759,\\\"webserver\\\":24.3785048969,\\\"evtx\\\":23.0140914828,\\\"firewall\\\":13.7913198383,\\\"identity\\\":12.6204246617,\\\"dhcp\\\":0.7523046444}\"",
        "Techniques" : {
            "T1001": "#8cdd69",
            "T1001.001": "#8cdd69",
            "..." : "..."
        },
        "Predictions Results / Path to predictions" : {
            "Path to predictions": "data/predictions/predictions.txt"
        }
    }
    

3. Endpoint 2/2: Train
==========================

The API offers also the option to provide raw data and re-train the model. In order to perform a new training of the selected model, there exists
two options, defined by a boolean parameter (``retrieve_data``)in the moment of the API request: either the parameter is false and the already retrieved raw data data is used,
or it is True, leading to retrieve again the data from the elastic server. 
**Disclaimer: if the parameter is True, the connection must be performed with the i2Cat Fortinet VPN activated.**
add the data in data/raw_data/ as a **file of raw logs, with the log's type as the first word of the file's name (f.i "dns-infloblox-nios.txt")**,
which will be properly processed before being automatically left in data/datasets/fasttext_train.txt. This processed data will be used to train 
the model when an API call with the structure of the following example is performed:


.. code-block:: bash

    $ curl http://127.0.0.1:8081/train

It returns the path were the trained model has been saved, specifically:

.. code-block:: json

    {
        "model path" : "data/model/model.bin"
    }


