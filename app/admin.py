from django.contrib import admin
from .models import Booking, Gallery, Video, Profile


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "event_type",
        "event_date",
        "status",
        "phone",
    )

    list_filter = (
        "status",
        "event_type",
        "event_date",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "user__username",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "user__username",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
    )

    search_fields = (
        "user__username",
        "phone",
    )