from django.shortcuts import render
from ..theme_package.common_theme import CommonTheme


def e_show_money_arrange(request):
    return render(request, '04_money_arrange/04_money_arrange.html', {'theme': CommonTheme.dark_theme})


def e_show_ledger_detail(request):
    return render(request, '04_money_arrange/04a_ledger_detail.html', {'theme': CommonTheme.dark_theme})
