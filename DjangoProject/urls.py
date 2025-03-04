from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-request/', views.create_request, name='create_request'),
    path('create-offer/', views.create_offer, name='create_offer'),
    path('offers/', views.offer_list, name='offer_list'),  # Исправляем на offers/
    path('select-offer/<int:offer_id>/', views.select_offer, name='select_offer'),
]