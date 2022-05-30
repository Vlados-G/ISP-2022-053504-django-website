from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from .models import Category, Actor, Rating, RatingStar, Reviews, Genre, Movie, MovieShots

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInLine(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("show_image",)

    def show_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" heigt="110"')

    show_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    readonly_fields = ("show_image",)
    actions = ["publish", "unpublish"]
    list_editable = ("draft",)
    fieldsets = (
        ("Head", {
            "fields": (("title", "tagline"),)
        }),
        ("View", {
            "fields": ("description", ("poster", "show_image"))
        }),
        ("Date", {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        ("Money", {
            "classes": ("collapse",),
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def show_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" heigt="110"')

    show_image.short_description = "Постер"

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    show_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "show_image")
    readonly_fields = ("show_image",)

    def show_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" heigt="60"')

    show_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "show_image")
    readonly_fields = ("show_image",)

    def show_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" heigt="60"')

    show_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = "Site of Movies"
admin.site.site_header = "Site of Movies"