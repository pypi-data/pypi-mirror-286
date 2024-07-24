from __future__ import annotations

from django.apps import AppConfig


class ProgressConfig(AppConfig):
    name = "isup.extensions.progress"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Прогресс"
