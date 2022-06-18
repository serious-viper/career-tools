from django.contrib import admin
from main.models import Cutoff
# Register your models here.

@admin.register(Cutoff)
class CutoffAdmin(admin.ModelAdmin):
    list_filter = ("round",)