"""
URL configuration for iblogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

    
urlpatterns = [
    # path('home/', home)
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('error-404/', views.error_404, name='error-404'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter-subscribe'),
    path('academics/fee-structure/', views.fee_structure, name='fee-structure'),

    # Student admission flow
    path('student/register/', views.register_student, name='student-register'),
    path('student/verify-otp/', views.verify_otp, name='student-verify-otp'),
    path('student/login/', views.student_login, name='student-login'),
    path('student/logout/', views.student_logout, name='student-logout'),
    path('student/dashboard/', views.student_dashboard, name='student-dashboard'),
    path('student/payment/', views.payment_summary, name='student-payment'),
    path('student/payment/create-order/', views.create_razorpay_order, name='create-razorpay-order'),
    path('student/payment/verify/', views.verify_razorpay_payment, name='verify-razorpay-payment'),
]
