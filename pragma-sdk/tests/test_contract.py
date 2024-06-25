from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.hash.address import compute_address
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair, StarkCurveSigner
from starknet_py.net.models import StarknetChainId
from starknet_py.contract import Contract
import asyncio
from pathlib import Path


# PREFUNDED CONFIGURATION FROM KATANA

PRIVATE_KEY = '0x2bbf4f9fd0bbb2e60b0316c1fe0b76cf7a4d0198bd493ced9b8df2a3a24d68a'
PUBLIC_KEY = '0x640466ebd2ce505209d3e5c4494b4276ed8f1cde764d757eb48831961f7cdea'
ACCOUNT_ADDRESS = '0xb3ff441a68610b30fd5e2abbf3a1548eb6ba6f3559f2862bf2dc757e5828ca'
RPC_URL =  'http://0.0.0.0:5050'


def read_contract(file_name: str) -> str:
    """
    Return contents of file_name from directory.
    """
    file_path = Path("pragma-sdk/contracts/target/dev") / file_name
    return file_path.read_text("utf-8")


async def get_account(): 
    # Returns a prefunded account 

    # First, make sure to generate private key and salt

    key_pair = KeyPair.from_private_key(int(PRIVATE_KEY, 16))

    # Prefund the address (using the token bridge or by sending fee tokens to the computed address)
    # Make sure the tx has been accepted on L2 before proceeding

    # Define the client to be used to interact with Starknet
    client = FullNodeClient(node_url=RPC_URL)

    return Account(
        address=  int(ACCOUNT_ADDRESS, 16), 
        client= client, 
        key_pair= key_pair,
        chain= StarknetChainId.MAINNET
    )

async def declare_deploy_contract(): 
    account = await get_account()

    compiled_contract_sierra = read_contract("contracts_simple_contract.contract_class.json")
    compiled_contract_casm = read_contract("contracts_simple_contract.compiled_contract_class.json")

    declare_transaction = await account.sign_declare_v3(
    compiled_contract=compiled_contract_sierra, compiled_class_hash=compiled_contract_casm, auto_estimate=True
    )
    resp = await account.client.declare(transaction=declare_transaction)
    await account.client.wait_for_tx(resp.transaction_hash)

    # To declare through Contract class you have to compile a contract and pass it
    # to Contract.declare_v1 or Contract.declare_v3
    declare_result = await Contract.declare_v3(
        account=account, compiled_contract=compiled_contract_sierra,compiled_class_hash=compiled_contract_casm,auto_estimate=True
    )
    # Wait for the transaction
    await declare_result.wait_for_acceptance()

    # After contract is declared it can be deployed
    deploy_result = await declare_result.deploy_v3(auto_estimate=True)
    await deploy_result.wait_for_acceptance()

    # You can pass more arguments to the `deploy` method. Check `API` section to learn more

    # To interact with just deployed contract get its instance from the deploy_result
    contract = deploy_result.deployed_contract

    return  contract.deployed_contract



if __name__ == "__main__":
    asyncio.run(declare_deploy_contract())