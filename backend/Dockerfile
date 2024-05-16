FROM python:3.9

WORKDIR /app

COPY ../requirements.txt .
RUN pip install -r requirements.txt
RUN pip install eventlet gunicorn

COPY app/ .

CMD ["gunicorn", "--worker-class", "eventlet", "--bind", "0.0.0.0:5000", "app:app"]
