from django.shortcuts import (render, HttpResponse, HttpResponseRedirect, 
								Http404, render_to_response, RequestContext)

from django.contrib import messages
# Create your views here.

from ecommerce_free.products.models import Product
from .models import Cart, CartItem
from .forms import ProductQtyForm

def add_to_cart(request):
	request.session.set_expiry(3000)#seconds
	try: 
		cart_id = request.session['cart_id']
	except Exception:
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
		cart_id = cart.id
	if request.method == 'POST':
		form_cart = ProductQtyForm(request.POST)
		if form_cart.is_valid():
			product_slug = form_cart.cleaned_data['slug']
			product_quantity = form_cart.cleaned_data['quantity']
			try:
				product = Product.objects.get(slug=product_slug)
			except Exception:
				product = None
			try:
				cart = Cart.objects.get(id=cart_id)
			except Exception:
				cart = None

			new_cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
			new_cart.quantity = product_quantity
			new_cart.save()
			if created:
				print 'Criado!'
			print new_cart.product
			print new_cart.quantity
			
			return HttpResponseRedirect('/products/')
		return HttpResponseRedirect('/contact/')
	else:
		raise Http404

def view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
	except Exception:
		cart = False

	# if cart == False or cart.active == False: -> refatorado
	if not cart or cart.active: 
		messages.add_message(request, messages.ERROR, 'Seu carrinho esta vazio! =/')

	if cart and cart.active: cart = cart

	context = {'cart':cart, 'items':CartItem.objects.all()}

	return render(request, 'cart/view_cart.html', context)