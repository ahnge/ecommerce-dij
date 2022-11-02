from django.shortcuts import render
from .models import *

# Create your views here.


def store(req):
    products = Product.objects.all()
    print(products)
    context = {"products": products}
    return render(req, "store/store.html", context)


def cart(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}

    context = {"items": items, "order": order}
    return render(req, "store/cart.html", context)


def checkout(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}

    context = {"items": items, "order": order}
    return render(req, "store/checkout.html", context)
