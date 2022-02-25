FROM python:3.8-slim

RUN pip3 install poetry

WORKDIR /dask

COPY . /dask

RUN poetry install --no-dev
RUN mv settings.toml.example settings.toml

EXPOSE 5000

ENTRYPOINT ["poetry","run", "python","run.py"]
