# Задание
# Создайте пару представлений в вашем первом приложении:
# — главная
# — о себе.
# Внутри каждого представления должна быть переменная html — многострочный текст с HTML-вёрсткой
# и данными о вашем первом Django-сайте и о вас.
# Сохраняйте в логи данные о посещении страниц.
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.http import Http404
import logging
from django.http import HttpResponse
from django.core.management import call_command
from hw_app.models import User, Product, Order
from .forms import ProductForm, ImageForm, EditProductForm
from .models import Product, User, Order
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import MultipleObjectsReturned


logger = logging.getLogger(__name__)


def index(request):
    logger.info('Просмотр главной страницы".')
    context = {
        'title': 'Главная',
        'message': 'Это главная страница'
    }
    return render(request, 'hw_app/index.html', context)



def about(request):
    logger.info('Просмотр страницы "Обо мне"".')
    context = {
        'title': 'О нас',
        'message': 'Это страница c информацией о нас...'
    }
    return render(request, 'hw_app/about.html', context)

def get_all_users(request):
    logger.info('Просмотр списка клиентов".')
    users = User.objects.all()
    return render(request, 'hw_app/get_all_users.html', {'users': users})

def get_all_products(request):
    logger.info('Просмотр списка товаров".')
    products = Product.objects.all()
    return render(request, 'hw_app/get_all_products.html', {'products': products})

# Задание №7
# Доработаем задачу 8 из прошлого семинара про клиентов,
# товары и заказы.
# Создайте шаблон для вывода всех заказов клиента и
# списком товаров внутри каждого заказа.
# Подготовьте необходимый маршрут и представление.

def get_orders_user(request, customer_id=None):
    logger.info('Просмотр списка заказов клиента')
    if customer_id:
        try:
            customer = get_object_or_404(User, id=customer_id)
            orders = Order.objects.filter(customer=customer)
            # if not orders.exists():
            #     raise Http404("Заказы для данного клиента не найдены")
            orders_with_products = []
            for order in orders:
                products = Product.objects.filter(order=order)
                orders_with_products.append((order, products))
            sorted_orders_with_products = sorted(orders_with_products, key=lambda x: x[0].date_ordered, reverse=True)
            context = {
                'customer': customer,
                'sorted_orders_with_products': sorted_orders_with_products,
                'user_id': customer_id,
                'user_name': customer.name
            }
            return render(request, 'hw_app/get_orders_user.html', context)
        except Http404 as e:
            return render(request, 'hw_app/choose_user.html', {'message': f'Клиента {customer_id} не существует'})
    else:
        message = "Выберите пользователя"
        context = {
            'message': message
        }
        return render(request, 'hw_app/choose_user.html', context)
#
# Домашнее задание
# Продолжаем работать с товарами и заказами.
# Создайте шаблон, который выводит список заказанных
# клиентом товаров из всех его заказов с сортировкой по
# времени:
# ○ за последние 7 дней (неделю)
# ○ за последние 30 дней (месяц)
# ○ за последние 365 дней (год)
# *Товары в списке не должны повторятся.
def get_products_user(request, customer_id=None, period=None):
    logger.info('Просмотр списка заказанных клиентом товаров')
    if customer_id:
        try:
            customer = get_object_or_404(User, id=customer_id)
            today = datetime.now().date()
            if period == 1:
                start_date = today - timedelta(days=7)
            elif period == 2:
                start_date = today - timedelta(days=30)
            elif period == 3:
                start_date = today - timedelta(days=365)
            else:
                start_date = today

            orders = Order.objects.filter(date_ordered__gte=start_date, date_ordered__lte=today, customer=customer)
            unique_products = set()
            for order in orders:
                for product in order.products.all():
                    unique_products.add(product)
            sorted_products = sorted(unique_products, key=lambda x: x.name, reverse=False)
            return render(request, 'hw_app/get_products_user.html', {'sorted_products': sorted_products, 'period': period})
        except Http404 as e:
            return render(request, 'hw_app/choose_user.html', {'message': f'Клиента {customer_id} не существует'})
    else:
        message = "Выберите пользователя"
        context = {
            'message': message
        }
        return render(request, 'hw_app/choose_user_and_period.html', context)

