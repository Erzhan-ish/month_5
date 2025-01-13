from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from .serializers import ProductSerializer, ProductItemSerializer
from rest_framework import status


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)

    elif request.method == 'PUT':
        # update
        product.title = request.data.get('title')
        product.text = request.data.get('text')
        product.price = request.data.get('price')
        product.is_active = request.data.get('is_active')
        product.category_id = request.data.get('category_id')
        product.search_words.set(request.data.get('search_words'))
        product.save()
        return Response(data=ProductItemSerializer(product).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        # destroy
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect all products from DB (QuerySet)
        products = Product.objects.select_related('category').prefetch_related('search_words', 'reviews').all()

        # step 2: Reformat (Serialize) QuerySet to list of dictionary
        list = ProductSerializer(instance=products, many=True).data

        # step 3: Return response as data and status (200)
        return Response(data=list)
    elif request.method == 'POST':
        print(request.data)
        # step 1: Receive data from RequestBody
        title = request.data.get('title')
        text = request.data.get('text')
        price = request.data.get('price')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        search_words = request.data.get('search_words')

        print(title, text, price, is_active)
        # step 2: Create product
        product = Product.objects.create(
            title=title,
            text=text,
            price=price,
            is_active=is_active,
            category_id=category_id
        )
        product.search_words.set(search_words)
        product.save()

        # step 3: Return response (product, status)
        return Response(data=ProductItemSerializer(product).data, status=status.HTTP_201_CREATED)
