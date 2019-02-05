from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .models import Product,Category,Stores,Cart,CartItem,Variation,Order,Comment,UserProfile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .forms import RegistrationForm,EditProfileForm, UserUpdateForm, orderinformation,CommentForm,ComplainForm,SaleontelestaiForm,PostForm,VariationForm

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.urls import reverse
import time
from django.db.models import Q
from django.http import HttpResponseRedirect
from .utils import id_generator
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#from django.views.generic.list import ListView 
# Create your views here.


def confirmcomplain(request):
	cat = Category.objects.all()

	context = {'category':cat}
			
	return render(request,'ebookstore/home.html',context)

def confirmsalesrequest(request):
	cat = Category.objects.all()

	context = {'category':cat}
			
	return render(request,'ebookstore/confirmsalesrequest.html',context)




def complain(request):

	cat = Category.objects.all()
	if request.method == 'POST':
				
				p_form =ComplainForm(request.POST)
				
				

				if p_form.is_valid()   :
						p_form.save()
						
						
						return redirect('ebookstore:confirmcomplain')
	else:
			
			p_form =  ComplainForm()
			
			context = {'p_form':p_form,'category':cat}
			
			return render(request,'ebookstore/homepage.html',context)

def Salesrequest(request):

	cat = Category.objects.all()
	if request.method == 'POST':
				
				p_form =SaleontelestaiForm(request.POST)
				
				

				if p_form.is_valid()   :
						p_form.save()
						
						
						return redirect('ebookstore:confirmsalesrequest')
	else:
			
			p_form =  SaleontelestaiForm()
			
			context = {'p_form':p_form,'category':cat}
			
			return render(request,'ebookstore/Salesrequest.html',context)			

'''
class ProductList(ListView):
	queryset = Product.objects.all()
	template_name = 'ebookstore/productdetail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductList, self).get_context_data(*args, **kwargs)
		print(context)
		return context

'''

def carthome(request):
	cat = Category.objects.all()
	try:
		the_id=request.session['cart_id']
		cart= Cart.objects.get(id=the_id)
		cartitem=CartItem.objects.get(id=the_id)
	except:
		the_id = None
	if the_id:		
		
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total = float(item.product.Product_price) * item.quantity
			new_total += line_total
			
			

		request.session['items_total'] = cart.cartitem_set.count()	
		cart.total = new_total
		
		cartitem.save()
		cart.save()	
		context = {'bas':cart,'category':cat}
	else:
		empty_message = 'Your cart is Empty,Please keep shopping.'
		context = {'empty':True,'empty_message':empty_message,'category':cat }	
	#return render(request,'ebookstore/carthome.html')
	'''
	cart_id = request.session.get("cart_id",None)
	qs = Cart.objects.filter(id=cart_id)
	if qs.count() == 1:
		cart_obj = qs.first()
		if request.user.is_authenticated() and cart_obj.user is None:
			cart_obj.user = request.user
			cart_obj.save()
	else:
		cart_obj = Cart.objects.new(user=request.user)
		request.session['cart_id'] = cart_obj.id
		'''
	return render(request,'ebookstore/carthome.html',context)


def add_to_cart(request,id):
	request.session.set_expiry(604800)
	try:
		the_id=request.session['cart_id']
	except:
		   new_cart = Cart()
		   new_cart.save()
		   request.session['cart_id'] = new_cart.id
		   the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)
	try:
		product = Product.objects.get(id=id)

	except Product.DoesNotExist:
		pass
	except:
		pass


	product_var =[] #product variation
	if request.method == 'POST':
			qty = request.POST['qty']

			for item in request.POST:
				key = item
				val = request.POST[key]
				try:
					v = Variation.objects.get(product=product,category__iexact=key, title__iexact=val)
					product_var.append(v)
				except:
					pass

			cart_item = CartItem.objects.create(cart=cart,product=product)
			if len(product_var) > 0:
				cart_item.variations.add(*product_var)

			for item in cart.cartitem_set.all():
			    store = item.product.user
			    price = item.product.Product_price

			cart_item.quantity = qty
			cart_item.user = store
			cart_item.price = price
			cart_item.save()

			#if	not cart_item in cart.items.all():
			#	cart.items.add(cart_item)
			#else:
				#cart.items.remove(cart_item)

			return HttpResponseRedirect(reverse('ebookstore:carthome'))

	else:
		return HttpResponseRedirect(reverse('ebookstore:carthome'))
