from django.contrib import admin

from blogelements.models import Article, Comment


# Register your models here.


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Article, PostAdmin)
