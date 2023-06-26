from django.contrib import admin


from core.models import Transaction
admin.site.site_header = "Bank Admin"
admin.site.site_title = "Bank Admin Portal"
admin.site.register(Transaction)