from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id

#Varification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 
import requests



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]  # Default username from email
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()


            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_varification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # send_mail(mail_subject, message, EMAIL_HOST_USER, [to_email])

            # messages.success(request, "Thank you for registering. Please check your email to activate your account.")

            return redirect('/accounts/login?command=verification&email=' + email)  # Redirect to login page with a message
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, "accounts/register.html", context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None: # Check if user exists
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key If the user is logged in, assign the cart items to the user
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_items:
                        variation = item.variation.all()
                        product_variation.append(list(variation))  # Get all variations of the cart items

                    # Get the cart items from the user to accessing product variations
                    cart_items = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    item_ids = []
                    for item in cart_items:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        item_ids.append(item.id)
                    
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = item_ids[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.get(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            
            url = request.META.get('HTTP_REFERER')  # Get the 
            try:
                #install requests library if not already installed
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    return redirect(params['next'])  # Redirect to the next page if it exists
            except:
                return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        

    return render(request, "accounts/login.html")



@login_required(login_url='login') #check if user is logged in
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid) #ye chatgpt nay diya ha
        # user = Account._default_manager.get(pk=uid) leature ma asa kiya tha 
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
    return redirect('register') 

@login_required(login_url='login') #check if user is logged in
def dashboard(request):
    return render(request, "accounts/dashboard.html")



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset link has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist.")
            return redirect('forgotPassword')
        
    return render(request, "accounts/forgotPassword.html")



def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid  # Store the user ID in the session
        messages.success(request, "Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request, "This link has expired!")
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')  # Get the user ID from the session
            if uid:
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "Invalid session. Please try again.")
                return redirect('forgotPassword')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('resetPassword')

    return render(request, "accounts/resetPassword.html")