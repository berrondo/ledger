from decimal import Decimal

from ledger.core.models import Contract, Transaction, Account


def test_venda():
    # accounts:
    conta1 = Account.objects.create()
    conta2 = Account.objects.create()

    # defining Venda contract:
    Venda = Contract(
        base=Transaction(
            debit_from=conta1,
            credit_to=conta2
        )
    )

    # using Venda contract:
    v = Venda(100)
    v.save()

    assert Transaction.objects.all().count() == 1
    assert Transaction.objects.all().first().amount == Decimal(100)


def test_venda_com_desconto():
    # accounts:
    conta1 = Account.objects.create()
    conta2 = Account.objects.create()

    # defining Venda contract:
    VendaCom10DinheirosDeDesconto = Contract(
        base=Transaction(
            debit_from=conta1,
            credit_to=conta2
        ),
        sub_transactions=dict(
            Desconto=Transaction(
                amount=10,
            )
        )
    )

    # using Venda contract:
    v = VendaCom10DinheirosDeDesconto(100)
    v.save()

    assert Transaction.objects.all().count() == 2
    assert Transaction.objects.all().first().amount == Decimal(100)


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
