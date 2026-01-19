"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.urls import re_path
from django.views.generic.base import RedirectView

# self define function locations
from .e__money_arrange import e_show_money_arrange, e_get_money_positions, \
    e_add_money_record, e_add_money_transfer_record, e_money_get_chart01_data, e_money_get_chart02_data, \
    e_money_get_chart03_data, e_money_get_chart_history01_data, e_get_money_record, e_modify_money_record, \
    e_delete_money_record, e_modify_money_transfer_record, e_upload_bill, \
    e_upload_money_records, e_search_money_record_form, e_get_ledgers, e_add_ledger, \
    e_modify_record_ledger, e_get_last_archive_time, e_do_money_archive, e_auto_complete_rule, \
    e_get_next_to_be_checked_money_record

from .z__common import z_login, z_get_select_list, z_get_quotation, z_stream_video, z_check_secret_order, z_storage_list


url_names = [
    # 04_money_arrange
    ('04money_arrange', e_show_money_arrange.e_show_money_arrange),
    ('04a_ledger_detail', e_show_money_arrange.e_show_ledger_detail),
    ('e_get_money_positions', e_get_money_positions.e_get_money_positions),
    ('e_search_money_record_form', e_search_money_record_form.e_search_money_record_form),
    ('e_add_money_record', e_add_money_record.e_add_money_record),
    ('e_get_money_record', e_get_money_record.e_get_money_record),
    ('e_modify_money_record', e_modify_money_record.e_modify_money_record),
    ('e_modify_money_transfer_record', e_modify_money_transfer_record.e_modify_money_transfer_record),
    ('e_delete_money_record', e_delete_money_record.e_delete_money_record),
    ('e_add_money_transfer_record', e_add_money_transfer_record.e_add_money_transfer_record),
    ('e_money_get_chart01_data', e_money_get_chart01_data.e_money_get_chart01_data),
    ('e_money_get_chart02_data', e_money_get_chart02_data.e_money_get_chart02_data),
    ('e_money_get_chart03_data', e_money_get_chart03_data.e_money_get_chart03_data),
    ('e_money_get_chart_history01_data', e_money_get_chart_history01_data.e_money_get_chart_history01_data),
    ('e_upload_bill', e_upload_bill.e_upload_bill),
    ('e_upload_money_records', e_upload_money_records.e_upload_money_records),
    ('e_get_ledgers', e_get_ledgers.e_get_ledgers),
    ('e_add_ledger', e_add_ledger.e_add_ledger),
    ('e_modify_record_ledger', e_modify_record_ledger.e_modify_record_ledger),
    ('e_get_last_archive_time', e_get_last_archive_time.e_get_last_archive_time),
    ('e_do_money_archive', e_do_money_archive.e_do_money_archive),
    ('e_auto_complete_rule', e_auto_complete_rule.EAutoCompleteRule.as_view()),
    ('e_get_next_to_be_checked_money_record', e_get_next_to_be_checked_money_record.e_get_next_to_be_checked_money_record),

    # common 部分
    ('z_get_select_list', z_get_select_list.z_get_select_list),
    ('z_get_quotation', z_get_quotation.z_get_quotation),
    ('z_stream_video', z_stream_video.z_stream_video),
    ('z_check_secret_order', z_check_secret_order.z_check_secret_order),
    ('z_storage_list', z_storage_list.z_storage_list),
    ('z_login', z_login.z_login_view),
    ('z_logout', z_login.z_logout_view),
]

urlpatterns = [
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),  # 允许 /media/ 路径访问
    path('favicon.ico', RedirectView.as_view(url=r'static/images/favicon.ico')),     # 网页图标
    path('', e_show_money_arrange.e_show_money_arrange),                             # 默认首页

] + [path(url_name+'/', url_view, name=url_name) for url_name, url_view in url_names]
