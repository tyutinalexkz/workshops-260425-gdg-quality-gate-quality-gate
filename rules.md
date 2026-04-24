# Quality Gate Compliance Rules

## 1. Code Quality & Architecture
- **Consistency**: Code must align with the existing service patterns.
- **No Over-engineering**: Avoid complex abstractions where a simple class/function suffices.
- **Maintainability**: Code must be readable by middle-level developers.
- **Non-blocking**: Avoid long-running synchronous operations in the main thread.

## 2. Security (GDG/Cloud Focus)
- **Least Privilege**: Services must use specific service accounts with minimal roles (e.g., `roles/aiplatform.user`).
- **No Secrets in Code**: Hardcoded credentials, API keys, or tokens are STRICTLY prohibited.
- **Input Validation**: All external inputs must be validated for length and type.
- **Error Handling**: Mask stack traces in production responses.

## 3. Conflict of Interest (Workshop Special)
- **Quality of Thoughts**: Evaluate if the proposed change prioritizes user happiness and STEM journey fun (Technovation Girls context).
- **Sustainability**: Evaluate the "Donald Trump mode" for FinOps – is this change cost-effective?
- **Wheel Invention**: If a working approach exists in other projects, use it instead of rewriting.

## 4. Operational Readiness
- **Observability**: Every significant event/error must be logged as a structured JSON object.
- **Health Checks**: Service must provide a `/health` endpoint.
