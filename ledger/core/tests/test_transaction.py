from decimal import Decimal

import pytest

from ledger.core.models import Journal, Transaction, Account, Percentual


@pytest.fixture
def conta1():
    return Account.objects.create()


@pytest.fixture
def conta2():
    return Account.objects.create()


@pytest.fixture
def conta3():
    return Account.objects.create()


def test_venda(conta1, conta2):
    # defining Venda contract:
    Venda = Journal(
        Transaction(
            debit_from=conta1,
            credit_to=conta2
        )
    )

    # using Venda contract:
    v = Venda(100)
    v.save()

    all_transactions = Transaction.objects.all()
    assert all_transactions.count() == 1
    assert all_transactions.first().amount == Decimal(100)


def test_venda_com_desconto(conta1, conta2):
    # defining Venda contract:
    VendaCom10DinheirosDeDesconto = Journal(
        Transaction(
            debit_from=conta1,
            credit_to=conta2
        ),
        Transaction(
            amount=-10,
        )
    )

    # using Venda contract:
    v = VendaCom10DinheirosDeDesconto(100)
    v.save()

    all_transactions = Transaction.objects.all()
    assert all_transactions.count() == 2
    assert all_transactions[0].amount == Decimal(100)
    assert all_transactions[1].amount == Decimal(-10)

    assert conta2.balance() == Decimal(90)


def test_venda_com_imposto(conta1, conta2, conta3):
    # defining Venda contract:
    VendaCom10PorcentoDeImposto = Journal(
        Transaction(
            debit_from=conta1,
            credit_to=conta2
        ),
        Transaction(
            amount=-10,
            credit_to=conta3
        )
    )

    # using Venda contract:
    v = VendaCom10PorcentoDeImposto(100)
    v.save()

    all_transactions = Transaction.objects.all()
    assert all_transactions.count() == 2
    assert all_transactions[0].amount == Decimal(100)
    assert all_transactions[1].amount == Decimal(-10)

    assert all_transactions[1].credit_to == conta3

    assert conta2.balance() == Decimal(90)
    assert conta3.balance() == Decimal(10)


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
