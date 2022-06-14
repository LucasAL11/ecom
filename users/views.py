from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders

from .models import UserBase, Address
from orders.models import Order
from products.models import Product

from .forms import RegistrationForm, UserEditForm,UserAddressForm


from .tokens import account_activation_token



@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/profile/user_wishlist.html", {"wishlist": products})

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.name + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def profile(request):
    orders = user_orders(request)
    return render(request,
                  'account/profile/profile.html',
                  {'section': 'profile', 'orders': orders})


def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        
        if user_form.is_valid(): 
                user_form.save()
    
    else:
        user_form = UserEditForm(instance=request.user)
            
    return render(request,'account/profile/edit_details.html', {'user_form':user_form})


@login_required
def delete_user(request):
    
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('users:delete_confirmation')

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')
    
def account_register(request):

    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            #email activation link
            current_site = get_current_site(request)
            subject = 'Ative sua conta'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            
            return render(request, 'account/registration/account_created.html')
    else:
        registerForm = RegistrationForm()
    return render(request,'account/registration/register.html', {'forms': registerForm})


def account_activate(request, uidb64, token):
    #try to get the user in the DB 
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:profile')
    else:
        return render(request, 'account/registration/activation_invalid.html')



# Addresses

@login_required
def view_address(request):
    addresses = Address.objects.filter(custumer=request.user)
    return render(request, "account/profile/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.custumer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("users:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/profile/edit_addresses.html", {"form": address_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, custumer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("users:addresses"))
    else:
        address = Address.objects.get(pk=id, custumer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/profile/edit_addresses.html", {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, custumer=request.user).delete()
    return redirect("users:addresses")

@login_required
def set_default(request, id):
    Address.objects.filter(custumer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, custumer=request.user).update(default=True)
    return redirect("users:addresses")

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(paid=True)
    return render(request, "account/profile/user_orders.html", {"orders": orders})