class Percentual:
    def __init__(self, percentual):
        self._percentual = percentual
        self.percentual = percentual / 100

    def __call__(self, amount):
        return self.percentual * amount

    def __repr__(self):
        return f'Percentual({self._percentual})'

    def __eq__(self, other):
        return self.percentual == other.percentual