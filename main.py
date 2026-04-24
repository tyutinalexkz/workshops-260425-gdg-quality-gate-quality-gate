"""Main entry point for the Quality Gate service."""

import json
import logging
from contextlib import asynccontextmanager
from typing import List

import vertexai
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from vertexai.generative_models import GenerativeModel, GenerationConfig

from config import settings

# Setup structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(settings.SERVICE_NAME)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize Vertex AI once at startup."""
    try:
        vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.LOCATION)
        logger.info(
            {"event": "vertex_init_success", "project": settings.GCP_PROJECT_ID}
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error({"event": "vertex_init_failed", "error": str(e)})
    yield


app = FastAPI(title="Quality Gate Demo", lifespan=lifespan)

# --- Schemas ---


class ReviewRequest(BaseModel):
    """Request model for the review endpoint."""

    content: str = Field(
        ..., max_length=100000
    )  # 100k chars for repo scanning/large diffs


class ReviewReport(BaseModel):
    """Schema for the structured AI review report."""

    summary: str = Field(description="Short summary of the review")
    pass_gate: bool = Field(description="Whether the content passes the gate")
    findings: List[str] = Field(description="List of critical findings or violations")
    recommendations: List[str] = Field(
        description="Actionable recommendations for improvement"
    )


# --- Error Handlers ---


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global generic exception handler to mask stack traces."""
    logger.error(
        {"event": "unhandled_error", "error": str(exc), "path": request.url.path}
    )
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )


# --- Endpoints ---


@app.post("/v1/review", response_model=ReviewReport)
async def review(req: ReviewRequest):
    """Evaluates content against rules using Vertex AI."""
    model = GenerativeModel(settings.MODEL_ID)

    prompt = (
        f"<content>\n{req.content}\n</content>\n"
        f"<rules>\n{settings.rules}\n</rules>\n"
        "Review the content against the rules and provide a structured JSON report."
    )

    try:
        # Manual schema to avoid Pydantic v2 / Vertex SDK compatibility issues
        response_schema = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "pass_gate": {"type": "boolean"},
                "findings": {"type": "array", "items": {"type": "string"}},
                "recommendations": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["summary", "pass_gate", "findings", "recommendations"],
        }

        response = model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.2,
            ),
        )

        report_data = json.loads(response.text)
        logger.info(
            {
                "event": "review_complete",
                "pass_gate": report_data.get("pass_gate"),
                "findings_count": len(report_data.get("findings", [])),
            }
        )

        return ReviewReport(**report_data)

    except json.JSONDecodeError as e:
        logger.error({"event": "ai_json_parse_failed", "error": str(e)})
        return JSONResponse(
            status_code=500, content={"message": "Failed to parse AI response."}
        )
    except Exception as e:
        logger.error({"event": "review_failed", "error": str(e)})
        raise e


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": settings.SERVICE_NAME}
