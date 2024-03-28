FROM python:3.8

RUN pip install pipenv

ENV PROJECT_DIR /administracion

COPY administracion /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy

CMD ["gunicorn", "--graceful-timeout", "5", "src.main:app",  "-w", "4", "-b", "0.0.0.0:5002"]