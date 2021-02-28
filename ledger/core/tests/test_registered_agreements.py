from ledger.core.models import (
    Transaction as T,
    Agreement,
)
from ..calculations import Percentual
from ..register import AgreementRegister as R


def test():
    # creating a Transaction by naming it automatically
    # registers its Agreement blue print to be reused:
    t = T('VendaComplicada',
          amount=100)

    assert Agreement.objects.all().count() == 1

    assert R.VendaComplicada
    assert type(R.VendaComplicada) == Agreement
    assert R.VendaComplicada.amount == '100'

    #using:
    tt = T(R.VendaComplicada)(
        T('ImpostoInjusto',
          amount=Percentual(10))
    )