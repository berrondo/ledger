from ledger.core.models import Agreement


class _AgreementRegister:
    def __getattribute__(self, name):
        agreement = Agreement.objects.get(name=name)
        return agreement


AgreementRegister = _AgreementRegister()