def remove_from_cart(request,id):
	try:
		the_id=request.session['cart_id']
		cart= Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse('ebookstore:carthome'))		

	cartitem = CartItem.objects.get(id=id)
	#cartitem.delete()
	cartitem.cart =None
	cartitem.save()
	return HttpResponseRedirect(reverse('ebookstore:carthome'))		

			
		
		

'''
	try:
		qty = request.GET.get('qty')
		update_qty = True

	except:
		qty = None
		update_qty = False	



	try:
		attr = request.GET.get('attr')
	except:
		attr = None		
	
	try:
		the_id=request.session['cart_id']
	except:
		   new_cart = Cart()
		   new_cart.save()
		   request.session['cart_id'] = new_cart.id
		   the_id = new_cart.id
	cart = Cart.objects.get(id=the_id)	   
	try:
		product = Product.objects.get(id=id)
	except Product.DoesNotExist:
		pass
	except:
		pass
	cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)	
	if qty and update_qty:
		if int(qty) <= 0:
			cart_item.delete()
		else:
			cart_item.quantity = qty
			cart_item.save()
	else:
		pass	
	#if	not cart_item in cart.items.all():
	#	cart.items.add(cart_item)
	#else:
		#cart.items.remove(cart_item)

	new_total = 0.00
	for item in cart.cartitem_set.all():
		line_total = float(item.product.Product_price) * item.quantity
		new_total += line_total
	request.session['items_total'] = cart.cartitem_set.count()	
	cart.total = new_total
	cart.save()	
	return HttpResponseRedirect(reverse('ebookstore:carthome'))		

'''

def loginredirect(request):
	if request.user.is_authenticated():
		user_groups = request.user.groups.values_list('name', flat=True)
		if request.user.is_superuser:
			return HttpResponseRedirect(reverse("admin"))
		elif "vendor" in user_groups:
			return HttpResponseRedirect(reverse('ebookstore:vendorhome'))
		elif not request.user in user_groups:
			return HttpResponseRedirect(reverse('ebookstore:displaycategory'))		




class ProductDetail(DetailView):
	
	template_name = 'ebookstore/productdetail.html'
	def get(self,request,pk):
		text = Comment.objects.filter(product_id= pk).order_by('-created_on')
		model = Product
		obj = Product.objects.get(pk=pk)
		cat = Category.objects.all()
		is_liked = False
		is_favourite =False
		if obj.likes.filter(id=request.user.id).exists():
			is_liked =True
		if obj.favourite.filter(id=request.user.id).exists():
			is_favourite =True

	
			
		context =    {'text':text,'obj':obj,'is_liked':is_liked,'total_likes':obj.total_likes(),'is_favourite':is_favourite,'category':cat}
		return render(request, self.template_name, context)



def display_category(request):
	cat = Category.objects.all().order_by('name')
	cate = UserProfile.objects.all()
	prod = Product.objects.all()
	query = request.GET.get('q')
	if query:
		prod = prod.filter(Q(Product_name__icontains=query)|
						   Q(Product_price__icontains=query)|
						   Q(Product_decription=query)
						   
						   )

	
	
	context = {'category':cat,'stores':cate,'prod':prod}
	return render(request,'ebookstore/displaycategory.html',context)

def display_percategory(request,id):
	text = Product.objects.filter(Product_category_id=id).order_by('-created_on')
	cat = Category.objects.all()
	sub =  Category.objects.filter(id=id)
	
	query = request.GET.get('q')
	if query:
		text = text.filter(Q(Product_name__icontains=query)|
						   Q(Product_price__icontains=query)|
						   Q(Product_decription=query)
						   )

	
	paginator = Paginator(text,20)		
	page = request.GET.get('page')
	#text = paginator.get_page(page)
	try:
		text = paginator.page(page)
	except PageNotAnInteger:
			text = paginator.page(1)
	except EmptyPage:
			text = paginator.page(paginator.num_page)
 


	context = {'product_cat': text,'category':cat,'cot': sub,'page':page}
	return render(request, 'ebookstore/display_percategory.html', context)

def display_stores(request):
	cat = Stores.objects.all()
	context = {'stores':cat }
	return render(request,'ebookstore/displaystores.html',context)

