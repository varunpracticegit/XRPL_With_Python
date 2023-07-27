import xrpl
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs


testnet_url = "https://s.altnet.rippletest.net:51234"

def mint_token(seed, uri, flags, transfer_fee, taxon):

    mint_wallet=Wallet(seed, 16237283)
    client=JsonRpcClient(testnet_url)

    mint_tx=xrpl.models.transactions.NFTokenMint(
        account=mint_wallet.classic_address,
        uri=xrpl.utils.str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )

    signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
        mint_tx, mint_wallet, client)
    
    reply=""
    try:
        response=xrpl.transaction.send_reliable_submission(signed_tx,client)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply


def get_tokens(account):
    """get_tokens"""

    client=JsonRpcClient(testnet_url)

    acct_nfts=AccountNFTs(
        account=account
    )

    response=client.request(acct_nfts)
    return response.result

def burn_token(seed, nftoken_id):
    """burn_token"""

    owner_wallet=Wallet(seed, sequence=16237283)
    client=JsonRpcClient(testnet_url)

    burn_tx=xrpl.models.transactions.NFTokenBurn(
        account=owner_wallet.classic_address,
        nftoken_id=nftoken_id    
    )

    signed_tx=xrpl.transaction.safe_sign_and_autofill_transaction(
        burn_tx, owner_wallet, client)   
    
    reply=""
    try:
        response=xrpl.transaction.send_reliable_submission(signed_tx,client)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply