from decimal import Decimal

from ledger.core.models import Journal, Transaction as T, _Transaction, Account, Percentual


def conta():
    return Account.objects.create()


def test_venda():
    # accounts:
    cash_in = conta()
    cash_out = conta()

    # defining Venda contract:
    Venda = Journal('Venda',
        T('Venda',
            debit_from=cash_in,
            credit_to=cash_out)
    )

    # using Venda contract:
    v = Venda(100)
    v.save()

    all_transactions = _Transaction.objects.all()
    assert all_transactions.count() == 1
    assert all_transactions[0].amount == Decimal(100)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(100)


def test_venda_com_desconto():
    # accounts:
    cash_in = conta()
    cash_out = conta()

    # defining Venda contract:
    VendaComDesconto10 = Journal('VendaComDesconto10',
        T('Venda',
            debit_from=cash_in,
            credit_to=cash_out),
        T('DescontoAbsoluto',
            amount=-10,)
    )

    # using Venda contract:
    v = VendaComDesconto10(100)
    v.save()

    all_transactions = _Transaction.objects.all()
    assert all_transactions.count() == 2
    assert all_transactions[0].amount == Decimal(100)
    assert all_transactions[1].amount == Decimal(-10)

    assert cash_in.balance() == Decimal(-90)
    assert cash_out.balance() == Decimal(90)


def test_venda_com_imposto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_imposto = conta()

    # defining Venda contract:
    VendaComImpostoPercentual = Journal('VendaComImpostoPercentual',
        T('Venda',
            debit_from=cash_in,
            credit_to=cash_out),
        T('ImpostoPercentual',
            amount=Percentual(10),
            debit_from=cash_out,
            credit_to=conta_imposto)
    )

    # using Venda contract:
    v = VendaComImpostoPercentual(100)
    v.save()

    all_transactions = _Transaction.objects.all()
    assert all_transactions.count() == 2
    assert all_transactions[0].amount == Decimal(100)
    assert all_transactions[1].amount == Decimal(10)

    assert all_transactions[1].credit_to == conta_imposto

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_imposto.balance() == Decimal(10)


def test_venda_com_imposto_com_comissao_com_imposto():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining Venda contract:
    VendaComImpostoEComissao = Journal(
        'VendaComImpostoEComissao',
        T('Venda',
            debit_from=cash_in,
            credit_to=cash_out,),
        T('ComissaoPercentual',
            amount=Percentual(10),
            debit_from=cash_out,
            credit_to=conta_comissao,
            sub=T('ImpostoPercentual',
                amount=Percentual(10),
                credit_to=conta_imposto)),
        T('ImpostoPercentual',
            amount=Percentual(10),
            debit_from=cash_out,
            credit_to=conta_imposto)
    )

    # using Venda contract:
    v = VendaComImpostoEComissao(100)
    v.save()

    all_transactions = _Transaction.objects.all()
    assert all_transactions.count() == 4
    assert all_transactions[0].amount == Decimal(100)
    assert all_transactions[1].amount == Decimal(10)
    assert all_transactions[2].amount == Decimal(1)
    assert all_transactions[3].amount == Decimal(10)

    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(80)  # 81 ??
    assert conta_comissao.balance() == Decimal(9)
    assert conta_imposto.balance() == Decimal(11)


# some proposals for contract definition:

# Venda = Transacoes(
#     name='Venda',
#     debit_from=conta1,
#     credit_to=conta2
# )(
#     Imposto(
#         percentual=10,
#         credit_to=conta3
#     )
# )


# class Venda(Transacoes):
#     debit_from = conta1
#     credit_to = conta2
#
#     transactions = (
#         Imposto(
#             percentual=10,
#             credit_to=conta3
#         ),
#     )


# class Venda(Transacoes):
#     class Meta:
#         debit_from = conta1
#         credit_to = conta2
#
#     class Imposto:
#         percentual = 10
#         credit_to = conta3
#
#         class Discount:
#             percentual = 1
