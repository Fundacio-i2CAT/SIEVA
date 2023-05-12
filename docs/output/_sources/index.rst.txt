.. SIEVA documentation master file, created by
   sphinx-quickstart on Wed Nov  9 19:07:09 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SIEVA's documentation!
=================================
So far, SIEVA is a machine learning powered software to train a model that is capable to receive
a text message (precisely a traffic log) as an input and identify from which protocol that log comes from.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Quickstart
==================
If you wish to run the API locally, you can use the following commands:

.. code-block:: bash

   cd SIEVA/
   pip install -r requirements.txt
   uvicorn AI_Engine.main:app --reload --port 8081 --reload

Once it has started, you can open your browser to http://127.0.0.1:8081/docs

Configuration File
===================

There are some parameters defined by the configuration file `src/config_files/config.ini`.

.. code-block:: ini

   [PATH]
   RAW_PATH = data/raw_data/
   DATASET_PATH = data/datasets/
   MODEL_PATH = data/model/
   MODEL_PATH_COMPLETENESS = data/model/model-best
   PREDICTIONS_PATH = data/predictions/

   [ELASTIC]
   CLIENT_HOST = localhost

   [OPTIONS]
   RETRIEVE = True
   PREPARE_DATA = True
   RETRIEVE_COMPLETENESS = True


Navigation
===================

.. toctree::
   summary
   data
   model
   integration
   handson
