from conftest import CONTRACT


def plant(vm, deploy, curator):
    vm.sender = curator
    contract = deploy(CONTRACT)
    contract.plant_specimen(
        "orchard-7",
        "Citrus Cipher",
        ["The answer is a fruit.", "Its skin is orange."],
        "Accept only a citrus fruit whose common skin color matches the second clue.",
        3,
        2,
    )
    return contract


def reject_graft(vm):
    vm.mock_llm(r".*Cipher Orchard semantic rule check.*", '{"fits":false,"conflicts":["not citrus"],"note":"fails the frozen growth law"}')
    vm.mock_llm(r".*Cipher Orchard verifier.*", '{"valid":true}')


def test_rejected_graft_cannot_be_replayed_by_a_fresh_wallet(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = plant(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    reject_graft(direct_vm)
    contract.propose_graft("orchard-7", "Apple", "It is a common fruit but does not satisfy the citrus rule.")
    first = contract.get_specimen("orchard-7")
    assert first["blight"] == 1 and first["state"] == "GERMINATING"
    assert contract.get_grafts_page("orchard-7", 0, 20)["total"] == 1

    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("one novel reasoned graft"):
        contract.propose_graft("orchard-7", "  APPLE  ", "A second wallet attempts to replay the same rejected graft.")

    after = contract.get_specimen("orchard-7")
    assert after["blight"] == 1 and after["state"] == "GERMINATING"
    assert contract.get_grafts_page("orchard-7", 0, 20)["total"] == 1
