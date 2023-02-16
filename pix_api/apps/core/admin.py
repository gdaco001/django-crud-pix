from django.contrib import admin

from .models import Receiver, Bank, BankAccount

admin.site.register([Receiver, Bank, BankAccount])
