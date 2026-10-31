# VulnTracker

This repository contains the completed security-hardening work for the take-home assignment. The service is built around a FastAPI application for managing vulnerability results and a lightweight Node.js notification service for webhook dispatch.

## Overview

- Python API: `app/`
- Notification service: `notify/`
- Security reports: `reports/`
- Deployment manifests: `helm/`
- Security docs: `docs/`

## Local setup

### Python API

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

The service listens on `http://localhost:8000` and exposes Swagger docs at `http://localhost:8000/docs`.

### Notification service

```bash
cd notify
npm install
npm start
```

The notifier listens on `http://localhost:3001`.

## Running tests

```bash
pytest tests/ -v
```

## Shared report link feature

The API includes the required secure sharing flow:

- `POST /scans/{scan_id}/share` — creates a share token for a scan, optionally password-protected
- `GET /share/{token}` — returns public scan data if the token is valid and not expired

If a password is supplied during share creation, it must be included as a query parameter on the public read endpoint:

```bash
curl "http://localhost:8000/share/<token>?password=secret"
```

## Docker

```bash
docker build -t vulntracker-api .
docker run --rm -p 8000:8000 --env SECRET_KEY=replace-me --env DATABASE_URL=sqlite:////tmp/vulntracker.db vulntracker-api
```

## Helm deployment

```bash
helm install vulntracker ./helm/vulntracker --namespace vulntracker --create-namespace
```

The chart is set up to consume secrets from a Kubernetes secret or a secret-manager integration and limits ingress to the API service only.
