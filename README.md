# Quality Gate Demo Workshop 🚀

Automated compliance and quality evaluation for code, architecture, and decisions using Vertex AI.

## Getting Started

### 1. Prerequisites
- A Google Cloud Project with billing enabled.
- [gcloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- Docker installed (only if you plan to build your own image).

### 2. Configuration
Copy the template `.env.example` to `.env` and fill in your project details:

```bash
cp .env.example .env
# Edit .env and set GCP_PROJECT_ID=your-project-id
```

### 3. Deployment

#### 🚀 Option A: Zero-Build (Recommended for Attendees)
Deploy instantly using the pre-built public image:
```bash
bash scripts/deploy.sh
```

#### 🏗️ Option B: Build & Push (For Workshop Owners)
Build your own image locally, push to Docker Hub, and deploy:
```bash
# 1. Build and push your image
bash scripts/build.sh

# 2. Deploy your custom image
bash scripts/deploy.sh --custom
```

## Testing the Gate

Once deployed, you can test the service using `curl`:

```bash
URL="https://your-service-url.a.run.app"

curl -X POST "${URL}/v1/review" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Add hardcoded API key for debugging purposes."
  }'
```

The service will respond with a structured JSON report:
```json
{
  "summary": "Fail. Security violation detected.",
  "pass_gate": false,
  "findings": [
    "Hardcoded API key detected in the code changes."
  ],
  "recommendations": [
    "Use Secret Manager to store and retrieve API keys.",
    "Remove credentials from source code immediately."
  ]
}
```

## Code Quality

To maintain a 10/10 pylint score and ensure consistent formatting, run the linter script:

```bash
bash scripts/run-linters.sh
```

## Security & Operations

- **Least Privilege**: The service uses a Cloud Run service account with only `roles/aiplatform.user`.
- **Structured Logging**: All requests and evaluations are logged in JSON format for easy analysis in Cloud Logging.
- **Observability**: Generic error handler masks internal details and stack traces.

## Tech Debt & Improvements
- **Auth**: Currently deployed with `--allow-unauthenticated` for workshop convenience. Production usage should be gated behind IAP or API Keys.
- **Scrubbing**: No automatic PII scrubbing is implemented in this demo; use test data only.
