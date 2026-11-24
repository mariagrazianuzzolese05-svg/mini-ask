# mini-ask

[![CI](https://github.com/mariagrazianuzzolese05-svg/mini-ask/actions/workflows/ci.yaml/badge.svg)](https://github.com/mariagrazianuzzolese05-svg/mini-ask/actions/workflows/ci.yaml)

A small example API built with FastAPI to learn the full path to production: tests, CI, Docker, deploy and monitoring.
The answers are fake on purpose: the focus is on how the service is built, tested and deployed, not on the model.

**Live:** https://mini-ask.onrender.com (Render Free: the first request after 15 minutes of inactivity can take up to a minute).

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/healthz` | health check, returns `{"status": "ok"}` |
| POST | `/ask` | takes `{"testo": "..."}` (1-500 characters) and returns a fake answer. Needs the `X-API-Key` header |
| GET | `/docs` | interactive OpenAPI documentation (`/` redirects here) |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
API_KEY=prova123 uvicorn app.main:app --reload
```

With Docker:

```bash
docker build -t mini-ask .
docker run -p 8000:8000 -e API_KEY=prova123 mini-ask
```

## Quality checks

```bash
ruff check . && ruff format --check . && mypy --strict app tests && pytest -q
```

- **pytest**: unit tests for the endpoints, the API key and the input limits (0, 1, 500, 501 characters).
- **Schemathesis**: tests generated from the OpenAPI schema. It found two undocumented status codes (400 and 401), now declared in the contract.
- **mutmut** (mutation testing) on the API key check: the first run killed 10 of 15 mutants (67%), because the tests checked only the status code and not the error message. After adding that check: 15 of 15 (100%). Run with `rm -rf mutants && mutmut run`.
- **ruff** and **mypy --strict**: linting, formatting and static type checks.

## CI/CD and monitoring

- **CI** (GitHub Actions, `ci.yaml`): runs all the checks above on every push and pull request.
- **CD** (Render): deploys automatically only after the CI is green.
- **Monitoring** (`health.yaml`): a daily scheduled workflow calls `/healthz` and fails if the service does not answer.
- **Secrets**: `API_KEY` lives only in Render's environment variables, never in the code.

## Decisions

- [ADR 001: where to deploy](docs/decisions/001-dove-pubblicare.md): why Render Free and not Railway or AWS.

## License

MIT
