# -*- coding: utf8 -*-
import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect

from models import Category, Product, Comment
from store.forms import CommentForm
from carton.cart import Cart


def get_categories():
    main_category = Category.objects.get(parent_category=None)
    categories = main_category.category_set.order_by('id')
    return categories

def get_cart(request):
    cart = Cart(request.session)
    return cart


class MainMock:
    name = "Главная"
    get_path_uri = ""


def render_category(request, *category_path):
    category_path = [int(s) for s in category_path if s]

    categories = get_categories()

    bread_categories = [MainMock()]
    if category_path:
        parent_category = Category.objects.get(pk=category_path[-1])

        render_categories = parent_category.category_set.all()
        product_list = parent_category.product_set.all()
        bread_categories += parent_category.get_path_up()
    else:
        render_categories = categories
        product_list = []

    product_paginator = Paginator(product_list, 36)
    page = request.GET.get('page') or 1
    if page:
        page = int(page)

    try:
        products = product_paginator.page(page)
    except PageNotAnInteger:
        products = product_paginator.page(1)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    context_dict = dict(category_path=category_path,
                        categories=categories,
                        render_categories=render_categories,
                        products=products,
                        current_page=page,
                        cart=get_cart(request),
                        bread_categories=bread_categories,
                        )
    return render(request, 'store/index.html', context_dict)


def product_page(request, product_id):
    product = Product.objects.get(pk=product_id)
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data.get("author_name") or u"Гость"
            body = form.cleaned_data.get("body")
            c = Comment(author_name=author_name,
                        body=body,
                        product=product)
            c.save()
            return HttpResponseRedirect('/product/' + product_id)
    else:
        form = CommentForm()

    categories = get_categories()
    comments = product.comment_set.all().order_by('-date')[:10]
    bread_categories = [MainMock()] + product.category.get_path_up()
    print(bread_categories)

    context_dict = dict(product=product,
                        categories=categories,
                        comments=comments,
                        form=form,
                        cart=get_cart(request),
                        bread_categories=bread_categories,
                        )

    return render(request, 'store/product.html', context_dict)


def rate_product(request):
    product_id = None
    rating = None
    if request.method == 'GET':
        product_id = int(request.GET.get('product_id'))
        rating = int(request.GET.get('value'))

    product = Product.objects.get(pk=product_id)

    product.total_rating = product.total_rating + rating
    product.raters = product.raters + 1
    product.save()

    results = {'rating': product.get_average_rating(),
               'raters': product.raters}

    json_response = json.dumps(results)
    return HttpResponse(json_response, content_type='application/json')


def add_product(request, product_id):
    cart = Cart(request.session)
    product = Product.objects.get(pk=product_id)
    cart.add(product, price=product.price_ukr())

    result = {'products_in_cart': len(cart.items),
              'cart_total_sum': int(cart.total)}

    json_response = json.dumps(result)
    return HttpResponse(json_response, content_type="application/json")

def show_products(request):
    categories = get_categories()
    cart = Cart(request.session)
    context = {'cart': cart,
               'categories': categories}
    print(render(request, "store/cart.html", context))
    return render(request, "store/cart.html", context)


def remove_product(request, product_id):
    cart = Cart(request.session)
    product = Product.objects.get(pk=product_id)
    cart.remove(product)
    return update_cart(request)


def show_delivery_page(request):
    categories = get_categories()
    cart = get_cart(request)
    context = {'cart': cart,
               'categories': categories}
    return render(request, "store/delivery.html", context)


def show_contact_page(request):
    categories = get_categories()
    cart = get_cart(request)
    context = {'cart': cart,
               'categories': categories}
    return render(request, "store/contact.html", context)


def receive_backcall_query(request):
    name = request.POST.get('back_call_name').encode('utf-8')
    phone = request.POST.get('back_call_phonenumber')

    title = '[Перезвонить] {} - {}'.format(name, phone)
    message = '{} посетитель по имени {} оставил заявку на обратный звонок по номеру {}'.format(datetime.datetime.now().strftime('%d.%m.%y в %H:%M'), name, phone)
    from_email = 'let.nemolution@gmail.com'
    recipients = ['alexey.milogradov@gmail.com']

    send_mail(title, message, from_email, recipients, fail_silently=False)

    return HttpResponse(json.dumps({}), content_type="application/json")


def checkout_order(request):
    return render(request, 'store/checkout.html')


def clear_cart(request):
    cart = Cart(request.session)
    cart.clear()
    return HttpResponseRedirect('/')


def update_cart(request):
    cart = get_cart(request)
    context = dict(cart=cart)
    print(cart.count, cart.total)

    json_response = {'table_html': render(request, 'store/_cart.html', context).content,
                     'cart_total_sum': int(cart.total),
                     'products_in_cart': cart.count,
                    }
    json_response = json.dumps(json_response)
    return HttpResponse(json_response, content_type="application/json")
