from django.contrib import admin
from .models import Product, Order, User
from django.db.models import F
from django.contrib.auth.models import Group

@admin.action(description="Сбросить количество в ноль")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)

@admin.action(description="Увеличить стоимость на 10 процентов")
def set_a_price_10(modeladmin, request, queryset):
    queryset.update(price = F('price')*1.1)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'quantity', 'price']#вывод этих полей с списке продуктов
    ordering = ['name', '-quantity']# сортировка (минус, сорт по убыванию)
    list_filter = ['data_addition', 'price']#фильтр
    search_fields = ['description']#поиск
    search_help_text = 'Поиск по полю Описание продукта (description)'#
    actions = [reset_quantity, set_a_price_10]
    #actions = [reset_quantity]
    # actions = [set_a_price_10]
    readonly_fields = ['data_addition']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': ' подробное описание', 'fields':['description', 'image']
            },
        ),
        (
            'Бухгалтерия',
            {
                'fields': ['price', 'quantity'],
            }
        ),
    ]

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['pk', 'total_price', 'date_ordered', 'customer_id']#вывод этих полей с списке продуктов
    ordering = ['date_ordered', '-total_price']# сортировка (минус, сорт по убыванию)
    list_filter = ['date_ordered', 'total_price']#фильтр


# @admin.action(description="Перенести в группу")
# def move_to_a_group(modeladmin, request, queryset):
#     group = Group.objects.get(name='Клиенты')
#     queryset.update(group=group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "telephone", "email", "data_registered"]
    ordering = ["name", "data_registered"]
    search_fields = ["name"]
    readonly_fields = ['data_registered']
    # actions = [move_to_a_group]
    fieldsets = [
        (
            "Клиент",
            {
                "classes": ["wide"],
                "fields": ["name", "telephone"],
            },
        ),

        (
            "Контакты",
            {
                "fields": ["email", "address"],
            },
        ),
    ]


# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(User)

# Register your models here.
