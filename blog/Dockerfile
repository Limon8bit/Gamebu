FROM python:latest

WORKDIR /django_app

COPY . .

RUN pip install -r requirements.txt
# RUN chmod +x entrypoint.sh

ENTRYPOINT ["/django_app/entrypoint.sh"]