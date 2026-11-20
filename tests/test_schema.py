from typing import Any

import schemathesis

from app.main import app

schema = schemathesis.openapi.from_asgi("/openapi.json", app)


@schema.parametrize()
def test_api_rispetta_lo_schema(case: Any) -> None:
    case.call_and_validate()