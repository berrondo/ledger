from decimal import Decimal


class Calculation:
    def __eq__(self, other):
        return str(self) == str(other)


class Percentual(Calculation):
    def __init__(self, percentual):
        self._percentual = percentual
        self.percentual = percentual / 100

    def __call__(self, transaction: 'Transaction'):
        return self.percentual * transaction.amount

    def __repr__(self):
        return f'{self.__class__.__name__}({self._percentual})'


class SalarioMinimo(Calculation):
    def __call__(self, transaction: 'Transaction'):
        # date = self.transaction.created_at
        return Decimal(1100)

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class IRRF(Calculation):
    def _table(self, amount: Decimal):
        if amount < Decimal(1903.99):
            return 0, 0
        if amount < Decimal(2826.65):
            return .075, 142.8
        return .275, 869.36

    def __call__(self, transaction: 'Transaction'):
        amount = transaction.amount
        percentual, deduction = self._table(amount)
        return (amount * Decimal(percentual)) - Decimal(deduction)

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class INSS(Calculation):
    MAX = 707.6927

    def __call__(self, transaction: 'Transaction'):
        amount = transaction.amount
        percentual = Decimal('0.11')
        inss = amount * percentual
        return Decimal(min(inss, self.MAX))

    def __repr__(self):
        return f'{self.__class__.__name__}()'
