from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import TemplateView

from .forms import (UserLoginForm, PwdResetForm, PwdResetConfirmForm)
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/user/login.html',
     form_class=UserLoginForm), 
     name='login'
     ),
    path('logout/',views.logout_view, name='logout'),

    path('register/',views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),

    #password reset without login
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/user/password_reset_form.html',
                                                                success_url='password_reset_email_confirm',
                                                                email_template_name='account/user/password_reset_email.html',
                                                                form_class=PwdResetForm),name='pwdreset'),

    
    path('passsword_reset_comfirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html',
                                                                                                success_url='password_reset_complete/',
                                                                                                form_class=PwdResetConfirmForm),name='pwdresetc'),
    

    
    path('password_reset/password_reset_email_confirm', TemplateView.as_view(template_name='account/user/reset_status.html'),name='password_reset_done'),
    path('password_reset_complete/', TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_reset_complete'),


    #profile
    path('profile/', views.profile, name ='profile'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_comfirmation', TemplateView.as_view(template_name='account/user/delete_confirmation.html'), name='delete_confirmation'),
    #path('profile/change_password/', template_name="account/user/change_password.html", success_url='password_reseted', form_class=PwdChangeForm),name='pwdchange')
    #path acima e relacionado a troca de senha que pode talvez ser subistituido por um sucess_url


    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),
    path("user_orders/", views.user_orders, name="user_orders"),
     # Wish List
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
]