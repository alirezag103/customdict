FROM python:3.10-alpine

# Configure poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/usr/local/bin
ENV POETRY_VENV=opt/poetry-venv
ENV POETRY_CACHE_DIR=opt/.cache
ENV POETRY_VIRTUALENVS_IN_PROJECT=true


EXPOSE 8000

WORKDIR /app 

RUN pip --default-timeout=100 install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
# ENV PATH="${PATH}:${POETRY_VENV}/bin"
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
COPY pyproject.toml /app
COPY poetry.lock /app
RUN poetry env use python3
RUN . /app/.venv/bin/activate && poetry install

# Copy the app
COPY customdict /app/customdict
COPY dictionary /app/dictionary
COPY manage.py /app
COPY LICENSE /app
COPY README.md /app

# Setting the database
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@docker.net', 'password')" | python3 manage.py shell

CMD ["python3", "/app/manage.py", "runserver", "0.0.0.0:8000"]