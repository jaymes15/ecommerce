
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth import get_user_model

from django.db.models.signals import post_save
from django.db.models.signals import pre_save,post_save,m2m_changed





# Create your models here.




'''

class CartManager(models.Manager):
	def get_or_create():
		return obj, True
	def new_or_get(self,request):	




			cart_id = request.session.get("cart_id",None)
			qs = self.get_queryset().filter(id=cart_id)
			if qs.count() == 1:
				new_obj = False
				cart_obj = qs.first()
				if request.user.is_authenticated and cart_obj.user is None:
					cart_obj.user = request.user
					cart_obj.save()
			else:
				cart_obj = Cart.objects.new(user=request.user)
				new_obj = True
				request.session['cart_id'] = cart_obj.id
				return cart_obj , new_obj







	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)



class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True,  on_delete=models.CASCADE)
	products = models.ManyToManyField('Product', blank=True)
	subtotal=models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)





def m2m_changed_cart_receiver(sender, instance,action, *args, **kwargs):
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
			products = instance.products.all()
			total = 0
			for x in products:
				total += x.Product_price
			instance.subtotal = total
			instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
	instance.total = instance.subtotal
pre_save.connect(pre_save_cart_receiver, sender=Cart)					

'''
class CartItem(models.Model):
	cart = models.ForeignKey('Cart',  null=True, blank=True,  on_delete=models.CASCADE)
	product = models.ForeignKey('Product',on_delete=models.CASCADE)
	order = models.ForeignKey('Order',  null=True, blank=True,  on_delete=models.CASCADE)

	#store = models.ForeignKey('Stores',on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)

	variations = models.ManyToManyField('Variation',null=True,blank=True)
	quantity = models.PositiveIntegerField(default=1)
	line_total =models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	price =models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		try:
		 	return str(self.cart.id)
		except:
			return self.product.title 	




class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True,  on_delete=models.CASCADE)
	#item = models.ManyToManyField('CartItem', blank=True, null=True,related_name='tem')
	#product = models.ManyToManyField('Product', blank=True, null=True,related_name='tem')
	subtotal=models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	total = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	profile = models.ForeignKey('UserProfile', null=True, blank=True,  on_delete=models.CASCADE)

	#objects = CartManager()

	def __str__(self):
		return str(self.id)


		


class Category(models.Model):
	name = models.CharField(max_length=300)
	slug = models.SlugField(unique=True,max_length=250)


	def __str__(self):
		return self.name

	

	def get_absolute_url(self):
		return reverse('booklibrary:post_by_category', args=[self.slug])




class Stores(models.Model):
	Store_name = models.CharField(max_length=300)
	Store_description = models.TextField()
	Store_email = models.EmailField(max_length=500)
	Store_location = models.CharField(max_length=700)
	Store_logo =  models.ImageField(null=True,blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)




	def __str__(self):
		return self.Store_name

	
	
	



	

class Product(models.Model):
	Product_name = models.CharField(max_length=250)
	Product_decription = models.TextField()
	Product_image = models.ImageField()
	Product_image1 = models.ImageField(null=True,blank=True)
	Product_image2 = models.ImageField(null=True,blank=True)
	Product_image3 = models.ImageField(null=True,blank=True)
	Product_image4 = models.ImageField(null=True,blank=True)
	Product_price = models.DecimalField(decimal_places=2,max_digits=10)
	likes = models.ManyToManyField(User,related_name='likes',blank=True)
	favourite = models.ManyToManyField(User,related_name='favourite',blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)

	Product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	#Product_store = models.ForeignKey(Stores,on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True,blank=True,null=True)


	

	def total_likes(self):
	        		return self.likes.count()	

	def __str__(self):
		return self.Product_name





class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=6,choices=(('Male','Male'),('Female','Female')),blank=True)
	age = models.PositiveIntegerField(blank=True,null=True)
	address = models.CharField(max_length=2000,default='')
	location = models.CharField(max_length=2000,default='',null=False,blank=False)
	city = models.CharField(max_length=100,default='')
	phone_number = models.CharField(max_length=16,default='')
	order = models.ForeignKey('Order', null=True, blank=True,  on_delete=models.CASCADE)

	#website = models.URLField(default='')
	image = models.ImageField(upload_to='profile_image',blank=True,null=True)
	def __str__(self):
		return self.user.username


	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'	








def create_profile(sender,**kwargs):
	if kwargs ['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)



class VariationManager(models.Manager):
	def  sizes(self):
		return super(VariationManager, self).filter(category='size')
	def colors(self):
		return super(VariationManager, self).filter(category='color')



VAR_CATEGORIES = (
	('size','size'),
	('color','color'),
	)

class Variation(models.Model):
	category = models.CharField(max_length=120,choices=VAR_CATEGORIES,default='size')
	title = models.CharField(max_length=120)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	#store = models.ForeignKey(Stores,on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)


	objects = VariationManager()


	
	def __str__(self):
		return "%s " %(self.title)	


User = get_user_model()
STATUS_CHOICES = (
	("Started","started"),
	("Seen","seen"),
	("Abandoned","Abandoned"),
	("Finished", "Finished"),



		)


class Order(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	#item_ordered =  models.ForeignKey(CartItem,on_delete=models.CASCADE,null=True)
	#user_profile =  models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
	delivery_address = models.CharField(max_length=2000,default='',null=False,blank=False)
	delivery_location = models.CharField(max_length=2000,default='',null=False,blank=False)
	
	telephone_number =models.CharField(max_length=16,default='')
	order_id = models.CharField(max_length=120,default='ABC', unique=True)
	cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
	status = models.CharField(max_length=120, choices=STATUS_CHOICES,default='started')
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return "%s, %s" %(self.order_id,self.status)	



class Comment(models.Model): 

	name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
	
	text = models.TextField() 
	product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments') 
	created_on = models.DateTimeField(auto_now_add=True)
	

	
	def __str__(self):
		return "%s said %s for %s"  %(self.name,self.text,self.product)

class Complain(models.Model): 

	name = models.CharField(max_length=2000)
	telephone_number =models.CharField(max_length=16,default='')
	email = models.EmailField(max_length=500,blank=True,null=True)
	
	text = models.TextField() 
	 
	created_on = models.DateTimeField(auto_now_add=True)
	

	
	def __str__(self):
		return "%s"  %(self.name)


class Saleontelestai(models.Model):
	name = models.CharField(max_length=2000)
	store_name= models.CharField(max_length=2000)
	address = models.CharField(max_length=2000)
	Email = models.EmailField(max_length=500)
	telephone_number= telephone_number =models.CharField(max_length=16,default='')
	product_category=models.CharField(max_length=2000)



	def __str__(self):
		return "%s"  %(self.name)





