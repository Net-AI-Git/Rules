## Mandate

All ASGI applications (FastAPI) in the project **MUST** be run with **Uvicorn**. Do not run with another ASGI server or with `python main.py` as the server process.

## Installation

* **Required:** Install Uvicorn with the `[standard]` extra so that optional performance and reload dependencies are available:
    * **Poetry:** `poetry add "uvicorn[standard]"`
    * **pip:** `pip install 'uvicorn[standard]'`
* **Included by `[standard]`:**
    * **uvloop** — Fast event loop; used by Uvicorn when installed.
    * **httptools** — Fast HTTP parsing; used by Uvicorn when installed.
    * **watchfiles** — File watching for `--reload`; required for reliable reload in development.
* **Dependency declaration:** Ensure `pyproject.toml` (or `requirements.txt`) includes `uvicorn[standard]`, not plain `uvicorn`, so that all environments get the same behavior.

## Default Run Commands

Only two Uvicorn options are standardized as defaults: `--reload` and `--workers`.

### Development

* **Command:** Run with `--reload`. Do **not** use `--workers` in development.
* **Example:**

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

* **Rule:** `--reload` is the default for local development. Never use `--reload` in production.

### Production

* **Command:** Run with `--workers <N>`. Do **not** use `--reload` in production.
* **Example:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

* **Rule:** `--workers` is required in production; set N per environment (e.g., by CPU cores or load). Omit `--reload`.

## Summary

| Environment  | Required options   | Forbidden options |
|-------------|--------------------|-------------------|
| Development | `--reload`         | `--workers`       |
| Production  | `--workers <N>`    | `--reload`        |

Other Uvicorn options (e.g. SSL, proxy headers, limit-concurrency) are not mandated by this rule; use them when needed for a specific deployment.

See rule: api-interface-and-streaming (in .amazonq/rules) for FastAPI and streaming; rule: deployment-and-infrastructure (in .amazonq/rules) for Docker and production deployment.
