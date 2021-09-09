from django import template

register=template.Library()

@register.filter(name="is_present_in_cart")
def is_present_in_cart(item, cart ):
    keys= list(cart.keys())
    for id in keys:
        if id is not None:
            if int(id) == item.id :
                return True
    return False;

@register.filter(name="cart_count")
def cart_count(item, cart ):
    keys= cart.keys()
    for id in keys:
        if int(id) == item.id:
            print(cart.get(id))
            return cart.get(id)
            
    return 0;

@register.filter(name="total_price")
def total_price(item, cart ):
   return item.price * cart_count(item , cart);


@register.filter(name="total_cart_price")
def total_cart_price(items, cart ):
    price =0
    for item in items:
        price = price + total_price(item , cart)
    return price;

@register.filter(name="total_quantity")
def total_quantity(items, cart ):
    quantity=0
    for item in items:
       quantity = quantity + cart_count(item , cart)
    return quantity;

@register.filter(name="currency")
def currency(price):
    return str(price)+' ₹';

@register.filter(name="cart_length")
def cart_length(cart ):
    if cart == {} :
        return 0
    else :
       return (len(cart))

@register.filter(name="orders_total")
def orders_total(quantity , price ):
    return quantity*price;

@register.filter(name="checkout_razorpay")
def checkout_razorpay(items, cart ):
    price =0
    for item in items:
        price = price + total_price(item , cart)
    return price*100;

@register.filter(name="user_info")
def checkout_razorpay(user_id ):
    
    return price*100;

