"""
ASGI config for HelloWorld project.

It exposes the ASGI callable as a module-level variable named ``application``.
一个 ASGI 兼容的 Web 服务器的入口，以便运行你的项目

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.settings')

application = get_asgi_application()
