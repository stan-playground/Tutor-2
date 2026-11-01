"""Generate disposable synthetic login credentials without displaying them."""

import json
import os
import secrets
from pathlib import Path


def prepare() -> None:
    """Prepare an ignored realm import; reuse it while its Keycloak realm exists."""
    root = Path(__file__).resolve().parents[2]
    target = root / ".highgrade/local/keycloak/tutor-copilot-realm.json"
    existing = json.loads(target.read_text()) if target.exists() else {"users": []}
    credentials = {user["id"]: user["credentials"] for user in existing["users"]}
    realm = json.loads((Path(__file__).parent / "realm.json").read_text())
    for user in realm["users"]:
        user["credentials"] = credentials.get(user["id"]) or [
            {"type": "password", "value": secrets.token_urlsafe(32), "temporary": False}
        ]
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        json.dump(realm, stream)
    temporary.replace(target)
    print("Synthetic Keycloak import prepared; credentials were not displayed.")


if __name__ == "__main__":
    prepare()
