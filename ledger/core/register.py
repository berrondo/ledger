from ledger.core.models import (
    Schema,
    Transaction,
)
from ledger.core.calculations import *


class _SchemaRegister:
    def __getattribute__(self, name: str) -> Transaction:
        schema = Schema.objects.get(name=name)
        transaction = Transaction(
            name=schema.name,
            d_from=schema.d_from,
            c_to=schema.c_to,
        )
        exec(f'transaction.amount = {schema.amount}')
        return transaction


SchemaRegister = _SchemaRegister()