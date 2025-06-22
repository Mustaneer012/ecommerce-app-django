from django.shortcuts import render, redirect
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# def add_cart(request, product_id):
#     # Get the product by ID
#     product = Product.objects.get(id=product_id)
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]

#             try:
#                 variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                 print(variation)
#                 product_variation.append(variation)
#             except Variation.DoesNotExist:
#                 variation = None

#     # Create or get the cart using the session key
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request)) 
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id=_cart_id(request))
#         cart.save()


#     is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#     if is_cart_item_exists:
#         cart_item = CartItem.objects.filter(product=product, cart=cart)
#         # existing variation -> database
#         # current variation -> product_variation
#         # item id -> database

#         ex_var_list = []
#         id = []
#         for item in cart_item:
#             existing_variation = item.variation.all()
#             ex_var_list.append(list(existing_variation))
#             id.append(item.id)

#         if product_variation in ex_var_list:
#             #increase the cart item quantity
#             index = ex_var_list.index(product_variation)
#             cart_item_id = id[index]
#             cart_item = CartItem.objects.get(product=product, id=cart_item_id)
#             cart_item.quantity += 1
#             cart_item.save()
#     else:
#             cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#             if len(product_variation) > 0:
#                 cart_item.variation.clear()  # Clear existing variations
#                 cart_item.variation.add(*product_variation)  # Add new variations
#                 cart_item.save()
#             else:
#                 cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     cart_item.variation.clear()  # Clear existing variations    
#                     cart_item.variation.add(*product_variation)
#                     cart_item.save()

#     return redirect('cart')



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # Get the product by ID
    # if the user is authenticated, add the product to their cart
    if current_user.is_authenticated:
            product_variation = []
    
            if request.method == 'POST':
                for item in request.POST:
                    key = item
                    value = request.POST[key]
                    try:
                        variation = Variation.objects.get(
                            product=product, 
                            variation_category__iexact=key, 
                            variation_value__iexact=value
                        )
                        product_variation.append(variation)
                    except Variation.DoesNotExist:
                        pass  # Skip invalid variations


            # Check if cart item exists for this product
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

            if is_cart_item_exists:
                cart_items = CartItem.objects.filter(product=product, user=current_user)
                
                ex_var_list = []
                item_ids = []
                for item in cart_items:
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    item_ids.append(item.id)

                # Check if current variation combination already exists
                if product_variation in ex_var_list:
                    # Increase quantity of existing item
                    index = ex_var_list.index(product_variation)
                    cart_item_id = item_ids[index]
                    cart_item = CartItem.objects.get(product=product, id=cart_item_id)
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    # Create new cart item for different variation
                    cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        cart_item.variation.add(*product_variation)
                    cart_item.save()
            else:
                # Create new cart item (no existing items for this product)
                cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    cart_item.variation.add(*product_variation)
                cart_item.save()

            return redirect('cart')
    # If the user is not authenticated, handle the cart using session
    else:
        product_variation = []
        
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(
                        product=product, 
                        variation_category__iexact=key, 
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass  # Skip invalid variations

        # Create or get the cart using the session key
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        # Check if cart item exists for this product
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            
            # Build lists of existing variations and IDs
            ex_var_list = []
            item_ids = []
            for item in cart_items:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                item_ids.append(item.id)

            # Check if current variation combination already exists
            if product_variation in ex_var_list:
                # Increase quantity of existing item
                index = ex_var_list.index(product_variation)
                cart_item_id = item_ids[index]
                cart_item = CartItem.objects.get(product=product, id=cart_item_id)
                cart_item.quantity += 1
                cart_item.save()
            else:
                # Create new cart item for different variation
                cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    cart_item.variation.add(*product_variation)
                cart_item.save()
        else:
            # Create new cart item (no existing items for this product)
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variation.add(*product_variation)
            cart_item.save()

        return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrement the quantity if more than one
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is 1
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_item.delete()  # Remove the item from the cart
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100  # Assuming a tax rate of 2%
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, "store/cart.html", context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100  # Assuming a tax rate of 2%
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, "store/checkout.html", context)