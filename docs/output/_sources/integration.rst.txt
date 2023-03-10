=================================
4. Integration
=================================

.. contents:: Table of Contents

API Routes
===============
Next, are listed the API routes :

.. list-table::
   :widths: 12 12 24
   :align: center
   :header-rows: 1

   * - Endpoint
     - HTTP Method
     - Description
   * - /predict/
     - GET
     - Predict new data using a previous model, stored in /data/model/fasttext_model.bin, with the data stored /data/datasets/fastext_test*.txt. Use the ``predict_index`` parameter to chose the index in which we can obtain of data  to predict.
   * - /train/
     - GET
     - Train a new model and store it in the predefined model path /src/config_files. Use the parameter ``retrieve_data`` to decide wether extract the data from elastic server again or not



Project Structure
==================

The project has the following structure:

.. code-block:: bash

   src/
    config_files/
        config.ini
    core/
        data_handler.py
        model.py
        utils.py
    main.py
   data/
      datasets/
      model/
      predictions/
      raw_data/
   docs/
      build/
   requirements.txt


where,

* */src directory*, contain the scripts to handle the data, retrieve it from the server and modify it (data_handler.py), train a ML model and predict using it (model.py), a script for secundary functions that may be used in multiple scripts (utils.py).

* */docs directory*, contain the sphinx documentation. The index file is located at /docs/build/index.html

* */data directory*, contain directories to store raw data, the processed datasets to make predictions, the pre-trained models and it is also where the predictions over the datasets are saved.

