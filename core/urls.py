from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('department/',views.department, name='departments'),
    path('login/',views.login, name='login'),
    # path('signup/',views.signup, name='signup'),
    path('forgotPassword/',views.forgotPassword, name='forgotPassword'),

] 