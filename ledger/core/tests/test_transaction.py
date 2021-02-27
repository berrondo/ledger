from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    Ledger,
    Agreement,
    Percentual
)

from .utils import conta


def test_venda():
    # accounts:
    cash_in = conta()
    cash_out = conta()

    # defining the agreement:
    Venda = T('Venda',
        d_from=cash_in,
        c_to=cash_out
    )

    # using the agreement:
    Venda(100).save()

    assert Agreement.objects.all().count() == 1

    transactions = Ledger.objects.all()
    assert transactions.count() == 1
    assert transactions[0].amount == Decimal(100)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(100)


def test_venda_com_desconto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_desconto = conta()

    # defining the agreement:
    VendaComDesconto10 = T('VendaComDesconto10',
        d_from=cash_in,
        c_to=cash_out)(
        T('Desconto',
            amount=10,
            c_to=conta_desconto)
    )

    # using the agreement:
    VendaComDesconto10(100).save()

    transactions = Ledger.objects.all()
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

    # defining the agreement:
    VendaComImpostoPercentual = T('VendaComImpostoPercentual',
        d_from=cash_in,
        c_to=cash_out)(
        T('ImpostoPercentual',
            amount=Percentual(10),
            c_to=conta_imposto)
    )

    # using the agreement:
    VendaComImpostoPercentual(100).save()

    transactions = Ledger.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    assert transactions[1].c_to == conta_imposto

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_imposto.balance() == Decimal(10)


def test_venda_com_imposc_tocom_comissao_com_imposto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the agreement:
    VendaComImpostoEComissao = T('VendaComImpostoEComissao',
        d_from=cash_in,
        c_to=cash_out)(
        T('ComissaoPercentual',
            amount=Percentual(10),
            c_to=conta_comissao)(
            T('ImpostoPercentual',
                amount=Percentual(10),
                c_to=conta_imposto)
            ),
        T('ImpostoPercentual',
            amount=Percentual(10),
            c_to=conta_imposto)
    )

    # using the agreement:
    VendaComImpostoEComissao(100).save()

    transactions = Ledger.objects.all()
    assert transactions.count() == 4
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)
    assert transactions[2].amount == Decimal(1)
    assert transactions[3].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(80)
    assert conta_comissao.balance() == Decimal(9)
    assert conta_imposto.balance() == Decimal(11)


# some proposals for agreement definition:

# Venda = Transacoes(
#     name='Venda',
#     d_from=conta1,
#     c_to=conta2
# )(
#     Imposto(
#         percentual=10,
#         c_to=conta3
#     )
# )


# class Venda(Transacoes):
#     d_from = conta1
#     c_to = conta2
#
#     transactions = (
#         Imposto(
#             percentual=10,
#             c_to=conta3
#         ),
#     )


# class Venda(Transacoes):
#     class Meta:
#         d_from = conta1
#         c_to = conta2
#
#     class Imposto:
#         percentual = 10
#         c_to = conta3
#
#         class Discount:
#             percentual = 1
