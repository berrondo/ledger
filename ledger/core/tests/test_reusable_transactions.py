from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    _Transaction,
    Contract, Percentual,
)
from .utils import conta


def test_transacoes_pre_definidas():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_desconto = conta()

    # defining the transactions:
    T('VendaComDesconto10',
        from_=cash_in,
        to_=cash_out)

    T('Desconto10',
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

    transactions = _Transaction.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_desconto.balance() == Decimal(10)


def test_venda_com_imposto_com_comissao_com_imposto_com_composicao_de_transacoes():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the transactions:
    T('VendaComImpostoEComissao',
        from_=cash_in,
        to_=cash_out)

    T('ComissaoPercentual',
        amount=Percentual(10),
        to_=conta_comissao)

    T('ImpostoPercentual',
        amount=Percentual(10),
        to_=conta_imposto)

    # defining the contract combining the transactions:
    VendaComImpostoEComissao =\
    T('VendaComImpostoEComissao')(
        T('ComissaoPercentual')(
            T('ImpostoPercentual')
        ),
        T('ImpostoPercentual')
    )

    # using the contract:
    VendaComImpostoEComissao(100).save()

    assert Contract.objects.all().count() == 3

    transactions = _Transaction.objects.all()
    assert transactions.count() == 4
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)
    assert transactions[2].amount == Decimal(1)
    assert transactions[3].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(80)
    assert conta_comissao.balance() == Decimal(9)
    assert conta_imposto.balance() == Decimal(11)
