import json
import re
import secrets
import time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
DEPLOYMENT = json.loads((ROOT / "deployment.json").read_text(encoding="utf-8"))


def env_value(name):
    match = re.search(rf'^{name}\s*=\s*"?([^"\r\n]+)', ENV, re.M)
    if not match:
        raise RuntimeError(f"{name} missing")
    return match.group(1).strip()


def account_from_random_key():
    return create_account(account_private_key="0x" + secrets.token_hex(32))


def wait(client, tx_hash):
    receipt = client.wait_for_transaction_receipt(
        transaction_hash=tx_hash,
        status="FINALIZED",
        retries=180,
        interval=5000,
        full_transaction=True,
    )
    executions = [
        str(row.get("execution_result", "")).upper()
        for row in receipt.get("consensus_data", {}).get("leader_receipt", [])
    ]
    return receipt, executions


owner = create_account(account_private_key=env_value("ACCOUNT_2_GENLAYER_PRIVATE_KEY"))
first_player = account_from_random_key()
replay_player = account_from_random_key()
owner_client = create_client(chain=studionet, account=owner)
first_client = create_client(chain=studionet, account=first_player)
replay_client = create_client(chain=studionet, account=replay_player)
address = DEPLOYMENT["contractAddress"]
specimen_id = "DUPLICATE-REPLAY-" + str(int(time.time()))

plant_tx = owner_client.write_contract(
    address=address,
    function_name="plant_specimen",
    args=[
        specimen_id,
        "Citrus Cipher",
        ["The answer is a fruit.", "Its skin is orange."],
        "Accept only a citrus fruit whose common skin color matches the second clue.",
        3,
        2,
    ],
)
_, plant_execution = wait(owner_client, plant_tx)
assert "SUCCESS" in plant_execution

graft = "STEEL WRENCH"
reasoning = "This is a metal tool and intentionally fails the frozen citrus-fruit rule."
first_tx = first_client.write_contract(
    address=address,
    function_name="propose_graft",
    args=[specimen_id, graft, reasoning],
)
_, first_execution = wait(first_client, first_tx)
assert "SUCCESS" in first_execution
before = owner_client.read_contract(address=address, function_name="get_specimen", args=[specimen_id])
before_page = owner_client.read_contract(address=address, function_name="get_grafts_page", args=[specimen_id, 0, 20])
assert before["blight"] == 1 and before["state"] == "GERMINATING"
assert before_page["total"] == 1 and before_page["items"][0]["accepted"] is False

replay_tx = replay_client.write_contract(
    address=address,
    function_name="propose_graft",
    args=[specimen_id, "  steel wrench  ", "A fresh wallet attempts to replay the rejected graft without a new proposal."],
)
replay_receipt, replay_execution = wait(replay_client, replay_tx)
assert "SUCCESS" not in replay_execution

after = owner_client.read_contract(address=address, function_name="get_specimen", args=[specimen_id])
after_page = owner_client.read_contract(address=address, function_name="get_grafts_page", args=[specimen_id, 0, 20])
assert after["blight"] == before["blight"] == 1
assert after["state"] == before["state"] == "GERMINATING"
assert after_page["total"] == before_page["total"] == 1

evidence = {
    "network": "StudioNet",
    "contract": address,
    "specimenId": specimen_id,
    "wallets": {
        "curator": owner.address,
        "firstAttempt": first_player.address,
        "replayAttempt": replay_player.address,
    },
    "transactions": {"plant": plant_tx, "rejectedGraft": first_tx, "duplicateReplay": replay_tx},
    "results": {
        "plantExecution": plant_execution,
        "rejectedGraftExecution": first_execution,
        "duplicateReplayExecution": replay_execution,
        "duplicateConsensus": replay_receipt.get("result_name"),
        "before": {"blight": before["blight"], "state": before["state"], "history": before_page["total"]},
        "after": {"blight": after["blight"], "state": after["state"], "history": after_page["total"]},
    },
}
(ROOT / "evidence").mkdir(exist_ok=True)
(ROOT / "evidence" / "duplicate-replay-live.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
print(json.dumps(evidence), flush=True)
