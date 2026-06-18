# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Masrobo RCS SDK — a multi-language SDK for the Masrobo RCS (Robot Control System) RESTful Open API (`https://api.boticz.cn/open`). The Go SDK lives in a separate repository at `d:\work2026\rcs-golang-sdk`.

Any change to one language SDK must be mirrored across all other language SDKs.

## Build & Test Commands

### Python (`python/`)

```bash
# Install dev dependencies
pip install -r python/requirements.txt

# Run tests (integration tests against live API; needs .env with credentials)
cd python && pytest tests/ -v

# Build distribution (wheel + sdist → python/dist/)
cd python && python -m build
```

### Node.js (`nodejs/`)

```bash
cd nodejs
npm install
npm test          # vitest run (integration tests against live API; needs .env)
npm run build     # vite build → dist/ (ESM + CJS + .d.ts)
```

### Java (`java/`)

```bash
# Run tests
bash java/scripts/mvn-test.sh
# Equivalent to: cd java && mvn test -Dsurefire.useFile=false

# Build JAR
cd java && mvn clean package -DskipTests

# Maven settings.xml is at D:\.m2\settings.xml
```

### Go (`d:\work2026\rcs-golang-sdk`)

```bash
cd d:\work2026\rcs-golang-sdk
go test ./tests/ -v    # integration tests (needs config.yaml with credentials)
go build ./...
```

## Architecture

### Authentication Flow (all SDKs)

1. `Config` is initialized with `app_id`, `app_key`, and `base_url`
2. Before each request, a JWT token is generated with claims `{app_id, app_key, iat, exp=iat+3600}` signed with HMAC-SHA256 using `app_key` as the secret
3. The token is sent in the `X-Token` HTTP header

### API Response Envelope

All API responses follow `{code: int, msg: string, data: ...}`. Success = HTTP status < 400 AND envelope `code == 200`. All SDKs define a custom `APIError`/`ApiException` type with `statusCode`, `code`, `message`, and `rawBody` fields.

### Layered Architecture (consistent across all four SDKs)

```
RobotController         — top-level entry point; owns Config, Client, IotDeviceService
├── Config              — URL normalization, credential validation, JWT generation
├── Client              — HTTP layer: X-Token injection, JSON serialization, error envelope parsing
└── IotDeviceService    — business logic for IoT device APIs (5 endpoints)
    ├── getLatestDeviceData   GET  /iot/device/data
    ├── sendDeviceCommand     POST /iot/device/command
    ├── bindDevice            POST /iot/device/bind
    ├── setting               POST /iot/device/setting
    └── getDeviceInfo         POST /iot/device/info
```

Shared utility modules across SDKs: `base` (success code constant, decode helper), `validator` (null/empty checks), `request` (request types, topic constants), `response` (response types).

### Topic Constants

- `TopicDeviceData` / `DEVICE_DATA` = `"device_data"`
- `TopicScreenshot` / `SCREENSHOT` = `"screenshot"`
- `TopicRemoteControl` / `REMOTE_CONTROL` = `"remote_control"`

### Key Differences Between SDKs

| Aspect | Python | Node.js | Java | Go |
|--------|--------|---------|------|-----|
| HTTP client | `requests` | `axios` | `java.net.http.HttpClient` | `net/http` |
| JWT library | `PyJWT` | `jsonwebtoken` | `jjwt` (0.12.x) | `golang-jwt/jwt/v5` |
| JSON | `dataclasses` + dict | TypeScript interfaces | Jackson `ObjectMapper` | `encoding/json` + struct tags |
| Validation | manual `require_value()` | manual `requireValue()` | `RequestValidator` helper | `go-playground/validator/v10` struct tags |
| Config source | `.env` (python-dotenv) | `.env` (Vite env vars) | `.env` (dotenv-java) | `config.yaml` |
| Error type | `APIError(Exception)` | `APIError(Error)` | `ApiException(RuntimeException)` | `APIError` (implements `error`) |

## Tests

All tests are **integration tests** that hit the live API at `api.boticz.cn`. They require valid credentials:

- Python/Node.js/Java: `.env` file with `APP_ID`, `APP_KEY`, `DEVICE_ID`, `PRODUCT_NAME` (variables prefixed with `VITE_` for Node.js)
- Go: `config.yaml` at repo root with `base_url`, `app_id`, `app_key`, `device_id`, `product_name`

When adding a new test in one language, reference the Python test (`python/tests/test_device_info.py`) as the canonical pattern and mirror it in other languages.

## Release Process

Per `.clinerules/project_rules.md` (manual release, do not use CI/CD):

1. Update the `VERSION` file at repo root, then update version in each SDK's build config
2. Ensure local code is in sync with remote
3. Push Go SDK to `https://github.com/masrobo/rcs-golang-sdk`
4. Publish each SDK manually:
   - Python: `twine upload python/dist/*`
   - Node.js: `cd nodejs && npm publish`
   - Java: `cd java && mvn clean deploy -DskipTests -s settings.xml`
   - Go: push tag to GitHub
