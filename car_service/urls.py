from django.urls import path, include
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
    path('myorders/<uuid:pk>', views.OrderByUserDetailView.as_view(), name='my-order'),
    path('myorders/new', views.OrderByUserCreateView.as_view(), name='my-ordered-new'),
    path('myorders/<uuid:pk>/update', views.OrderByUserUpdateView.as_view(), name='my-order-update'),
    path('myorders/<uuid:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my-order-delete'),
    path('i18n/', include('django.conf.urls.i18n')),
]
