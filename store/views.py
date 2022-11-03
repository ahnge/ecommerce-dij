from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime

# Create your views here.


def store(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]
    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(req, "store/store.html", context)


def cart(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(req, "store/cart.html", context)


def checkout(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(req, "store/checkout.html", context)


def update_item(req):

    data = json.loads(req.body)
    productId = data["productId"]
    action = data["action"]

    customer = req.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("item was added", safe=False)


def process_order(req):
    data = json.loads(req.body)
    transaction_id = datetime.datetime.now().timestamp()

    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                order=order,
                customer=customer,
                address=data["address"],
                city=data["city"],
                state=data["state"],
                zipcode=data["zipcode"],
            )

    else:
        print("userj is not loggin ")
    return JsonResponse("payment processed", safe=False)
