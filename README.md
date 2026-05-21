# Agentic Commerce Delivery Pod Lab

Portfolio repo for the full responsibilities section of the JD.

This repo is a small "pod operating system" for rapidly delivering partner-ready agentic commerce integrations:

- API-first lifecycle templates
- Secure REST API implementation
- Orchestration/composition flows
- MCP tool contracts
- Partner POC onboarding
- POC-to-production quality gates
- Agentic variability testing strategy
- Pod collaboration artifacts

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn pod_delivery.main:app --reload --app-dir src
```

## Endpoints

- `POST /v1/pocs`
- `POST /v1/pocs/{poc_id}/quality-gate`
- `GET /v1/mcp/contracts`
- `POST /v1/orchestrations/quote-to-fulfillment`

