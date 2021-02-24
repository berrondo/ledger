from ledger.core.models import Account


def conta():
    return Account.objects.create()
