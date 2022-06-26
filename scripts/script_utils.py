from .development_environment import (
    FORKED_LOCAL_ENVIRONMENTS,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

from brownie import (
    network,
    config,
    accounts,
    MockV3Aggregator,
)


PRECISION = 8
INIT_VALUE = 200_000_000_000


def get_account():
    active_network = network.show_active()
    if active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS or active_network in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(
        config["wallet"]["private_key"]
    )


def get_mock_pricefeed():
    return MockV3Aggregator[-1].address


def deploy_mocks():
    print(f"Using {network.show_active()}")
    print("Deploying Mocks...")
    if not MockV3Aggregator:
        print("Creating MockAggregator...")
        MockV3Aggregator.deploy(
            PRECISION,  # Decimal points
            INIT_VALUE,  # Seed value
            {
                "from": get_account(),
            },
        )
    else:
        print(f"Using existing MockAggregator {MockV3Aggregator[-1].address}")
    print("Deployed Mocks!")


def main():
    deploy_mocks()