def creat_user(request):
    logger.info('Добавить клиента".')
    call_command('create_user',)
    return HttpResponse(f'Новый клиент создан')

def delete_user(request, user_id):
    logger.info('Удалить клиента".')
    call_command('delete_user', user_id)
    return HttpResponse(f'Пользователь удален')



# def creat_product(request):
#     logger.info('Добавить товар".')
#     call_command('create_product',)
#     return HttpResponse(f'Новый товар добавлен')

def delete_product(request, product_id):
    logger.info('Удалить товар".')
    call_command('delete_product', product_id)
    return HttpResponse(f'Товар c id: {product_id} удален')

#дз Задание №6, №7 фото хранить в базе ссылкой, а фото в медиа

# def add_product(request):
#     message = ''
#     filename = None
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             price = form.cleaned_data['price']
#             quantity = form.cleaned_data['quantity']
#             if Product.objects.filter(name=name).exists():
#                 message = f'Товар с названием {name} уже добавлен, введите новый'
#                 logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
#             else:
#                 logger.info(f'Добавлен товар {name=}, {description=}, {price=}.')
#                 product = Product(name=name, description=description, price=price, quantity=quantity, image=filename)
#                 product.save()
#                 message = f'Товар {name} добавлен'
#                 #messages.success(request, message)
#
#     else:
#         form = ProductForm()
#         message = 'Добавление нового товара. Введите данные о товаре'
#     return render(request, "hw_app/add_product.html", {'form': form, 'message': message})

# def add_product(request):
#     message = ''
#     filename = None
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             price = form.cleaned_data['price']
#             quantity = form.cleaned_data['quantity']
#             # image = form.cleaned_data['image']
#             # fs = FileSystemStorage()
#             # fs.save(image.name, image)
#             #image = form.cleaned_data['image']
#             if 'image' in request.FILES:  # Проверка наличия файла image
#                 image = form.cleaned_data['image']
#                 # Сохраняем файл, указывая путь назначения
#                 filename = 'products/' + image.name
#                 product = Product(name=name, description=description, price=price, quantity=quantity)
#                 product.save()
#                 filename = 'products/' + image.name
#                 fs = FileSystemStorage()
#                 fs.save(filename, image)
#                 product.image = filename
#                 product.save()
#             else:
#                 product = Product(name=name, description=description, price=price, quantity=quantity)
#                 product.save()
#                 message = f'Товар {name} добавлен'
#             # if Product.objects.filter(name=name).exists():
#             #     message = f'Товар с названием {name} уже добавлен, введите новый'
#             #     logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
#             # else:
#             #     logger.info(f'Добавлен товар {name=}, {description=}, {price=}.')
#             #     product = Product(name=name, description=description, price=price, quantity=quantity, image=filename)
#             #     product.save()
#             #     message = f'Товар {name} добавлен'
#                 #messages.success(request, message)
#
#     else:
#         form = ProductForm()
#         message = 'Добавление нового товара. Введите данные о товаре'
#     return render(request, "hw_app/add_product.html", {'form': form, 'message': message})


