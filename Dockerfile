FROM python:3

#make a dir for the app
WORKDIR /usr/src/app
#install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
#copy source code
COPY . /
CMD ["python", "app.py"]