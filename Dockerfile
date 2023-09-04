FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Views /usr/src/app/

EXPOSE 8080

CMD [ "python", "./App.py" ]
