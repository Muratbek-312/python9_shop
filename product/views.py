from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import View

from .forms import CreateProductForm, ImagesFormSet
from .models import Category, Product, ProductImage


class HomePageView(ListView):
    model = Category
    template_name = 'product/index.html'
    context_object_name = 'categories'


class ProductsListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if not Category.objects.filter(slug=category_slug).exists():
            raise Http404('Нет такой категории')
        queryset = queryset.filter(category_id=category_slug)
        return queryset


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


class ProductEditView(IsAdminCheckMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product)
        formset = ImagesFormSet(queryset=product.images.all())
        return render(request, 'product/edit.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product, data=request.POST)
        formset = ImagesFormSet(request.POST,
                                request.FILES,
                                queryset=product.images.all())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None and not ProductImage.objects.filter(product=product, image=image).exists():
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            for form in formset.deleted_forms:
                image = form.cleaned_data.get('id')
                if image is not None:
                    image.delete()

            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)



class ProductEditView(IsAdminCheckMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product)
        formset = ImagesFormSet(queryset=product.images.all())
        return render(request, 'product/edit.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product, data=request.POST)
        formset = ImagesFormSet(request.POST,
                                request.FILES,
                                queryset=product.images.all())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None and not ProductImage.objects.filter(product=product, image=image).exists():
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            for form in formset.deleted_forms:
                image = form.cleaned_data.get('id')
                if image is not None:
                    image.delete()

            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('index-page')


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('index-page')


