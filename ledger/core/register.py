from ledger.core.models import (
    Agreement,
    Transaction,
)
from ledger.core.calculations import *


class _AgreementRegister:
    def __getattribute__(self, name: str) -> Transaction:
        agreement = Agreement.objects.get(name=name)
        agreement_transaction = Transaction(
            name=agreement.name,
            d_from=agreement.d_from,
            c_to=agreement.c_to,
        )
        exec(f'agreement_transaction.amount = {agreement.amount}')
        return agreement_transaction


AgreementRegister = _AgreementRegister()