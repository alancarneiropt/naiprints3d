import os

from django.conf import settings
from django.http import JsonResponse


class DatabaseAvailabilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.REQUIRE_SQLITE_FILE and not os.path.isfile(settings.SQLITE_PATH):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Base de dados SQLite nao encontrada. Acesso bloqueado.",
                },
                status=503,
            )
        return self.get_response(request)
