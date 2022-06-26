import pytest
from brownie import accounts, exceptions, network
from scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund, get_account
from scripts.deploy import deploy_fund_me


def test_can_fund_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    print(fund_me, dir(fund_me))
    enterance_fee = fund_me.getEnteranceFee() + 100

    fund_me.fund(
        {
            "from": account,
            "value": enterance_fee,
        },
    ).wait(1)

    assert fund_me.addressToAmountFunded(account.address) == enterance_fee

    fund_me.withdraw(
        {
            "from": account,
        },
    ).wait(1)

    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()

    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw(
            {
                "from": bad_actor,
            },
        )
