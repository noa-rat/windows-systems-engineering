# AI News Application

An asynchronous desktop news application with a FastAPI backend, a PySide6 client, semantic retrieval, and two specialized Ollama models.

## Features

- JWT-based authentication.
- Bcrypt password hashing.
- SQL Server persistence with a bounded connection pool.
- Local client caching with TTL, stale-cache fallback, and request coalescing.
- Background client requests through Qt workers.
- Bounded server executor for blocking database and model integrations.
- Semantic article retrieval using `nomic-embed-text`.
- Answer generation and article summarization using `tinyllama`.
- Explicit news refresh flow.
- Rate limiting, request-size limits, per-user chat quotas, and circuit breakers.
- Pydantic models at API boundaries and for client response models.
- Configurable HTTPS enforcement for production deployments.

## Architecture

```text
PySide6 Client
    |
    | HTTP(S) + JWT Bearer token
    v
FastAPI Server
    |
    +--> Authentication and authorization
    +--> Pydantic request/response validation
    +--> Bounded worker executor
    +--> SQL Server connection pool
    +--> NewsAPI gateway
    +--> Ollama gateway
              |
              +--> nomic-embed-text: embeddings and retrieval
              +--> tinyllama: answers and summaries
```

## AI and Semantic RAG Flow

```text
User question
    -> Validate prompt length
    -> Check JWT and per-user quota
    -> Use selected article context, or:
       -> Read article summaries from SQL Server
       -> Generate embeddings with nomic-embed-text
       -> Normalize vectors and rank by similarity
    -> Limit context size
    -> Add untrusted-context instruction
    -> Generate answer with tinyllama
    -> Return typed response
```

The embedding model is used only for retrieval. The generation model is used only for summaries and answers.

## Security

- Passwords are stored as bcrypt hashes, never as plaintext.
- JWT access tokens are signed with `JWT_SECRET` and have an expiration time.
- Protected routes require a Bearer token.
- Users can access only their own preferences.
- SQL queries use parameterized statements.
- Secrets are loaded from `.env` and are excluded from Git.
- CORS allows only configured origins.
- Request bodies are size-limited.
- Chat prompts and article context have maximum lengths.
- Chat requests have a per-user quota.
- Circuit breakers prevent repeated calls to unavailable external services.
- Production deployments can enforce HTTPS with `FORCE_HTTPS=true`.

JWT provides authentication and integrity. It does not encrypt network traffic. HTTPS is required for transport encryption.

## Load Protection and Resilience

The application uses multiple independent protections:

| Layer | Protection |
|---|---|
| Client | Background workers, timeouts, cache, stale fallback, request coalescing |
| HTTP client | Thread-local connection pool and safe GET retries |
| FastAPI | Async routes, bounded executor, request-size limit |
| Rate control | Per-client request rate limit and per-user chat quota |
| Database | Bounded SQL connection pool, health checks, pool exhaustion handling |
| External services | Timeouts, typed response validation, circuit breakers |
| Ollama | Prompt/context limits and output token limit |

Failures are returned as explicit errors such as `401`, `409`, `413`, `429`, or `503` instead of silently returning success-shaped responses.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/login` | Authenticate and issue a JWT |
| POST | `/auth/register` | Create a user |
| GET | `/auth/preferences` | Read the current user's preferences |
| POST | `/auth/preferences` | Update the current user's preferences |
| GET | `/news` | Read stored news |
| POST | `/news/refresh` | Fetch, summarize, store, and return news |
| GET | `/news/search` | Search stored news |
| POST | `/ask-ai` | Ask the AI with article or semantic context |
| GET | `/graphs/by-category` | Return category statistics |

All endpoints except login, registration, and the health root require JWT authentication.

## Local Development

### Requirements

- Windows 10 or later.
- Python 3.11 or later.
- ODBC Driver 18 for SQL Server.
- A reachable SQL Server database.
- Ollama.
- The following Ollama models:

```text
tinyllama
nomic-embed-text
```

### Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the repository root:

```env
NEWS_API_KEY=replace-with-newsapi-key
SOMEE_DB_PASSWORD=replace-with-database-password
JWT_SECRET=replace-with-a-long-random-secret

OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_GENERATION_MODEL=tinyllama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

ALLOWED_ORIGINS=http://localhost:8000
FORCE_HTTPS=false

AI_API_BASE_URL=http://localhost:8000
AI_API_VERIFY_TLS=true
```

Do not commit `.env`. Use a long, random value for `JWT_SECRET`.

### Start Ollama

Make sure the Ollama service is running and verify the models:

```powershell
ollama list
```

Install missing models:

```powershell
ollama pull tinyllama
ollama pull nomic-embed-text
```

### Start the Backend

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start the Client

In a second terminal:

```powershell
.\.venv\Scripts\python.exe -m client.main
```

Local development uses HTTP on `localhost`. This is intentional for local execution only.

## Production Deployment

Run the application behind a TLS-enabled reverse proxy such as IIS, Nginx, or a cloud load balancer.

Recommended production settings:

```env
FORCE_HTTPS=true
AI_API_BASE_URL=https://api.example.com
AI_API_VERIFY_TLS=true
ALLOWED_ORIGINS=https://app.example.com
```

The reverse proxy should:

1. Terminate TLS.
2. Forward requests to Uvicorn over a private network.
3. Enforce request and connection limits.
4. Provide access logs and health monitoring.
5. Run multiple Uvicorn workers only when the database pool and Ollama capacity support it.

The in-process rate limiter and caches are instance-local. For a multi-instance deployment, use shared infrastructure such as Redis for distributed rate limiting and cache coordination.

## Operational Notes

- The client cache is memory-only and is cleared when the application exits.
- Database pooling is separate from HTTP connection pooling.
- Ollama is local by default and can become the primary latency bottleneck.
- Embedding indexes are rebuilt when stored article signatures change.
- A load test should be performed before production deployment with concurrent login, news, graph, and chat requests.
- Logs must never include passwords, JWTs, or full user prompts containing sensitive information.

## Validation

Compile the application:

```powershell
.\.venv\Scripts\python.exe -m compileall -q backend client
```

Check repository whitespace:

```powershell
git diff --check
```
