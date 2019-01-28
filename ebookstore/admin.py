from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category,Product,Stores,Cart,UserProfile,CartItem,Variation, Order, Comment,Complain,Saleontelestai


admin.site.register(Category)

admin.site.register(Stores)
admin.site.register(UserProfile)
admin.site.register(Comment) 
admin.site.register(Complain) 
admin.site.register(Saleontelestai)




class CartItemTabularInline(admin.TabularInline):
	model =CartItem

admin.site.register(CartItem)	



class CartAdmin(admin.ModelAdmin):
	inlines = [CartItemTabularInline]
	class meta:
		model = Cart

admin.site.register(Cart,CartAdmin)




admin.site.register(Order)






class VariationTabularInline(admin.TabularInline):
	model =Variation

admin.site.register(Variation)



class ProductAdmin(admin.ModelAdmin):
	inlines = [VariationTabularInline]
	class meta:
		model = Product

admin.site.register(Product,ProductAdmin)





