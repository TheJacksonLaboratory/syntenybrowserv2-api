FROM python:3.7-slim

LABEL org.jax.project="JAX Synteny Browser"
LABEL org.opencontainers.image.authors="synbrowser-support@jax.org"
LABEL org.opencontainers.image.source="https://github.com/TheJacksonLaboratory/syntenybrowserv2-api.git"
LABEL org.opencontainers.image.version="0.0.1"

ENV PYTHONUNBUFFERED 1
ENV PORT 8000
ENV APP_HOME /opt/sb
RUN mkdir -p $APP_HOME

COPY . $APP_HOME
WORKDIR $APP_HOME
EXPOSE $PORT

ENTRYPOINT ["./deploy/entrypoint.sh"]

RUN pip install --upgrade pip && pip install -r requirements.txt
CMD gunicorn --workers=2 --threads=4 -b :$PORT wsgi:app