# def add_product(request):#рабочий
#     message = ''
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             price = form.cleaned_data['price']
#             quantity = form.cleaned_data['quantity']
#             if 'image' in request.FILES:
#                 image = form.cleaned_data['image']
#                 filename = 'products/' + image.name
#                 try:
#                     product = Product.objects.get(name=name)
#                     message = f'Товар с названием {name} уже добавлен, введите новый'
#                     logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
#                 except Product.DoesNotExist:
#                     fs = FileSystemStorage()
#                     fs.save(filename, image)
#                     product = Product(name=name, description=description, price=price, quantity=quantity, image=filename)
#                     product.save()
#                     message = f'Товар {name} добавлен'
#             else:
#                 try:
#                     product = Product.objects.get(name=name)
#                     message = f'Товар с названием {name} уже добавлен, введите новый2'
#                     logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
#                 except Product.DoesNotExist:
#                     product = Product(name=name, description=description, price=price, quantity=quantity)
#                     product.save()
#                     message = f'Товар {name} добавлен2'
#     else:
#         form = ProductForm()
#         message = 'Добавление нового товара. Введите данные о товаре'
#     return render(request, "hw_app/add_product.html", {'form': form, 'message': message})
#
# def edit_product(request):
#     if request.method == 'POST':
#         form = EditProductForm(request.POST)
#         if form.is_valid():
#             id = form.cleaned_data['id']
#             name = form.cleaned_data['name']
#             description = form.cleaned_data['description']
#             price = form.cleaned_data['price']
#             quantity = form.cleaned_data['quantity']
#             try:
#                 product = Product.objects.get(id=id)
#                 product.name = name
#                 product.description = description
#                 product.price = price
#                 product.quantity = quantity
#                 product.save()
#                 message = f'Товар {name} отредактирован'
#                 logger.info(f'Товар {name=} был отредактирован')
#             except Product.DoesNotExist:
#                 message = f'Товар с id {id} и названием {name} не найден'
#                 logger.info(f'Отказ в редактировании товара с id {id} и названием {name}')
#
#     else:
#         form = ProductForm()
#         message = 'Выберите товар для редактирования'
#     return render(request, "hw_app/edit_product.html", {'form': form, 'message': message})

def add_product(request):
    message = ''
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            if 'image' in request.FILES:
                image = form.cleaned_data['image']
                filename = 'products/' + image.name
                fs = FileSystemStorage()
                fs.save(filename, image)

                product_exists = Product.objects.filter(name=name).exists()
                if product_exists:
                    message = f'Товар с названием {name} уже добавлен, введите новый'
                    logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
                else:
                    product = Product(name=name, description=description, price=price, quantity=quantity, image=filename)
                    product.save()
                    message = f'Товар {name} добавлен'
            else:
                product_exists = Product.objects.filter(name=name).exists()
                if product_exists:
                    message = f'Товар с названием {name} уже добавлен, введите новый'
                    logger.info(f'Отказ в добавлении дубля товара {name=}, {description=}, {price=}.')
                else:
                    product = Product(name=name, description=description, price=price, quantity=quantity)
                    product.save()
                    message = f'Товар {name} добавлен2'
        else:
            message = 'Форма содержит неверные данные'
    else:
        form = ProductForm()
        message = 'Добавление нового товара. Введите данные о товаре'
    return render(request, "hw_app/add_product.html", {'form': form, 'message': message})

def get_selected_product(request):
    product_id = request.GET.get('product_id', None)
    response_data = {}
    product = Product.objects.get(pk=product_id)
    response_data['name'] = product.name
    response_data['description'] = product.description
    response_data['price'] = product.price
    response_data['quantity'] = product.quantity
    #message = f"Выбран товар для редактирования {product.name}"
    return JsonResponse(response_data)

def edit_product(request):
    message = ""

    if request.method == 'GET':
        product_id = request.GET.get('product_options', None)

        if product_id is not None:
            product = Product.objects.get(pk=product_id)
            form = EditProductForm(initial={
                'product_options': product_id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity
            })
            message = f"Выбран товар для редактирования {form.name}"
            return render(request, "hw_app/edit_product.html",
                          {'form': form, 'message': message})
            #get_selected_product(request)
            # selected_product_id = int(product_id)
            # response_data = {}
            # product = Product.objects.get(pk=product_id)
            # response_data['name'] = product.name
            # response_data['description'] = product.description
            # response_data['price'] = product.price
            # response_data['quantity'] = product.quantity
            #
            # return JsonResponse(response_data, message)
        else:
            form = EditProductForm()
            message = 'Выберите товар для редактирования'
    elif request.method == 'POST':
        form = EditProductForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_options']
            product = Product.objects.get(pk=product_id)
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.quantity = form.cleaned_data['quantity']
            product.save()
            message = f"Товар {product.name} успешно сохранен, выберите следующий товар для редактирования"
            form = EditProductForm()
    else:
        form = EditProductForm()
        message = 'Выберите товар для редактирования'

    return render(request, "hw_app/edit_product.html", {'form': form, 'message': message, '_product_id': product_id})

# Измените модель продукта, добавьте поле для хранения
# фотографии продукта.

