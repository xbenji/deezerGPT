FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ARG OPENAPI_API_KEY
ENV OPENAPI_API_KEY=$OPENAPI_API_KEY

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.serverAddress=0.0.0.0", "--browser.serverPort=8501", "--server.enableXsrfProtection=false", "--server.enableCORS=false", "--server.enableWebsocketCompression=false"]