# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages

from planet.models import (Blog, Generator, Feed, FeedLink, Post, PostLink,
    Author, PostAuthorData, Enclosure)

from django.shortcuts import redirect
from django.core import management

# NEW
from django.core.exceptions import ValidationError


class PostLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "rel", "mime_type", "post", "link")
    list_filter = ("rel", "mime_type")

admin.site.register(PostLink, PostLinkAdmin)


class PostAuthorDataAdmin(admin.ModelAdmin):
    list_display = ("author", "is_contributor", "post")
    list_filter = ("is_contributor", "author")

admin.site.register(PostAuthorData, PostAuthorDataAdmin)


class EnclosureAdmin(admin.ModelAdmin):
    list_display = ("post", "mime_type", "length", "link")
    list_filter = ("mime_type", )

admin.site.register(Enclosure, EnclosureAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "blog", "language", "generator")
    list_filter = ("language", "generator", )
    fieldsets = (
        (None, {'fields': ('url',)}),
        ('Extras', {'fields': ('blog', 'site', 'title', 'subtitle', 'rights', 'generator', 'info', 'language', 'guid', 'icon_url', 'image_url', 'etag', 'last_modified', 'last_checked', 'is_active')}),
    )

    # overrides the add_view so that the add_feed management command is execute with the url given.
    def add_view(self, request, form_url='', extra_context={}):
        if request.method == 'POST':
            try:
                management.call_command('add_feed', request.POST.get('url'))
                request.user.message_set.create(message="Feed was added successfully.")
            except ValidationError, e:
                pass # how do we show the custom validation error message?
                
            return redirect('admin:planet_feed_changelist')
        return super(FeedAdmin, self).add_view(request, form_url, extra_context)

admin.site.register(Feed, FeedAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email")

admin.site.register(Author, AuthorAdmin)

class EnclosureInline(admin.StackedInline):
    model = Enclosure
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "feed", "url")
    list_filter = ("feed", )
    # filter_horizontal = ('tags',)

admin.site.register(Post, PostAdmin, inlines=[EnclosureInline])


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "url")

admin.site.register(Blog, BlogAdmin)


class GeneratorAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "link")

admin.site.register(Generator, GeneratorAdmin)


class FeedLinkAdmin(admin.ModelAdmin):
    list_display = ("feed", "mime_type", "rel", "link")
    list_filter = ("mime_type", "rel")

admin.site.register(FeedLink, FeedLinkAdmin)