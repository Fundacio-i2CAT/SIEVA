<div style="display: flex; justify-content: space-between;">
  <div style="position: relative;">
    <img src="https://wikifab.org/images/b/b6/Group-i2CAT_logo-color-alta.jpg" style="width: 25%; height: 25%; position: absolute; left: 0;">
  </div>
  <div style="position: relative;">
    <img src="https://github.com/Fundacio-i2CAT/SIEVA/blob/master/logo.PNG" style="width: 25%; height: 25%; position: absolute; right: 0;">
  </div>
</div>



[![Maintenance](https://img.shields.io/badge/Status-Maintained-green.svg)]()
[![Linux](https://svgshare.com/i/Zhy.svg)](https://www.linux.org/pages/download/)
[![made-with-cpp](https://img.shields.io/badge/Made%20with-Python-blue)](https://www.python.org/)
[![AGPLv3 license](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)


# Overview

SIEVA is a tool which provides visibility to data ingested by SIEMs, using artificial intelligence, SIEVA analyses the information contained in the logs, classifies such information according to the MITRE ATT&CK framework data sources, and provides a high level view of the ATT&CK Matrix, colour coded to reflect which tactics and techniques can be monitoried with the current information of the system. SIEVA also provides a detailed view of the data analysed on each individual Elasticsearch Index.

This project is currently under development

The current version is a stable MVP which requires adjustment and fine tunning before it can be deployed to a production environemnt

# Pre-requisites

Docker (recommended 20.x or latest)

ElasticSearch 7.x (recommended 7.17.x)


# How to build it

``` bash
cd sieva
docker-compose up -d --build --quiet
```

The application can be accessed in server_ip:9000 and the plots data in server_ip:9001


# How to use

## Once executed

### `/train`

```bash
curl http://server_ip:8081/train?train_pairs={["webserver" : ["webproxy-squid", "webserver-generic", "webserver-nginx"]]}
```

Call this endpoint in order to re-train the model with the existent data. 

**`parameters`** : `train_pairs` -> Dictionary made out of _training-label_ : [_train-index0_, _train-index1_, ...]

**`returns`** : `json` with the path where the model has been saved

```json
    "model path" : "data/model/model.bin"
```


### `/predict`

```bash
curl http://server_ip:8081/predict?predict_idxs=["classification_validate_dataset"]
```

Call this endpoint to perform a prediction with the pre-trained model over the indexes provided as a parameter. 

**`parameters`** : `predict_idxs` -> List made out of [_predict-index0_, _predict-index1_, ...]

**`returns`** : `json` with:

1. The \% of the category split
2. The MITRE techniques to use
3. The path to the predictions file created

```json
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
```




# Source

This code has been developed within the innovation project SIEVA: SIEM visibility assesment.

This project has received funding from the European Union’s GÉANT Innovation Programme 2022 research and innovation programme under grant agreement No SER-22-109. 

More information about the grant at https://community.geant.org/community-programme-portfolio/innovation-programme/

# Copyright

This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT).

i2CAT is a *non-profit research and innovation centre* that  promotes mission-driven knowledge to solve business challenges, co-create solutions with a transformative impact, empower citizens through open and participative digital social innovation with territorial capillarity, and promote pioneering and strategic initiatives.

i2CAT *aims to transfer* research project results to private companies in order to create social and economic impact via the out-licensing of intellectual property and the creation of spin-offs.

Find more information of i2CAT projects and IP rights at https://i2cat.net/tech-transfer/

# License

This code is licensed under the terms *AGPLv3*. Information about the license can be located at [link](https://www.gnu.org/licenses/agpl-3.0.html).

If you find that this license doesn't fit with your requirements regarding the use, distribution or redistribution of our code for your specific work, please, don’t hesitate to contact the intellectual property managers in i2CAT at the following address: techtransfer@i2cat.net
