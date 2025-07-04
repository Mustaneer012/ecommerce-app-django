from django.shortcuts import render , get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewForm
from .models import ReviewRating, ProductGallery
from django.shortcuts import redirect
from orders.models import OrderProduct



# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(product_category=categories, product_available=True)
        paginator = Paginator(products, 1)  # Show 6 products per page
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(product_available=True).order_by('id')
        paginator = Paginator(products, 6)  # Show 6 products per page
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()


    context = {
        "products": page_products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(product_category__slug=category_slug, product_slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists() # filtering cart items by cart_id
        
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews for the product
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery images
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery":product_gallery
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Get the URL of the page that made the request
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(product_id=product_id, user__id=request.user.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
        