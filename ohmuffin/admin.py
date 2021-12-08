from django.contrib import admin

from ohmuffin.models import Interest, Profile


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    """Interest admin model"""

    search_fields = [
        "name",
    ]

    list_display = [
        "id",
        "name",
        "created",
        "modified",
    ]

    fieldsets = [
        ("ID", {"fields": ["id"]}),
        ("System dates", {"fields": ["created", "modified"]}),
        ("Information", {"fields": ["name"]}),
    ]

    readonly_fields = ["id", "created", "modified"]

    # Custom fields

    # Overrides


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin model"""

    search_fields = [
        "first_name",
        "last_name",
        "slack_id",
    ]

    list_display = [
        "id",
        "first_name",
        "last_name",
        "slack_id",
        "created",
        "modified",
    ]

    fieldsets = [
        ("ID", {"fields": ["id"]}),
        ("System dates", {"fields": ["created", "modified"]}),
        ("Information", {"fields": ["first_name", "last_name", "slack_id"]}),
        ("Interests", {"fields": ["interests"]}),
    ]

    readonly_fields = ["id", "created", "modified"]

    # Custom fields

    # Overrides
