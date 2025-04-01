import sqlite3
import hashlib
from django.http import JsonResponse


def check_secret_order(secret_order):

    if not secret_order:
        return False

    m = hashlib.md5()
    m.update(secret_order.encode('utf-8'))

    # 创建数据库连接
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute(""" select value from z_settings where key = 'secret_order_encrypted'; """)
    secret_order_encrypted = cur.fetchone()[0]

    # 关闭数据库连接
    cur.close()
    conn.close()

    if m.hexdigest() == secret_order_encrypted:
        return True

    return False


def z_check_secret_order(request):
    secret_order = request.POST.get('secret_order')

    if check_secret_order(secret_order):
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)
