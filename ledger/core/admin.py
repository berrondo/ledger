from django.contrib import admin
from .models import (
    Account,
    Schema,
    Ledger,
)


admin.site.register(Account)
admin.site.register(Schema)
admin.site.register(Ledger)
