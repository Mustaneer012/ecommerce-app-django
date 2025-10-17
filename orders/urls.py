from django.urls import path
from . import views





urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('cod_payment/', views.cod_payment, name='cod_payment'),
]
