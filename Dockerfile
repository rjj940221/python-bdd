FROM python:3.10.2-alpine

WORKDIR /usr/bdd

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY features ./features
COPY src ./src


CMD [ "behave", "--junit" ]