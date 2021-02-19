from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404

from .models import Category, Product


def homepage(request):
    categories = Category.objects.all()
    # SELECT * FROM product_category;
    return render(request, 'product/index.html', {'categories': categories})


#products/frukty
# def products_list(request, category_slug):
#     products = get_list_or_404(Product, category_id=category_slug)
#     return render(request, 'product/products_list.html', {'products': products})


def products_list(request, category_slug):
    if not Category.objects.filter(slug=category_slug).exists():
        raise Http404('Нет такой категории')
    products = Product.objects.filter(category_id=category_slug)
    return render(request, 'product/products_list.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_details.html', {'product': product})


#TODO: переписать вьюшки на CBV (Class-Based Views)

# # products/?category=slug
# def products_list_2(request):
#     category_slug = request.GET.get('category')
#     products = Product.objects.all()
#     if category_slug is not None:
#         products = products.filter(category_id=category_slug)
#     return render(request, '', {'products': products})


#all() - выводит все объекты модели
# SELECT * FROM table;

# filter() - фильтрует результаты запроса
# SELECT * FROM table WHERE ...;

# exclude(category_id=1) - исключает из результатов объекты, отвечающие условию;
# SELECT * FROM table WHERE category != 1;

# exclude(title__startswith='Apple')
# SELECT * FROM product WHERE title NOT LIKE 'Apple%';

# order_by() - сортировка результатов запроса
# Product.objects.order_by('price');
# SELECT * FROM product ORDER BY price ASC;

# Product.objects.order_by('-price')
# SELECT * FROM product ORDER BY price DESC;

# Product.objects.order_by('price', 'popularity')
# SELECT * FROM product ORDER BY price ASC, popularity ASC;

# Product.objects.order_by('?') - рандомная сортировка

# reverse() - изменяет порядок на обратный

# Product.objects.all() ->
# <Queryset: ["Мясо", "Картошка", "Молоко"]>

# Product.objects.reverse() ->
# <Queryset: ["Молоко", "Картошка", "Мясо"]>

# distinct() - исключает повторения
# Product.objects.values_list('category', flat=True)
# ['frukty', 'frukty', 'milk', 'myaso', 'milk']
#
# Product.objects.values_list('category', flat=True).distinct()
# ['frukty', 'milk', 'myaso']
#
# values()
# # Product.objects.all() ->
# # <QuerySet: [object1, object2, object3]>
#
# Product.objects.values() ->
# <QuerySet: [{'id': 1, 'title': 'Молоко', 'description': ...}, {'id': 2, ...}]>
#
# Product.objects.values('id', 'title')->
# <QuerySet: [{'id': 1, 'title': 'Молоко'}, {'id': 2, 'title': 'Мясо'}]


# values_list()
# Product.objects.all() ->
# # <QuerySet: [object1, object2, object3]>

# Product.objects.values_list() ->
# <QuerySet: [(1,'Молоко', 'Вкусное молоко', 45.50), (2, 'Мясо', ...)]>

# Product.objects.values_list('id', 'title') ->
# <QuerySet: [(1,'Молоко'), (2, 'Мясо')]>

# Product.objects.values_list('title') ->
# < QuerySet: [('Молоко', ), ('Мясо', )] >
#
# Product.objects.values_list('title', flat=True)
# < QuerySet: ['Молоко', 'Мясо', 'Картошка']>

# none() - пустой queryset

# Product.objects.none() ->
# <QuerySet: []>

# select_related()
# prod = Product.objects.get(id=1)
# prod.category - запрос в БД

# prod = SELECT * FROM product WHERE id=5;
# SELECT * FROM category WHERE id = prod.id;

#
# prod = Product.objects.select_related('category').get(id=1)
# prod.category - запроса нет
# SELECT * FROM product AS p JOIN category AS c ON p.category_id = c.id WHERE p.id = 5;

# # prefetch_related()
# categories = Category.objects.filter(...)
# for cat in categories:
#     cat.product_set.all()
#
# SELECT * FROM category WHERE ...;
# SELECT * FROM product WHERE category_id=5;
# SELECT * FROM product WHERE category_id=6;
# SELECT * FROM product WHERE category_id=8;
#
# categories = Category.objects.prefetch_related('products').filter(...)
# for cat in categories:
#     cat.product_set.all()
#
# SELECT * FROM category WHERE...;
# SELECT * FROM product WHERE category_id IN (5,6,8,9,10, ...);


# defer()
# id, title, description, price, category_id
# Product.objects.all() ->
# SELECT * FROM product;

# Product.objects.defer('price', 'category_id') ->
# SELECT id, title, description FROM product

# only()

# Product.objects.only('price', 'category_id') ->
# SELECT price, category_id FROM product;
#
# get() - возвращает объект
# # product = Product.objects.get(id=1) -> "Молоко"
# # product.id -> 1
# # product.title - > "Молоко"
#
# Если нет объекта по условию:
# # Product.objects.get(id=100) -> Product.DoesNotExist
#
# Если get находит несколько объектов:
# ошибка Product.MultipleObjectsReturned

# create() - позволяет создавать новые объекты модели
# Product.objects.create(title='Пшено', description='...', price=100)
#
# prod = Product(title='Пшено', description='...', price=100)
# prod.save()

# get_or_create(условие) - выбирает объект, отвечающий условию, если объекта нет,
# тогда создаёт

# update_or_create() - обновляет или создаёт объекты

# bulk_create() - позволяет создать одновременно несколько объектов

# obj1 = Product()
# obj2 = Product()
#
# Product.objects.bulk_create([obj1, obj2])

# bulk_update() - обновляет несколько объектов
# update() - обновляет несколько объектов

# count() - возвращает количество результатов queryset

# first(), last()
# Product.objects.order_by('price').first() - первое значение
#
# earliest, latest()
# Product.objects.earliest('price') - первое значение по цене

# exists() - проверяет, есть ли в queryset хоть один результат

# Product.objects.filter(price__gt=2000).exists() -> True/False

# delete() -> удаляет результаты queryset
#
# Product.objects.filter(category_id=2).delete()
#
# explain() - возвращает SQL запрос queryset
# # Product.objects.all().explain() -> SELECT * FROM product;
#
# Field lookups:
# сравнение:
# gt -> ">"
# lt -> "<"
# gte -> ">="
# lte -> "<="
# = -> "="

# starstwith="A" -> LIKE "A%"
# istartswith="A" -> ILIKE "A%"

# contains="day" -> LIKE "%day%"
# icontains="day" -> ILIKE "%day%"

# endswith='j' -> LIKE "%j"
# iendswith="j" -> ILIKE "%j"

# title__exact="Milk" -> WHERE title = "Milk";
# title__iexact="Milk" -> WHERE title ILIKE 'Milk';

# category__isnull=True -> WHERE category IS NULL;
# category__isnull=False -> WHERE category IS NOT NULL;

# id__in=[1,2,3,4] -> WHERE id IN (1, 2, 3, 4);

# Order.objects.filter(date__range=(start_date, stop_date)) ->
# WHERE date BETWEEN start_date AND end_date;

# MVC (Model, View, Controller)
#
# MVT(Model, View, Template)

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='products', null=True, blank=True)
#
#     def get_image_url(self):
#         if self.image:
#             return self.image.url
#         return ''