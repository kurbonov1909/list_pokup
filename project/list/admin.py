from django.contrib import admin
from .models import Store, Purchase, History

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('date', 'store', 'user', 'length', 'width', 'thickness', 'quantity', 'total_cost')
    list_filter = ('date', 'store', 'user')
    search_fields = ('store__name', 'user__username')
    ordering = ('-date',)
    readonly_fields = ('mass', 'sheet_price', 'total_cost')

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('get_timestamp', 'user', 'action', 'model_type', 'object_repr', 'ip_address')
    list_filter = ('action', 'model_type', 'user', 'timestamp')
    search_fields = ('user__username', 'object_repr', 'description', 'ip_address')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'ip_address', 'user_agent')
    
    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%d.%m.%Y %H:%M:%S')
    get_timestamp.short_description = 'Vaqt'
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('user', 'action', 'model_type', 'timestamp')
        }),
        ('Obekt ma\'lumotlari', {
            'fields': ('object_id', 'object_repr', 'description')
        }),
        ('Texnik ma\'lumotlar', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        # Faqat superuserlar tarixni ko'rishi mumkin
        return request.user.is_superuser
