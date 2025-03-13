# pull official base image
FROM python:3.13.2-slim-bullseye AS python-base


ENV APP_HOME=/home/python_user

# ENV APP_USER=python_user
# RUN adduser --disabled-password --gecos "" $APP_USER && chown -R $APP_USER:$APP_USER $APP_HOME
# RUN usermod -aG sudo $APP_USER
# USER $APP_USER

WORKDIR $APP_HOME

ENV TZ 'Asia/Tehran'
RUN echo $TZ > /etc/timezone && apt-get update && \
    apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.8.4
ENV POETRY_HOME=$APP_HOME/poetry
ENV POETRY_VENV=$APP_HOME/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_C8000ACHE_DIR=$APP_HOME/.poetry-cache

# Upgrade pip
RUN pip install --upgrade pip

# Create a new stage from the base python image
FROM python-base AS poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV 
RUN $POETRY_VENV/bin/pip install -U pip setuptools 
RUN $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base AS example-app-base

# Copy Poetry to django_core image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# copy dependency
COPY ./pyproject.toml ./README.md $APP_HOME

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache

FROM example-app-base AS example-app-final

COPY django_config/ $APP_HOME/django_config/
COPY manage.py $APP_HOME/manage.py

EXPOSE 8000