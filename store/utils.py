from .models import Product, Order, OrderItem, Customer
import json


def cookie_cart(
    req,
):
    try:
        cart = json.loads(req.COOKIES["cart"])
        print(cart)
    except:
        cart = {}

    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            cartItems += cart[i]["quantity"]

            total = product.price * cart[i]["quantity"]
            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image_url": product.image_url,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }
            items.append(item)

            if not product.digital:
                order["shipping"] = True
        except:
            pass

    return {"items": items, "order": order, "cartItems": cartItems}


def cart_data(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(req)
        items = cookieData["items"]
        order = cookieData["order"]
        cartItems = cookieData["cartItems"]

    return {"items": items, "order": order, "cartItems": cartItems}


def guest_checkout(req, data):
    name = data["name"]
    email = data["email"]

    cookie_data = cookie_cart(req)
    items = cookie_data["items"]

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    print(customer)
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for i in items:
        product = Product.objects.get(id=i["product"]["id"])

        order_item = OrderItem.objects.create(
            product=product, order=order, quantity=i["quantity"]
        )
    return order, customer
