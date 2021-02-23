from django.urls import path

from .views import HomePageView, ProductsListView, ProductDetailsView

urlpatterns = [
    path('', HomePageView.as_view(), name='index-page'),
    path('products/<slug:category_slug>/', ProductsListView.as_view(), name='products-list'),
    path('products/details/<int:pk>/', ProductDetailsView.as_view(), name="product-details"),
]
