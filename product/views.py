from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Category, Product


# def homepage(request):
#     categories = Category.objects.all()
#     # SELECT * FROM product_category;
#     return render(request, 'product/index.html', {'categories': categories})
#
#
# class HomePageView(View):
#     def get(self, request):
#         categories = Category.objects.all()
#         return render(request, 'product/index.html', {'categories': categories})


class HomePageView(ListView):
    model = Category
    template_name = 'product/index.html'
    context_object_name = 'categories'


#products/frukty
# def products_list(request, category_slug):
#     products = get_list_or_404(Product, category_id=category_slug)
#     return render(request, 'product/products_list.html', {'products': products})


# def products_list(request, category_slug):
#     if not Category.objects.filter(slug=category_slug).exists():
#         raise Http404('Нет такой категории')
#     products = Product.objects.filter(category_id=category_slug)
#     return render(request, 'product/products_list.html', {'products': products})


# class ProductsListView(View):
#     def get(self, request, category_slug):
#         if not Category.objects.filter(slug=category_slug).exists():
#             raise Http404('Нет такой категории')
#         products = Product.objects.filter(category_id=category_slug)
#         return render(request, 'product/products_list.html', {'products': products})


class ProductsListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'

    # def get(self, request, category_slug):
    #     if not Category.objects.filter(slug=category_slug).exists():
    #         raise Http404('Нет такой категории')
    #     products = self.get_queryset().filter(category_id=category_slug)
    #     return render(request, 'product/products_list.html', {'products': products})

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if not Category.objects.filter(slug=category_slug).exists():
            raise Http404('Нет такой категории')
        queryset = queryset.filter(category_id=category_slug)
        return queryset


# def product_details(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product/product_details.html', {'product': product})


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'product/product_details.html'
