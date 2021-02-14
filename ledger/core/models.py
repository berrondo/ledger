from django.db import models
from django.utils.datetime_safe import datetime

from polymorphic.models import PolymorphicModel


class Account(models.Model):
    ...


class Transaction(PolymorphicModel):
    created_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    debit_from = models.ForeignKey(Account, on_delete=models.PROTECT)
    credit_to = models.ForeignKey(Account, on_delete=models.PROTECT)
    # uuid =


class Contract:
    def __init__(self, base: Transaction, sub_transactions=None):
        if sub_transactions is None:
            sub_transactions = {}
        self.base = base
        self.sub_transactions = sub_transactions

    def __call__(self, amount):
        self.created_at = datetime.now()
        self._process_sub_transactions()
        self.base.amount = amount
        self.base.created_at = self.created_at
        return self

    def _process_sub_transactions(self):
        for name, transaction in self.sub_transactions.items():
            transaction.debit_from = self.base.debit_from
            transaction.credit_to = self.base.credit_to
            transaction.created_at = self.created_at

    def save(self):
        for transaction in [self.base] + list(self.sub_transactions.values()):
            transaction.save()
