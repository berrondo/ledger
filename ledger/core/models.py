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
        return _Transaction.objects.filter(
            to_=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def all_debits(self):
        return _Transaction.objects.filter(
            from_=self
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def balance(self):
        return self.all_credits() - self.all_debits()


class _Transaction(models.Model):
    created_at = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    from_ = models.ForeignKey(Account, on_delete=models.PROTECT)
    to_ = models.ForeignKey(Account, on_delete=models.PROTECT)


class Transaction:
    def __init__(self,
                 name: str,
                 created_at=None,
                 amount=None,
                 from_: Account=None,
                 to_: Account=None):

        self.name = name
        self.created_at = created_at
        self.amount = amount
        self.from_ = from_
        self.to_ = to_

        self.sub = None

    def __call__(self, transaction: 'Transaction'):
        self.sub = transaction
        return self

    def calculate_amount(self, amnt):
        try:
            self.amount = self.amount(amnt)
        except TypeError:
            ...
        return self.amount

    def save(self):
        t = _Transaction(
            created_at=self.created_at,
            amount=Decimal(self.amount),
            from_=self.from_,
            to_=self.to_
        ).save()

        if self.sub:
            self.sub = _Transaction(
                created_at=self.created_at,
                amount=self.sub.calculate_amount(self.amount),
                from_=self.to_,
                to_=self.sub.to_
            )
            self.sub.save()

        return t


class Journal:
    def __init__(self, *transactions: [Transaction]):
        self.transactions = transactions
        self.base = list(transactions).pop(0)
        self.name = self.base.name
        self.sub_transactions = transactions

    def __call__(self, amount):
        self._process_sub_transactions()
        self.base.amount = amount
        return self

    def _process_sub_transactions(self):
        for transaction in self.sub_transactions:
            if not transaction.from_:
                transaction.from_ = self.base.from_
            if not transaction.to_:
                transaction.to_ = self.base.to_

    def save(self):
        created_at = datetime.now()
        for transaction in self.transactions:
            transaction.created_at = created_at
            transaction.calculate_amount(self.base.amount)
            transaction.save()
