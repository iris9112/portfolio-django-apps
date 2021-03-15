from django.contrib import admin
from todo_app.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "complete", "description", "created_at"]

    readonly_fields = ["id", "created_at"]

    search_fields = ["user__username", "complete", "description"]
