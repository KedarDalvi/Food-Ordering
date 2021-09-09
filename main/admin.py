from django.contrib import admin
from .models import detail,MenuItem,Order,Category

class Admindetail(admin.ModelAdmin):
    list_display=['user','phone_no' ,'address']
    search_fields = ('user__username','phone_no' ,'address',)
    readonly_fields=()
    filter_horizontal =()
    list_filter=()
    fieldsets = ()

class AdminMenuItem(admin.ModelAdmin):
    list_display=['name','price' ,'category','image','id']
    search_fields = ('name','price' ,'category__name','image','id')
    readonly_fields=()
    filter_horizontal =()
    list_filter=()
    fieldsets = ()


class AdminOrderItem(admin.ModelAdmin):
    list_display=['user','username','name','phone_no','address','item_name','quantity','price','ordered_date']
    search_fields = ('username','address','phone_no','name','item__name','quantity','price','ordered_date' )
    readonly_fields=()
    filter_horizontal =()
    list_filter=()
    fieldsets = ()


admin.site.register(detail,Admindetail)
admin.site.register(MenuItem,AdminMenuItem)
admin.site.register(Order,AdminOrderItem)
admin.site.register(Category)


