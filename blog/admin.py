from django.contrib import admin
from .models import Category, Post, Comment

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at')
    list_filter = ('published', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"
