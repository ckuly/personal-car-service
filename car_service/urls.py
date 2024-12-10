from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<uuid:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path('mycars/', views.LoanedCar.as_view(), name='my-cars'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('myorders/', views.OrderServicesByUserListView.as_view(), name='my-ordered'),
]
