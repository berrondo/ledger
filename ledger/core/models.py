from decimal import Decimal
from typing import Union, List

from django.db import models
from django.db.models import Sum
from django.utils.datetime_safe import datetime

from ledger.core.calculations import Percentual


class Account(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def all_credits(self):
        return Ledger.objects.filter(
            c_to=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def all_debits(self):
        return Ledger.objects.filter(
            d_from=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def balance(self):
        return self.all_credits() - self.all_debits()


class Agreement(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.CharField(max_length=255, null=True)
    d_from = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, related_name='cdebit')
    c_to = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, related_name='ccredit')


class Ledger(models.Model):
    created_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    d_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='tdebit')
    c_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='tcredit')


class Transaction:
    def __init__(self,
                 name: str,
                 created_at=None,
                 amount: Union[int, Decimal, Percentual]=None,
                 d_from: Account=None,
                 c_to: Account=None):

        self.name = name
        self.created_at = created_at

        self.amount = amount
        self.d_from = d_from
        self.c_to = c_to

        self.sub_transactions = []

        # agreement lookup...
        agreement, created = Agreement.objects.get_or_create(
            name=name,
            defaults=dict(
                amount=str(amount),
                d_from=d_from,
                c_to=c_to,))
        self.agreement = agreement
        self.d_from = d_from or agreement.d_from
        self.c_to = c_to or agreement.c_to
        exec(f"self.amount = amount or {agreement.amount}")
        # end agreement lookup

    def __call__(self, *args: Union[
        int, Decimal,
        'Transaction', List['Transaction']]) -> 'Transaction':

        for arg in args:
            if type(arg) == Transaction:
                self.sub_transactions.append(arg)

            elif type(arg) in (int, Decimal):
                self.amount = arg

        return self

    def calculate_amount(self, amnt):
        try:
            self.amount = self.amount(amnt)
        except TypeError:
            ...
        return self.amount

    def save(self):
        if not self.created_at:
            self.created_at = datetime.now()

        Ledger(
            created_at=self.created_at,
            amount=self.amount,
            d_from=self.d_from,
            c_to=self.c_to
        ).save()

        self._save_sub_transactions()

    def _save_sub_transactions(self):
        for transaction in self.sub_transactions:
            transaction.created_at = self.created_at
            transaction.amount = transaction.calculate_amount(self.amount)
            if not transaction.d_from:
                transaction.d_from = self.c_to
            transaction.save()
