from django.contrib import admin
from core.models import Post, Bookshelf, BookExchangePartner, BookExchangeRequest, Comment, Event, ReplyComment, Notification, EventPost, Page

# Register your models here.
class BookshelfAdminTab(admin.TabularInline):
    model = Bookshelf

class PostAdmin(admin.ModelAdmin):
    inlines = [BookshelfAdminTab]
    list_editable = ['active']
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    prepopulated_fields = {"slug": ("title", )}


class BookshelfAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['thumbnail', 'post', 'active']
    # prepopulated_fields = {"slug": ("title", )}


class BookExchangeRequestAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['sender', 'receiver', 'status']

class PartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'partner']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'active']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'active']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'sender', 'post', 'comment', 'is_read']


class EventPostTabAdmin(admin.TabularInline):
    model = EventPost

class EventAdmin(admin.ModelAdmin):
    # inlines = [GroupPostTabAdmin]
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name', 'visibility']
    prepopulated_fields = {"slug": ("name", )}


class PageAdmin(admin.ModelAdmin):
    # inlines = [GroupPostTabAdmin]
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name', 'visibility']
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Post, PostAdmin)
admin.site.register(Bookshelf, BookshelfAdmin)
admin.site.register(BookExchangeRequest, BookExchangeRequestAdmin)
admin.site.register(BookExchangePartner, PartnerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPost)
