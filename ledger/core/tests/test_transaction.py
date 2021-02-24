from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    _Transaction,
    Contract,
    Percentual
)

from .utils import conta


def test_venda():
    # accounts:
    cash_in = conta()
    cash_out = conta()

    # defining the contract:
    Venda = T('Venda',
        from_=cash_in,
        to_=cash_out
    )

    # using the contract:
    Venda(100).save()

    assert Contract.objects.all().count() == 1

    transactions = _Transaction.objects.all()
    assert transactions.count() == 1
    assert transactions[0].amount == Decimal(100)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(100)


def test_venda_com_desconto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_desconto = conta()

    # defining the contract:
    VendaComDesconto10 = T('VendaComDesconto10',
        from_=cash_in,
        to_=cash_out)(
        T('Desconto',
            amount=10,
            to_=conta_desconto)
    )

    # using the contract:
    VendaComDesconto10(100).save()

    transactions = _Transaction.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_desconto.balance() == Decimal(10)


def test_venda_com_imposto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_imposto = conta()

    # defining the contract:
    VendaComImpostoPercentual = T('VendaComImpostoPercentual',
        from_=cash_in,
        to_=cash_out)(
        T('ImpostoPercentual',
            amount=Percentual(10),
            to_=conta_imposto)
    )

    # using the contract:
    VendaComImpostoPercentual(100).save()

    transactions = _Transaction.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    assert transactions[1].to_ == conta_imposto

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_imposto.balance() == Decimal(10)


def test_venda_com_imposto_com_comissao_com_imposto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the contract:
    VendaComImpostoEComissao = T('VendaComImpostoEComissao',
        from_=cash_in,
        to_=cash_out)(
        T('ComissaoPercentual',
            amount=Percentual(10),
            to_=conta_comissao)(
            T('ImpostoPercentual',
                amount=Percentual(10),
                to_=conta_imposto)
            ),
        T('ImpostoPercentual',
            amount=Percentual(10),
            to_=conta_imposto)
    )

    # using the contract:
    VendaComImpostoEComissao(100).save()

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


# some proposals for contract definition:

# Venda = Transacoes(
#     name='Venda',
#     from_=conta1,
#     to_=conta2
# )(
#     Imposto(
#         percentual=10,
#         to_=conta3
#     )
# )


# class Venda(Transacoes):
#     from_ = conta1
#     to_ = conta2
#
#     transactions = (
#         Imposto(
#             percentual=10,
#             to_=conta3
#         ),
#     )


# class Venda(Transacoes):
#     class Meta:
#         from_ = conta1
#         to_ = conta2
#
#     class Imposto:
#         percentual = 10
#         to_ = conta3
#
#         class Discount:
#             percentual = 1
