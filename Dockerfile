FROM python:3.12-slim

WORKDIR /app

RUN set -eux && \
    apt-get update &&  \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        dos2unix \
        libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
  groupadd \
          --system \
       receive-t1 && \
      useradd \
          --system \
      receive-t1 \
          -g \
      receive-t1

COPY ./requirements.txt ./requirements.txt

RUN set -eux && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=receive-t1:receive-t1 app ./
COPY --chown=receive-t1:receive-t1 ./tests ./tests
COPY ./commands /commands

RUN dos2unix /commands/*.sh && \
    chmod +x /commands/*.sh

USER receive-t1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]