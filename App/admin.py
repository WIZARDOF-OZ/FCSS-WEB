# from django.contrib import admin
# from .models import Dashboard, Banner, GalleryItem, About

# # For Configuration of tables
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('image_tag','title', 'add_date')
#     search_fields = ('title',)
    
# class DashboardAdmin(admin.ModelAdmin):
#     list_display = ('banner_title', 'add_date')
    
# # Register your models here.
# admin.site.register(Dashboard, DashboardAdmin)
# admin.site.register(Banner, CategoryAdmin)
# admin.site.register(GalleryItem)
# admin.site.register(About)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import Dashboard, Banner, GalleryItem, About
from App.models import NewsletterSubscriber

# Unregister default User and re-register with Unfold
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    pass


class CategoryAdmin(ModelAdmin):
    list_display = ('image_tag', 'title', 'add_date')
    search_fields = ('title',)


class DashboardAdmin(ModelAdmin):
    list_display = ('banner_title', 'add_date')


@admin.register(GalleryItem)
class GalleryItemAdmin(ModelAdmin):
    pass


@admin.register(About)
class AboutAdmin(ModelAdmin):
    pass


admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Banner, CategoryAdmin)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
