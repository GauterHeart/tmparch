FROM python:3.11

RUN groupadd -g 1000 app_group \
    && useradd -r -u 1000 -g app_group -m -s /sbin/nologin app_user

RUN mkdir -p /usr/src/app/ && chown -R app_user:app_group /usr/src/app
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - \
    && ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry

COPY --chown=app_user:app_group poetry.lock pyproject.toml /usr/src/app/

COPY --chown=app_user:app_group src /usr/src/app/src
COPY --chown=app_user:app_group /contrib/ /usr/src/app/contrib/
COPY --chown=app_user:app_group /main.py /usr/src/app/
COPY --chown=app_user:app_group /migrate.py /usr/src/app/
COPY --chown=app_user:app_group /yoyo.ini /usr/src/app/
COPY --chown=app_user:app_group /poetry.toml /usr/src/app/


RUN poetry config virtualenvs.create false \
    && poetry install

USER app_user