def display_perstores(request,id):
	text = Product.objects.filter(user_id=id).order_by('-created_on')
	cat = Category.objects.all()
	sub =  UserProfile.objects.filter(id=id)
	query = request.GET.get('q')
	if query:
		text = text.filter(Q(Product_name__icontains=query)|
						   Q(Product_price__icontains=query)|
						   Q(Product_decription=query)
						   )

	paginator = Paginator(text,20)		
	page = request.GET.get('page')
	#text = paginator.get_page(page)
	try:
		text = paginator.page(page)
	except PageNotAnInteger:
			text = paginator.page(1)
	except EmptyPage:
			text = paginator.page(paginator.num_page)

	context = {'product_cat': text,'category':cat,'cot': sub,'page':page}
	return render(request, 'ebookstore/display_perstore.html', context)	


def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:	

				return redirect('ebookstore:login')

	else:
		form = UserCreationForm()
		
	return render(request,'ebookstore/signup.html',{'form':form})



def login_view(request):
	if request.method =='POST':
		p_form = AuthenticationForm(data=request.POST)
		if p_form.is_valid():
			#Log user in
			user = p_form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:	

				return redirect('ebookstore:displaycategory')



	else:
		p_form = AuthenticationForm()
	return render(request,'ebookstore/login.html',{'p_form':p_form})



        
	# your sign up logic goes here

def logout_view(request):
	if request.method =='POST':
		logout(request)
		return redirect('ebookstore:login')

		
#@login_required(login_url="login/")
@login_required(login_url="/login/")
def profile(request,pk=None):
	cat = Category.objects.all()
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user = request.user

	args = {'user':user,'category':cat}
	return render(request,'ebookstore/profile.html',args)





@login_required(login_url="/login/")
def edit_profile(request):
		cat = Category.objects.all()
		if request.method == 'POST':
				
				p_form = EditProfileForm(request.POST, instance=request.user)
				u_form = UserUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
				

				if p_form.is_valid() and u_form.is_valid()  :
						p_form.save()
						u_form.save()
						
						return redirect('ebookstore:confirmorder')
		else:
			
			p_form =  EditProfileForm( instance=request.user)
			u_form =UserUpdateForm(instance=request.user.userprofile)
			context = {'p_form':p_form,'u_form':u_form,'category':cat}
			
			return render(request,'ebookstore/editprofile.html',context)






@login_required(login_url="/login/")
def checkout(request):
	cat = Category.objects.all()



	try:
		the_id =request.session['cart_id']
		cart = Cart.objects.get(id=the_id)

		user = request.user
	

	except:
		the_id = None
		return HttpResponseRedirect(reverse('ebookstore:carthome'))
	try:
		new_order = Order.objects.get(cart=cart)
		product =  CartItem.objects.get(cart=cart,product=product)
		
	except Order.DoesNotExist:
		new_order = Order()
		new_order.cart=cart
		
		new_order.delivery_location= user.userprofile.location
		new_order.delivery_address= user.userprofile.address
		new_order.telephone_number = user.userprofile.phone_number
		
		new_order.user = request.user
		#new_order.delivery_location = Order.delivery_location 
		
		new_order.order_id = str(time.time())
		

		
						
						
		new_order.save()
	except:
		return HttpResponseRedirect(reverse('ebookstore:carthome'))
			
	
	
	del request.session['cart_id']
	del request.session['items_total']

	
	context={'category':cat}

	template = 'ebookstore/checkout.html'
	return render(request,template,context)

def confirmorder(request):
	the_id=request.session['cart_id']
	cart= Cart.objects.get(id=the_id)
	cat = Category.objects.all()
	user = request.user
	
	
	
	context = {'bas':cart,'user':user,'category':cat}
	return render(request,'ebookstore/confirmorder.html',context)	




def like_products(request):
	obj = get_object_or_404(Product,id=request.POST.get('obj_id'))
	is_liked = False
	if obj.likes.filter(id=request.user.id).exists():
		obj.likes.remove(request.user)
		is_liked = False
	else:	
			obj.likes.add(request.user)
			is_liked = True
	return HttpResponseRedirect(obj.get_absolute_url())


	
@login_required(login_url="/login/")

