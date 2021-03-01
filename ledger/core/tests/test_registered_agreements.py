from ledger.core.models import (
    Transaction as T,
    Agreement,
)
from ..calculations import Percentual
from ..register import AgreementRegister as R


def test():
    # creating a Transaction by naming it automatically
    # registers its Agreement blue print to be reused:
    T('VendaComplicada',
        amount=100)

    T('ImpostoInjusto',
        amount=Percentual(10))

    assert Agreement.objects.all().count() == 2

    assert R.VendaComplicada
    assert type(R.VendaComplicada) == Agreement
    assert R.VendaComplicada.amount == '100'

    assert R.ImpostoInjusto
    assert type(R.ImpostoInjusto) == Agreement
    assert R.ImpostoInjusto.amount == 'Percentual(10)'

    #using:
    # R.VendaComplicada()(
    #     R.ImpostoInjusto()
    # )
