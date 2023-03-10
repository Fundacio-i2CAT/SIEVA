=================================
2. Dataset
=================================

.. contents:: Table of Contents


Raw Data
---------------------

The raw data is entirely obtained from internet traffic logs from diverse protocols (i.e DHCP, DNS... ). 
This logs come in a text message format. We offer the option to, or either train and make predictions using the `fasttext` library text classificator 
model over the text messages itself, or either train a model over a set of extracted features.

A couple of examples of how this logs are received, dns and dhcp respectively:
    - "1331901146.170000	CQOQFp33WT631cLl0h	fe80::223:dfff:fe97:4e12	5353	ff02::fb	5353	udp	0	-	-	-	-	-	-	-	T	F	F	F	0	enigma.local	120.000000	F"
    - "Jan 20 05:59:00 198.24.1.30 dhcpd[8738]: Added new forward map from DGU2C010027.gcc.intranet.gencat.cat to 10.96.20.53"


Fasttext library
----------------------

As the library model is prepared to allow introducing the messages by themselves, the only needed
<<preprocessing>> referes to the concrete way that we have to prepare the input to train the model. 
Precisely, we must compose a file in the following way: first the keyword '\__label\__' (in this exact format), followed
by the category label itself, an space character and the message log in string format (bounded by quotes).
I.e: 
  
  - __label__webserver "tcp_miss get http umbel org umbel rc none application rdf xml"
  - __label__dns "chwsqo jzsgoox udp www google com c_internet"


Feature Engineering
----------------------
Feature engineering is the process of using domain knowledge to extract features
(characteristics, properties, or indicators) from raw data [1]. In this precise
case, the features are limited on what we can extract from the text messages. 
In order to obtain valuable data to distinct among log types, we have decided to extract the following features:

.. list-table:: Features extracted from the logs
   :widths: 25 25 25 25 25
   :header-rows: 1

   * - Feature
     - # of characters
     - # of words
     - # of special characters
     - Special characters ratio
   * - Description
     - Longitude of the log counted character-wise    
     - Longitude of the log counted word-wise
     - Number of non alfanumeric characters in the log
     - Fraction of the special characters over the alfanumeric ones     


As a last step before fitting this data, we normalize it within the same range to avoid problems with the magnitudes.

[1] "Machine Learning and AI via Brain simulations". Stanford University. Retrieved 2022-08-26.