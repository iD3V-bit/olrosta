
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('apie/', views.about, name='about'),
    path('prekes/', views.product_list, name='products'), # Pataisyta į product_list pagal tavo views.py
    path('kategorija/<int:pk>/', views.category_detail, name='category_detail'),
    path('darbai/', views.projects, name='projects'),
    path('kontaktai/', views.contact, name='contact'),
    path('preke/<int:pk>/', views.product_detail, name='product_detail'),
    path('registracija/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('preke/<int:product_id>/atsiliepimas/', views.add_review, name='add_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
