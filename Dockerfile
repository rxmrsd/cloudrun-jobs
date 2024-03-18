#####################################
FROM python:3.11.7-slim as base

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false

WORKDIR /workspace

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry export --without-hashes --output requirements.txt

#####################################
FROM python:3.11.7-slim

ENV PYTHONUNBUFFERED true
ENV PYTHONPATH /workspace/src/:$PYTHONPATH

WORKDIR /workspace

RUN pip install --no-cache-dir --upgrade pip
COPY --from=base /workspace/requirements.txt ./
COPY ./src/ src/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]