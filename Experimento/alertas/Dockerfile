FROM python:3.8

RUN pip install pipenv

ENV PROJECT_DIR /alertas

COPY . /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy

ENV GOOGLE_APPLICATION_CREDENTIALS='./src/config/gcp-key.json'

CMD ["gunicorn", "--graceful-timeout", "5", "src.main:app",  "-w", "4", "-b", "0.0.0.0:3002"]