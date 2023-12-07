FROM python:3.10

WORKDIR /app

COPY . /app/

EXPOSE 8000
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]

ENV DJANGO_SETTINGS_MODULE=drop_app.settings
ENV PYTHONPATH=/app

RUN pip install -r requirements.txt
RUN chmod +x /app/docker-entrypoint.sh

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
