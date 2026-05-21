from uuid import uuid4

from pod_delivery.models import (
    PartnerPocPlan,
    PartnerPocRequest,
    QualityEvidence,
    QualityGateResult,
    QuoteToFulfillmentRequest,
    OrchestrationResult,
    ToolContract,
)


def create_poc_plan(request: PartnerPocRequest) -> PartnerPocPlan:
    backlog = [
        "Define OpenAPI contract and examples",
        "Implement partner adapter and sandbox config",
        "Add auth scopes and tenant checks",
        "Add retry, timeout, and idempotency policy",
        "Add contract tests and agentic evals",
        "Write runbook and POC-to-production notes",
    ]
    contracts = [f"{flow.value}.contract.yaml" for flow in request.target_flows]
    if request.needs_mcp_tools:
        contracts.append("mcp.tools.json")
    return PartnerPocPlan(
        poc_id=f"poc_{uuid4().hex[:8]}",
        partner_id=request.partner_id,
        backlog=backlog,
        contracts=contracts,
        quality_gate_required=True,
    )


def evaluate_quality_gate(evidence: QualityEvidence) -> QualityGateResult:
    fields = type(evidence).model_fields
    missing = [name for name in fields if not getattr(evidence, name)]
    score = int(((len(fields) - len(missing)) / len(fields)) * 100)
    return QualityGateResult(production_ready=not missing, missing=missing, score=score)


def mcp_contracts() -> list[ToolContract]:
    return [
        ToolContract(
            name="commerce.quote",
            description="Create a non-binding commerce quote.",
            side_effects="none",
            required_scope="tools:invoke",
            input_schema={
                "type": "object",
                "required": ["customer_id", "sku", "quantity", "destination_zip"],
            },
        ),
        ToolContract(
            name="commerce.checkout",
            description="Submit an approved checkout.",
            side_effects="external_payment",
            required_scope="orders:write",
            input_schema={
                "type": "object",
                "required": ["customer_id", "sku", "quantity", "destination_zip", "payment_token"],
            },
        ),
    ]


def quote_to_fulfillment(request: QuoteToFulfillmentRequest) -> OrchestrationResult:
    return OrchestrationResult(
        correlation_id=f"corr_{uuid4().hex[:8]}",
        status="planned",
        steps=[
            "validate customer and tenant authorization",
            "quote price, tax, shipping, and inventory",
            f"reserve {request.quantity} unit(s) of {request.sku}",
            "authorize payment after approval",
            f"create fulfillment order for {request.destination_zip[:5]}",
            "emit order.created event",
        ],
    )
