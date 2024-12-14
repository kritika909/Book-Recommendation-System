FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y python3-distutils python3-pip

COPY requirements.txt .


RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python" , "manage.py" , "runserver" , "0.0.0.0:8000"]