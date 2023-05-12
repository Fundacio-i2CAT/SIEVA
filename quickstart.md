
# SIEVA: SIEM Visibility Assessment

## Quickstart

Install requirements file:

``` bash
pip3 install -r requirements.txt
```

The following commands allow to run the API locally. Once it has started, you can open your browser to http://127.0.0.1:8081/

``` bash
cd SIEVA/
pip install -r requirements.txt
uvicorn AI_Engine.ngine.main:app --reload --port 8081 --reload
```

Otherwise with `docker`:

``` bash
cd sieva
docker compose up -d --build --quiet
```

Then, the matrix is found in 127.0.0.1:9000 and the plots data in 127.0.0.1:9001

Afterwards, requests can be done to 3 different endpoints:

## Once executed

### `/train`

```bash
curl http://127.0.0.1:8081/train?train_pairs={["webserver" : ["webproxy-squid", "webserver-generic", "webserver-nginx"]]}
```

Call this endpoint in order to re-train the model with the existent data. The data that will be used is found in an `elasticsearch` database which, so far, requires to be connected to the i2Cat FortiNet VPN to retrieve data from it.

**`parameters`** : `train_pairs` -> Dictionary made out of _training-label_ : [_train-index0_, _train-index1_, ...]

**`returns`** : `json` with the path where the model has been saved

```json
    "model path" : "data/model/model.bin"
```


### `/predict`

```bash
curl http://127.0.0.1:8081/predict?predict_idxs=["classification_validate_dataset"]
```

Call this endpoint to perform a prediction with the pre-trained model over the indexes provided as a parameter. Again, if the datasets are stored in the `elasticsearch` database, a connection through the VPN is required.

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

### `/assert_completeness`

```bash
curl http://127.0.0.1:8081/assert_completeness?predict_idxs=["classification_validate_dataset"]
```

Call this endpoint in order to assert the completeness (identify the entities on a set of logs) of a provided dataset as a paramater. Again, if the datasets are stored in the `elasticsearch` database, a connection through the VPN is required.

**`parameters`** : `predict_idxs` -> List made out of [_predict-index0_, _predict-index1_, ...]

**`returns`** : `json` with the entities that make each one of the logs.


## Documentation

A full `sphinx` built documentation is provided.

```bash
cd docs 
make html 
firefox _build/index.html &
```
