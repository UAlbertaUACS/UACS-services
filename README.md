# UACS-services

## Set up Docker

```bash
docker build -t uacs-services:latest .
docker run -d -p 8000:8000 uacs-services:latest
```

Health check:
```bash
curl http://localhost:8000/v1/healthcheck
```

## Set up local environment

```bash
pyenv install 3.10.0
pyenv local 3.10.0
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker set up MongoDB

```bash
docker pull mongo
docker run -d -p 27017:27017 --name mongodb mongo
```

Run the server:
```bash
uvicorn app.main:app --reload
```