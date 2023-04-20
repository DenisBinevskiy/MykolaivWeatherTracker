FROM python:latest
WORKDIR /python

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./MWT.py" ]