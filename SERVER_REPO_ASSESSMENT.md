# Server9 Repository Assessment (Updated)

Last updated: 2026-04-13 (UTC)

This updated assessment is focused on one goal: help you quickly identify the real runtime path so you can modify the server safely without touching the wrong project.

---

## 1) Executive summary

Your repository is a **multi-project dump** from a Docker host, not a single coherent application.

- It contains at least 4 runnable app stacks (`logistics_stack`, `apifirst`, `shipping_app_docker`, `laravel-dual-stack`) plus scaffolds/prototypes.
- There are **plaintext secrets and credentials** committed in compose files.
- There is significant repository bloat from committed dependencies (`vendor/`) and binary upload data.

If you want clean, reliable changes: first select one primary stack, then archive the rest.

---

## 2) What is in this repo (practical inventory)

### Likely runnable stacks

| Folder | Type | Likely role |
|---|---|---|
| `logistics_stack/` | Docker Compose multi-service | Fleetbase + Karrio + gateway orchestration |
| `apifirst/` | FastAPI + MySQL | Custom logistics API with auth/shipments/tracking |
| `shipping_app_docker/` | Laravel + Docker | PHP app with full dependency tree committed |
| `laravel-dual-stack/` | Docker Compose | 2 Laravel apps sharing one MySQL |

### Likely secondary/prototype folders

- `api-first-example/` (reference demo project)
- `shipping_app/` (minimal Laravel shipping app)
- `laravel-backAPI/` (compose present, but app source appears mostly empty)
- `shipment/`, `shipment-lite/`, `microservices-platform/`, `karrio/`, `fleetbase-stack/`, `laravel-api-boilerplate/` (mostly placeholders right now)

---

## 3) Runtime map you can use immediately

### `apifirst/` runtime signals
- FastAPI app includes routers at `/v1` for `auth`, `carriers`, `shipments`, `tracking`.
- Compose exposes host port `8009` -> container `8000`.
- MySQL runs in same compose file.

### `logistics_stack/` runtime signals
- Fleetbase API exposed at host `8010`.
- Fleetbase console exposed at host `4200`.
- Karrio API exposed at host `5005`.
- Karrio dashboard exposed at host `3005`.
- Gateway exposed at host `8011` and proxies Fleetbase/Karrio and route optimization.

### `laravel-dual-stack/` runtime signals
- Two nginx frontends exposed on `8181` and `8182`.
- Shared MySQL exposed on `3308`.

---

## 4) High-priority risks (with impact)

### A) Secrets committed in Git (critical)
Impact: credential leakage, third-party API abuse, production compromise.

Examples currently present include:
- API tokens in `apifirst/docker-compose.yml`
- app keys/passwords in `logistics_stack/docker-compose.yml`

### B) Hardcoded host/IP assumptions
Impact: brittle deployment and failed migrations between environments.

Examples:
- `192.168.1.9` values hardcoded in logistics stack env vars.

### C) Committed dependency trees and runtime artifacts
Impact: huge diffs, slower Git operations, noisy reviews, accidental leakage.

Observed:
- `shipping_app_docker/shipping-app/vendor` contains thousands of files.
- `data/shipment-docs/` includes binary documents/images.

---

## 5) Evidence snapshot (quick metrics)

- `shipping_app_docker/` is ~32MB in this repo (largest top-level directory).
- `data/` is ~1.3MB with document/image uploads.
- `shipping_app_docker/shipping-app/vendor` currently tracks ~4,845 files.
- `data/shipment-docs` currently tracks 8 files.

These are strong indicators this repository includes runtime/dev machine state, not just source code.

---

## 6) How to determine the true "active" stack in 10 minutes

Run on your Docker host (or where this was exported from):

1. List running containers and compose projects.
2. Map host ports to containers.
3. Hit `/health` or known endpoints.
4. Match responses to folder/service signatures above.

Interpretation:
- If you see ports `8010/4200/5005/3005/8011`, your primary is likely `logistics_stack`.
- If you see `8009` and `/v1/*` endpoints, your primary is likely `apifirst`.
- If you see `8181/8182`, your primary is likely `laravel-dual-stack`.

---

## 7) Recommended consolidation strategy

### Step 1 (now): declare one source of truth
Pick **one** primary stack folder and mark all others as `archive/` (or move to separate repos).

### Step 2: remove sensitive and generated content from Git tracking
- move secrets to `.env`
- add/strengthen `.gitignore`
- stop tracking vendor/build/runtime upload paths

### Step 3: add root-level operator docs
Create:
- `README.md` (golden start command)
- `docs/architecture.md` (services + ports + dependencies)
- `docs/runbook.md` (deploy, rollback, rotate secrets)

### Step 4: enforce safe change process
Before feature edits, require:
- one smoke test for health
- one API contract test
- one DB connectivity check

---

## 8) Modification playbook (what you should do next)

If your business is centered on integrated logistics platforms and dashboards:
- keep `logistics_stack` as primary.

If your business is centered on custom Python API development:
- keep `apifirst` as primary.

Then:
1. Freeze non-primary folders (read-only/archive).
2. Rotate all exposed secrets.
3. Add environment templating.
4. Implement CI checks only for the primary stack.

This gives you a stable base where every change is intentional and traceable.
