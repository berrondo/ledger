from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    Ledger,
    Agreement,
    Percentual,
)
from .utils import conta


def test_transacoes_pre_definidas():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_desconto = conta()

    # defining the Transaction Agreements:
    T('VendaComDesconto10',
        d_from=cash_in,
        c_to=cash_out)

    T('Desconto10',
        amount=10,
        c_to=conta_desconto)

    # defining new combined Transaction Agreements:
    VendaComDesconto10 =\
    T('VendaComDesconto10')(
        T('Desconto10')
    )

    # checking registered Transaction Agreements:
    assert Agreement.objects.all().count() == 2

    # using the agreement:
    VendaComDesconto10(100).save()

    # checking transactions in the ledger
    transactions = Ledger.objects.all()
    assert transactions.count() == 2
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)

    # checking account balances:
    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_desconto.balance() == Decimal(10)


def test_venda_com_imposc_tocom_comissao_com_imposc_tocom_composicao_de_transacoes():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the Transaction Agreements:
    T('VendaComImpostoEComissao',
        d_from=cash_in,
        c_to=cash_out)

    T('ComissaoDe10Porcento',
        amount=Percentual(10),
        c_to=conta_comissao)

    T('ImpostoDe10Porcento',
        amount=Percentual(10),
        c_to=conta_imposto)

    # defining new combined Transaction Agreement:
    VendaComImpostoEComissao =\
    T('VendaComImpostoEComissao')(
        T('ComissaoDe10Porcento')(
            T('ImpostoDe10Porcento')
        ),
        T('ImpostoDe10Porcento')
    )

    # checking registered Transaction Agreements:
    assert Agreement.objects.all().count() == 3

    # using the agreement:
    VendaComImpostoEComissao(100).save()

    # checking transactions in the ledger
    transactions = Ledger.objects.all()
    assert transactions.count() == 4
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)
    assert transactions[2].amount == Decimal(1)
    assert transactions[3].amount == Decimal(10)

    # checking account balances:
    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(80)
    assert conta_comissao.balance() == Decimal(9)
    assert conta_imposto.balance() == Decimal(11)


def test_venda_com_imposc_tocom_comissao_com_imposc_tocom_composicao_de_transacoes_2():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the Transaction Agreements:
    T('VendaComImpostoEComissao',
      d_from=cash_in,
      c_to=cash_out)

    T('ComissaoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_comissao)

    T('ImpostoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_imposto)

    # defining new combined Transaction Agreement different order:
    VendaComImpostoEComissao2 =\
    T('VendaComImpostoEComissao')(
        T('ImpostoDe10Porcento'),
        T('ComissaoDe10Porcento')(
            T('ImpostoDe10Porcento')
        )
    )

    # checking registered Transaction Agreements:
    assert Agreement.objects.all().count() == 3

    # using the Transaction Agreement:
    VendaComImpostoEComissao2(100).save()

    # checking transactions in the ledger
    transactions = Ledger.objects.all()
    assert transactions.count() == 4
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)
    assert transactions[2].amount == Decimal(10)
    assert transactions[3].amount == Decimal(1)

    # checking account balances:
    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(80)
    assert conta_comissao.balance() == Decimal(9)
    assert conta_imposto.balance() == Decimal(11)


def test_venda_com_imposc_tocom_comissao_com_imposc_tocom_composicao_de_transacoes_3():
    # accounts:
    cash_in = conta()
    cash_out = conta()
    conta_comissao = conta()
    conta_imposto = conta()

    # defining the Transaction Agreements:
    T('VendaComImpostoEComissao',
      d_from=cash_in,
      c_to=cash_out)

    T('ComissaoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_comissao)

    T('ImpostoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_imposto)

    # defining new combined Transaction Agreement another order:
    VendaComImpostoEComissao2 =\
    T('VendaComImpostoEComissao')(
        T('ImpostoDe10Porcento')(
            T('ComissaoDe10Porcento')(
                T('ImpostoDe10Porcento')
            )
        )
    )

    # checking registered Transaction Agreements:
    assert Agreement.objects.all().count() == 3

    # using the Transaction Agreement:
    VendaComImpostoEComissao2(100).save()

    # checking transactions in the ledger
    transactions = Ledger.objects.all()
    assert transactions.count() == 4
    assert transactions[0].amount == Decimal(100)
    assert transactions[1].amount == Decimal(10)
    assert transactions[2].amount == Decimal(1)
    assert transactions[3].amount == Decimal('0.10')

    # checking account balances:
    assert cash_in.balance() == Decimal(-100)
    assert cash_out.balance() == Decimal(90)
    assert conta_comissao.balance() == Decimal('0.90')
    assert conta_imposto.balance() == Decimal('9.10')
