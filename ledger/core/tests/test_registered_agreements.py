from ledger.core.models import (
    Transaction as T,
    Agreement,
    Percentual,
)
from ..register import AgreementRegister as R


def test():
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