from django.urls import path
from django.conf.urls import url
from Apptemp import views

# FOR TEMPLATE TAGGING:
app_name = 'Apptemp'

urlpatterns = [
    path('', views.index,name='index'),
    path('relative/', views.rel_url, name='relative'),
    path('other/', views.other, name='other'),
    path('register/', views.registration, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]
