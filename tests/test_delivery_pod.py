from fastapi.testclient import TestClient

from pod_delivery.main import app
from pod_delivery.models import QualityEvidence
from pod_delivery.service import evaluate_quality_gate

client = TestClient(app)


def test_create_poc_plan_includes_contracts_and_mcp_tools() -> None:
    response = client.post(
        "/v1/pocs",
        json={
            "partner_id": "partner_google_ucp",
            "target_flows": ["catalog", "quote", "checkout"],
            "auth_pattern": "oauth_client_credentials",
            "needs_mcp_tools": True,
        },
    )
    body = response.json()
    assert response.status_code == 200
    assert "mcp.tools.json" in body["contracts"]
    assert body["quality_gate_required"] is True


def test_quality_gate_blocks_missing_production_evidence() -> None:
    result = evaluate_quality_gate(QualityEvidence(auth_tests=True, contract_tests=True))
    assert result.production_ready is False
    assert "mcp_tool_tests" in result.missing


def test_quality_gate_passes_when_all_evidence_exists() -> None:
    result = evaluate_quality_gate(
        QualityEvidence(
            auth_tests=True,
            contract_tests=True,
            mcp_tool_tests=True,
            idempotency_tests=True,
            observability_plan=True,
            runbook=True,
            agentic_eval_cases=True,
        )
    )
    assert result.production_ready is True
    assert result.score == 100


def test_mcp_contracts_include_side_effect_policy() -> None:
    response = client.get("/v1/mcp/contracts")
    assert response.status_code == 200
    checkout = next(tool for tool in response.json() if tool["name"] == "commerce.checkout")
    assert checkout["side_effects"] == "external_payment"


def test_orchestration_flow_lists_downstream_steps() -> None:
    response = client.post(
        "/v1/orchestrations/quote-to-fulfillment",
        json={"customer_id": "cust_1", "sku": "coffee", "quantity": 1, "destination_zip": "45202"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "planned"
    assert len(response.json()["steps"]) >= 5

