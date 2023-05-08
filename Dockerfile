
#FROM python:3.10.6
#WORKDIR /code
#COPY ./requeriments.txt ./requeriments.txt
#RUN pip install -r requeriments.txt
#EXPOSE 8081
#COPY . /code/src
#CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]
#RUN mkdir /code/logs
#RUN mkdir /code/data/predictions



 
 
FROM python:3.9

WORKDIR /code
 
COPY ./requeriments.txt /code/requeriments.txt

RUN pip install --no-cache-dir --upgrade -r /code/requeriments.txt

COPY . /code
# COPY ./production_src /code/production_src
CMD ["uvicorn", "AI_Engine.main:app", "--host", "0.0.0.0", "--port", "8081"]

