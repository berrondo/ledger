from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    _Transaction,
    Contract,
)
from .utils import conta


def test_transacoes_pre_definidas():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_desconto = conta()

    # defining the transactions:
    ContratoComDesconto10 = T('VendaComDesconto10',
      from_=cash_in,
      to_=cash_out)

    ContratoDesconto10 = T('Desconto10',
      amount=10,
      to_=conta_desconto)

    # defining the contract combining the transactions:
    VendaComDesconto10 =\
    T('VendaComDesconto10')(
        T('Desconto10')
    )

    # using the contract:
    VendaComDesconto10(100).save()

    assert Contract.objects.all().count() == 2
    ContratoComDesconto10.contract.name = 'ContratoComDesconto10'
    ContratoComDesconto10.contract.from_ = cash_in
    ContratoComDesconto10.contract.to_ = cash_out

    transactions = _Transaction.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_desconto.balance() == Decimal(10)
