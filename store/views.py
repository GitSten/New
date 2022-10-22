from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *


# Create your views here.


def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {'trending_products': trending_products}
    return render(request, "store/index.html", context)


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "store/layouts/collections.html", context)


def collectionsview(request, slug):
    if (Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products': products, 'category': category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if (Category.objects.filter(slug=cate_slug, status=0)):
        if (Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products': products}
        else:
            messages.error(request, "No such product found")
            return redirect('collections')

    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    return render(request, "store/products/view.html", context)


def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productList = list(products)

    return JsonResponse(productList, safe=False)


def searchproduct(request):
    if request.method == 'POST':
        serchedterm = request.POST.get('productsearch')
        if serchedterm == '':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=serchedterm).first()

            if product:
                return redirect('collections/' + product.category.slug + '/' + product.slug)
            else:
                messages.info(request, "No product matched for your search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))
