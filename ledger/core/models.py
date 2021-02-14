from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.datetime_safe import datetime


class Percentual:
    def __init__(self, percentual):
        self.percentual = percentual / 100

    def __call__(self, amount):
        return self.percentual * amount


class Account(models.Model):
    def all_credits(self):
        return Transaction.objects.filter(
            credit_to=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def all_debits(self):
        return Transaction.objects.filter(
            debit_from=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def balance(self):
        return self.all_credits() - self.all_debits()


class Transaction(models.Model):
    created_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    debit_from = models.ForeignKey(Account, on_delete=models.PROTECT)
    credit_to = models.ForeignKey(Account, on_delete=models.PROTECT)


class Journal:
    def __init__(self, *transactions):
        self.transactions = transactions
        self.base = list(transactions).pop(0)
        self.sub_transactions = transactions

    def __call__(self, amount):
        self._process_sub_transactions()
        self.base.amount = amount
        return self

    def _process_sub_transactions(self):
        for transaction in self.sub_transactions:
            if not hasattr(transaction, 'debit_from'):
                transaction.debit_from = self.base.debit_from
            if not hasattr(transaction, 'credit_to'):
                transaction.credit_to = self.base.credit_to

    def save(self):
        created_at = datetime.now()
        for transaction in self.transactions:
            transaction.created_at = created_at
            transaction.save()
