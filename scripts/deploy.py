from brownie import FundMe, config, network

from scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    deploy_mocks,
    get_account,
    get_mock_pricefeed,
)


def deploy_fund_me():
    account = get_account()
    print(f"Using account: {account}")

    active_network = network.show_active()

    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Not using development network!")

        pricefeed_address = config["networks"][active_network][
            "eth_usd_price_feed"
        ]

    else:
        deploy_mocks()
        pricefeed_address = get_mock_pricefeed()

    print("Deploying contract")
    fund_me = FundMe.deploy(
        pricefeed_address,
        {
            "from": account,
        },
        publish_source=config["networks"][active_network].get("verify"),
    )
    print(f"Deployed contract at {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
