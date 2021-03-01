class Percentual:
    def __init__(self, percentual):
        self._percentual = percentual
        self.percentual = percentual / 100

    def __call__(self, amount):
        return self.percentual * amount

    def __repr__(self):
        return f'{self.__class__.__name__}({self._percentual})'

    def __eq__(self, other):
        return str(self) == str(other)
