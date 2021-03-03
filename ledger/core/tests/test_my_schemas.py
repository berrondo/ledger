from decimal import Decimal

import pytest

from ledger.core.models import Transaction as T
from ledger.core.register import SchemaRegister as R
from ledger.core.calculations import *
from ledger.core.tests.utils import conta

@pytest.fixture(scope='function')
def contas():
    # accounts:
    class A:
        in_labrdev_sch = conta('Income.Margarin.LabrDev.LongView.SAManager.SCH')
        in_ggeek_gespag = conta('Income.Margarin.GarageGeek.Gespag')

        as_cash = conta('Assets.cash')

        ex_prolabore = conta('Expense.Prolabore')
        ex_das_anexo_iii = conta('Expense.Tax.DAS.AnexoIII')
        ex_das_anexo_v = conta('Expense.Tax.DAS.AnexoV')
        ex_iss_rio = conta('Expense.Tax.Rio.ISS')
        ex_irrf = conta('Expense.Tax.BR.IRRF')
        ex_inss = conta('Expense.Tax.BR.INSS')

    # defining Simple Transaction Schemas:
    T('PrestacaoServico_GGeek',
        d_from=A.in_ggeek_gespag,
        c_to=A.as_cash)

    T('ProLaboreMinimo',
        d_from=A.as_cash,
        amount=SalarioMinimo(),
        c_to=A.ex_prolabore)

    T('ProLaboreFatorR',
        d_from=A.as_cash,
        amount=2240,
        c_to=A.ex_prolabore)

    T('DASAnexoIII',
        amount=Percentual(6),
        c_to=A.ex_das_anexo_iii)

    T('DASAnexoV',
        amount=Percentual(15.5),
        c_to=A.ex_das_anexo_v)

    T('IssRio',
        amount=Percentual(2.17),
        c_to=A.ex_iss_rio)

    T('IRRF',
        amount=IRRF(),
        c_to=A.ex_irrf)

    T('INSS',
        amount=INSS(),
        c_to=A.ex_inss)

    return A


def test_anexo_iii(contas):
    # Composed Transaction Schema in a Journal:
    PrestacaoServico_GGeek = R.PrestacaoServico_GGeek(
        R.ProLaboreFatorR(
            R.IRRF,
            R.INSS
        ),
        R.DASAnexoIII
    )

    PrestacaoServico_GGeek(8000).save()

    # checking...
    assert contas.in_ggeek_gespag.balance() == -8000
    assert contas.ex_das_anexo_iii.balance() == Decimal('480')
    assert contas.ex_prolabore.balance() == Decimal('1968.4')
    assert contas.ex_inss.balance() == Decimal('246.4')
    assert contas.ex_irrf.balance() == Decimal('6.72')


def test_anexo_v(contas):
    # Composed Transaction Schema in a Journal:
    PrestacaoServico_GGeek = R.PrestacaoServico_GGeek(
        R.ProLaboreMinimo(
            R.IRRF,
            R.INSS
        ),
        R.DASAnexoV
    )

    PrestacaoServico_GGeek(8000).save()

    # checking...
    assert contas.in_ggeek_gespag.balance() == -8000
    assert contas.ex_das_anexo_v.balance() == Decimal('1240.00')
    assert contas.ex_prolabore.balance() == 979
    assert contas.ex_inss.balance() == 121
    assert contas.ex_irrf.balance() == 0



