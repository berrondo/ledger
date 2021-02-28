from django.contrib import admin
from .models import (
    Account,
    Agreement,
    Ledger,
)


admin.site.register(Account)
admin.site.register(Agreement)
admin.site.register(Ledger)
