FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

CMD gunicorn app:app --workers 4 --timeout 600 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000