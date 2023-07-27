import xrpl
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests.account_info import AccountInfo

testnet_url = "https://s.altnet.rippletest.net:51234"

def create_trust_line(seed, issuer, currency, amount):
    """create_trust_line"""

    # Get the wallet and a new client instance.

    receiving_wallet = Wallet(seed, 16237283)
    client = JsonRpcClient(testnet_url)

    # Define the TrustSet transaction.
    trustline_tx=xrpl.models.transactions.TrustSet(
        account=receiving_wallet.classic_address,
        limit_amount=xrpl.models.amounts.IssuedCurrencyAmount(
            currency=currency,
            issuer=issuer,
            value=int(amount)
        )
    )

    # Sign the transaction.

    signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
        trustline_tx, receiving_wallet, client)
    
    # Submit the transaction to the XRP Ledger.
    reply = ""
    try:
        response = xrpl.transaction.send_reliable_submission(signed_tx,client)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"

    # Return the results.
    return reply

def send_currency(seed, destination, currency, amount):
    """send_currency"""

    # Get the sending wallet and a client instance on Testnet.
    sending_wallet=Wallet(seed, 16237283)
    client=JsonRpcClient(testnet_url)

    # Define the payment transaction.

    send_currency_tx=xrpl.models.transactions.Payment(
        account=sending_wallet.classic_address,
        amount=xrpl.models.amounts.IssuedCurrencyAmount(
            currency=currency,
            value=int(amount),
            issuer=sending_wallet.classic_address
        ),
        destination=destination
    )

    # Sign and fill the transaction.
    signed_tx=xrpl.transaction.safe_sign_and_autofill_transaction(
        send_currency_tx, sending_wallet, client)
    
    # Submit the transaction and get the response.
    reply = ""
    try:
        response=xrpl.transaction.send_reliable_submission(signed_tx,client)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"

    # Return the JSON response
    return reply


def get_balance(sb_account_id, op_account_id):
    """get_balance"""

    #Connect to the XRP Ledger and instantiate a client.

    JSON_RPC_URL='wss://s.altnet.rippletest.net:51234'
    client=JsonRpcClient(JSON_RPC_URL)

    # Create the GatewayBalances request.

    balance=xrpl.models.requests.GatewayBalances(
        account=sb_account_id,
        ledger_index="validated",
        hotwallet=[op_account_id]
    )

    # Return the result.
    response = client.request(balance)
    return response.result


def configure_account(seed, default_setting):
    """configure_account"""

    # Get the account wallet and instantiate a client.
    wallet=Wallet(seed, 16237283)
    client=JsonRpcClient(testnet_url)

    # Enable and disable ripple
    if (default_setting):
        setting_tx=xrpl.models.transactions.AccountSet(
            account=wallet.classic_address,
            set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE
        )
    else:
        setting_tx=xrpl.models.transactions.AccountSet(
            account=wallet.classic_address,
            clear_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE
        )
    
    # Sign and fill the transaction.
    signed_tx=xrpl.transaction.safe_sign_and_autofill_transaction(
        setting_tx, wallet, client)
    
    # Submit the transaction and get results.
    reply = ""
    try:
        response = xrpl.transaction.send_reliable_submission(signed_tx,client)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"

    # Return the results.
    return reply







