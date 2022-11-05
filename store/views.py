from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cart_data, guest_checkout
import json
import datetime

# Create your views here.


def store(req):
    data = cart_data(req)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(req, "store/store.html", context)


def cart(req):
    data = cart_data(req)
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(req, "store/cart.html", context)


def checkout(req):
    data = cart_data(req)
    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

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

    return JsonResponse("item was updated", safe=False)


def process_order(req):
    data = json.loads(req.body)

    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = order.objects.get_or_create(customer=customer, complete=False)
    else:
        order, customer = guest_checkout(req, data)

    if order.shipping == True:
        ShippingAddress.objects.create(
            order=order,
            customer=customer,
            address=data["address"],
            city=data["city"],
            state=data["state"],
            zipcode=data["zipcode"],
        )

    transaction_id = datetime.datetime.now().timestamp()
    total = float(data["total"])
    order.transaction_id = transaction_id

    print(total)
    print(order.get_cart_total)
    if total == float(order.get_cart_total):
        print("total and order total are the same")
        order.complete = True
    order.save()
    return JsonResponse("payment processed", safe=False)
