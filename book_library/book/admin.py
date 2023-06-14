from django.contrib import admin
from book.models import Book, Author, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'remains')
    search_fields = ('title',)
    filter_horizontal = ('author', 'genre',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_day',)
    empty_value_display = '-пусто-'


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
