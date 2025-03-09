from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-request/', views.create_request, name='create_request'),
    path('create-offer/', views.create_offer, name='create_offer'),
    path('offers/', views.offer_list, name='offer_list'),
    path('select-offer/<int:offer_id>/', views.select_offer, name='select_offer'),
    path('view-requests/', views.view_requests, name='view_requests'),
    path('my-profile/', views.my_profile, name='my_profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)