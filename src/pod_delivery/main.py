from fastapi import FastAPI

from pod_delivery.models import (
    OrchestrationResult,
    PartnerPocPlan,
    PartnerPocRequest,
    QualityEvidence,
    QualityGateResult,
    QuoteToFulfillmentRequest,
    ToolContract,
)
from pod_delivery.service import create_poc_plan, evaluate_quality_gate, mcp_contracts, quote_to_fulfillment

app = FastAPI(title="Agentic Commerce Delivery Pod Lab", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/pocs", response_model=PartnerPocPlan)
def create_poc(request: PartnerPocRequest) -> PartnerPocPlan:
    return create_poc_plan(request)


@app.post("/v1/pocs/{poc_id}/quality-gate", response_model=QualityGateResult)
def quality_gate(poc_id: str, evidence: QualityEvidence) -> QualityGateResult:
    return evaluate_quality_gate(evidence)


@app.get("/v1/mcp/contracts", response_model=list[ToolContract])
def contracts() -> list[ToolContract]:
    return mcp_contracts()


@app.post("/v1/orchestrations/quote-to-fulfillment", response_model=OrchestrationResult)
def orchestrate(request: QuoteToFulfillmentRequest) -> OrchestrationResult:
    return quote_to_fulfillment(request)

