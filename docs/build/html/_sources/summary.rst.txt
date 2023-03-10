=================================
1. Introduction to SIEVA
=================================

This page contain an overview of SIEVA

.. contents:: Table of Contents

Overview
-------------------------------
SIEVA is a solution made by i2Cat for GÉANT which is intended to accomplish three main purposes (sorted also in the following way):
    1. Identify data sources using uniquely log message as input
    2. Assess the completeness of each data source
    3. Map each data source to TTPs from MITRE ATT&CK Framework.

The project arquitecture is the following one, composed of a SIEM platform, an AI engine and a GUI

.. image:: ../imgs/sieva_arquitecture.png
   :width: 400px
   :height: 180px
   :scale: 100 %
   :alt: alternate text
   :align: center


Realized tasks
-------------------------------
#. **Data obtention**:
#. **Data preparation**:
#. **Model selection**:
#. **Model training**:
#. **API developement**:
#. **UI integration**:


Results obtained
-------------------------------
As part of the first section, the selection of the ``fasttext`` library classification model for text as ML algorithm has been notably good, 
providing a 99.7 in both accuracy and recall in the first task (log type classification).
