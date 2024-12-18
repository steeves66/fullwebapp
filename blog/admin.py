from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.core import paginator
from django.utils.functional import cached_property
from blog import models


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False


class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'word_count', 'author_full_name']
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    # raw_id_fields = ('author',)   # For the big table, disable dropdown foreign key and replace it by text field
    list_select_related = ['author']    # For avoid N+1 issue without custom get_queryset in list_display attribute
    paginator = CustomPaginator

    def word_count(self, obj):
        return obj.content.split()
    
    def author_full_name(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'
    
    actions = ('print_blogs_titles',)
    @admin.action(description='Prints title')
    def print_blogs_titles(self, request, queryset):
        for data in queryset.all():
            print(data.title)
    
    # Use for avoid N+1 issue
    # def get_queryset(self, request):
    #     default_qs = super().get_queryset(request)
    #     improved_qs = default_qs.select_related('author')
    #     return improved_qs

# Register your models here.
admin.site.register(models.Blog, BlogAdmin)