from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from .forms import CreateProductForm, UpdateProductForm, ImagesFormSet
from .models import Category, Product, ProductImage


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



class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and\
               (self.request.user.is_staff or self.request.user.is_superuser)


class ProductCreateView(IsAdminCheckMixin, View):
    def get(self, request):
        form = CreateProductForm()
        formset = ImagesFormSet(queryset=ProductImage.objects.none())
        return render(request, 'product/create.html', locals())

    def post(self, request):
        form = CreateProductForm(request.POST)
        formset = ImagesFormSet(request.POST,
                                request.FILES,
                                queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None:
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)


class ProductEditView(IsAdminCheckMixin, UpdateView):
    model = Product
    template_name = 'product/edit.html'
    form_class = UpdateProductForm


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
