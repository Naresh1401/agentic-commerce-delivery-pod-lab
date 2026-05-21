from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Flow(StrEnum):
    catalog = "catalog"
    quote = "quote"
    checkout = "checkout"
    fulfillment = "fulfillment"
    post_purchase = "post_purchase"


class PartnerPocRequest(BaseModel):
    partner_id: str
    target_flows: list[Flow] = Field(min_length=1)
    auth_pattern: str = Field(pattern="^(oauth_client_credentials|api_key|mtls)$")
    needs_mcp_tools: bool = True


class PartnerPocPlan(BaseModel):
    poc_id: str
    partner_id: str
    backlog: list[str]
    contracts: list[str]
    quality_gate_required: bool


class QualityEvidence(BaseModel):
    auth_tests: bool = False
    contract_tests: bool = False
    mcp_tool_tests: bool = False
    idempotency_tests: bool = False
    observability_plan: bool = False
    runbook: bool = False
    agentic_eval_cases: bool = False


class QualityGateResult(BaseModel):
    production_ready: bool
    missing: list[str]
    score: int


class ToolContract(BaseModel):
    name: str
    description: str
    side_effects: str
    required_scope: str
    input_schema: dict[str, Any]


class QuoteToFulfillmentRequest(BaseModel):
    customer_id: str
    sku: str
    quantity: int = Field(gt=0)
    destination_zip: str


class OrchestrationResult(BaseModel):
    steps: list[str]
    status: str
    correlation_id: str