def userfavourite_products(request):
	user = request.user
	favourite_posts = user.favourite.all()
	cat = Category.objects.all()


	paginator = Paginator(favourite_posts,20)		
	page = request.GET.get('page')
	#text = paginator.get_page(page)
	try:
		favourite_posts = paginator.page(page)
	except PageNotAnInteger:
			favourite_posts = paginator.page(1)
	except EmptyPage:
			favourite_posts = paginator.page(paginator.num_page)
	context ={'favourite_posts':favourite_posts,'category':cat,'page':page}
	return render(request,'ebookstore/userfavourite_products.html',context)
	
	#query = request.GET.get('q')
	#if query:
	  	 	#favourite_posts =favourite_posts.filter(Q(title__icontains=query)|
						  # Q(text__icontains=query)|
						   #Q(author__icontains=query)
						  
						   #)
'''
	paginator = Paginator( favourite_posts,24)
	page = request.GET.get('page')
	favourite_posts = paginator.get_page(page)
	try:
	  	 	 favourite_posts = paginator.page(page)
	except PageNotAnInteger:
	  	 	 favourite_posts = paginator.page(1)
	except EmptyPage:
		favourite_posts = paginator.page(paginator.num_page)
'''
 
	


@login_required(login_url="/login/")

def favourite_products(request,id):
	obj = get_object_or_404(Product,id=id)
	if obj.favourite.filter(id=request.user.id).exists():
		obj.favourite.remove(request.user)
	else:
			obj.favourite.add(request.user)
	return HttpResponseRedirect(obj.get_absolute_url())		






@login_required(login_url="/login/")
def add_comment(request,id):
	cat = Category.objects.all()
	product = get_object_or_404(Product,id=id)
	
	if request.method == 'POST':
			p_form = CommentForm(request.POST)
			if p_form.is_valid()  :
				comment=p_form.save(commit=False)
				comment.product = product
				comment.name = request.user
				comment.save()
				
				#return redirect(request.path) 
				return redirect('ebookstore:product_detail',pk=id)
	else:
			p_form = CommentForm()
			context = {'p_form':p_form,'category':cat}
			return render(request, 'ebookstore/addcomment.html', context)		

@login_required(login_url="/login/")
def change_password(request):
	cat = Category.objects.all()
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('ebookstore:userprofile')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'ebookstore/password_change.html',{'form': form,'category':cat})

@login_required(login_url="/login/")
def	add_post(request):
	
	if request.method =='POST':
		a_form = PostForm(request.POST,request.FILES)
		
		if a_form.is_valid():


			#save to db
			product= a_form.save(commit=False)
			product.user = request.user
			
			product.save()
			return redirect('ebookstore:displaycategory')
	else:
		a_form =  PostForm()
				
		return render(request, 'ebookstore/post_form.html',{ 'a_form':a_form })

@login_required(login_url="/login/")
def postbyuser(request,user_id):
	user =	 Product.objects.filter(user_id=user_id)

	
	context = {'user': user}
	return render(request, 'ebookstore/userprofile_form.html', context)		

class ProductUpdate(UpdateView): 
	model = Product
	fields = ['Product_name','Product_decription','Product_image','Product_image1','Product_image2','Product_image3','Product_image4','Product_category']	

class ProductDelete(DeleteView):
	model = Product 
	success_url = reverse_lazy('ebookstore:userprofile')	
@login_required(login_url="/login/")
def	add_variation(request,id):
	product = get_object_or_404(Product,id=id)
	if request.method =='POST':
		a_form = VariationForm(request.POST,request.FILES)
		
		if a_form.is_valid():
			com= a_form.save(commit=False)
			com.product = product
			com.save()
			return redirect('ebookstore:product_detail',pk=id)
	else:
		a_form =  VariationForm()
		return render(request, 'ebookstore/addvariation.html',{ 'a_form':a_form })	

@login_required(login_url="/login/")

def orders(request):
	order = Order.objects.all().order_by('-timestamp')
	query = request.GET.get('q')
	if query:
		order = order.filter(Q(status__icontains=query)|
						   Q(order_id__icontains=query)
						  
						   )
	context = {'order':order}
	return render(request, 'ebookstore/orders.html',context)





class OrderDetail(DetailView):
	model = Order
	template_name = "ebookstore/orderdetail.html"

@login_required(login_url="/login/")

def orderedcart(request,id):
	sub =  Cart.objects.get(id=id)
	context = {'sub':sub}
	return render(request,'ebookstore/orderedcart.html',context)





