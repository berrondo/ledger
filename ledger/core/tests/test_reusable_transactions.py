from decimal import Decimal

from ledger.core.models import (
    Transaction as T,
    Ledger,
    Schema,
)
from ..calculations import Percentual
from .utils import conta


def test_transacoes_pre_definidas():
    # accounts:
    cash_in = conta('cash_in')
    cash_out = conta('cash_out')
    conta_desconto = conta('conta_desconto')

    # defining the Transaction Schemas:
    T('VendaComDesconto10',
        d_from=cash_in,
        c_to=cash_out)

    T('Desconto10',
        amount=10,
        c_to=conta_desconto)

    # defining new combined Transaction Schemas:
    VendaComDesconto10 =\
    T('VendaComDesconto10')(
        T('Desconto10')
    )

    # checking registered Transaction Schemas:
    assert Schema.objects.all().count() == 2

    # using the schema:
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
    cash_in = conta('cash_in')
    cash_out = conta('cash_out')
    conta_comissao = conta('conta_comissao')
    conta_imposto = conta('conta_imposto')

    # defining the Transaction Schemas:
    T('VendaComImpostoEComissao',
        d_from=cash_in,
        c_to=cash_out)

    T('ComissaoDe10Porcento',
        amount=Percentual(10),
        c_to=conta_comissao)

    T('ImpostoDe10Porcento',
        amount=Percentual(10),
        c_to=conta_imposto)

    # defining new combined Transaction Schema:
    VendaComImpostoEComissao =\
    T('VendaComImpostoEComissao')(
        T('ComissaoDe10Porcento')(
            T('ImpostoDe10Porcento')
        ),
        T('ImpostoDe10Porcento')
    )

    # checking registered Transaction Schemas:
    assert Schema.objects.all().count() == 3

    # using the schema:
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
    cash_in = conta('cash_in')
    cash_out = conta('cash_out')
    conta_comissao = conta('conta_comissao')
    conta_imposto = conta('conta_imposto')

    # defining the Transaction Schemas:
    T('VendaComImpostoEComissao',
      d_from=cash_in,
      c_to=cash_out)

    T('ComissaoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_comissao)

    T('ImpostoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_imposto)

    # defining new combined Transaction Schema different order:
    VendaComImpostoEComissao2 =\
    T('VendaComImpostoEComissao')(
        T('ImpostoDe10Porcento'),
        T('ComissaoDe10Porcento')(
            T('ImpostoDe10Porcento')
        )
    )

    # checking registered Transaction Schemas:
    assert Schema.objects.all().count() == 3

    # using the Transaction Schema:
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
    cash_in = conta('cash_in')
    cash_out = conta('cash_out')
    conta_comissao = conta('conta_comissao')
    conta_imposto = conta('conta_imposto')

    # defining the Transaction Schemas:
    T('VendaComImpostoEComissao',
      d_from=cash_in,
      c_to=cash_out)

    T('ComissaoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_comissao)

    T('ImpostoDe10Porcento',
      amount=Percentual(10),
      c_to=conta_imposto)

    # defining new combined Transaction Schema another order:
    VendaComImpostoEComissao2 =\
    T('VendaComImpostoEComissao')(
        T('ImpostoDe10Porcento')(
            T('ComissaoDe10Porcento')(
                T('ImpostoDe10Porcento')
            )
        )
    )

    # checking registered Transaction Schemas:
    assert Schema.objects.all().count() == 3

    # using the Transaction Schema:
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
