from ledger.core.models import Account


def conta(name: str):
    return Account.objects.create(name=name)
