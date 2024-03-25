from django.contrib import admin

from .models import Book, Status, HistoryMove


@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year',
        'author',
        'is_taken',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'year',
        'author',
    )
    list_editable = (
        'year',
        'author',
    )
    search_fields = (
        'title',
    )
    list_per_page = 10


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'taken_at',
        'returned_at',
    )


@admin.register(HistoryMove)
class HistoryMoveAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'user',
        'action',
        'action_date',
    )
