from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product, Category, SearchWord
from .serializers import (ProductSerializer,
                          ProductItemSerializer,
                          ProductValidateSerializer,
                          CategorySerializer,
                          SearchWordSerializer)
from rest_framework import status
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.viewsets import ModelViewSet


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        print(request.data)
        print(serializer.validated_data)
        # step 1: Receive data from RequestBody
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        search_words = serializer.validated_data.get('search_words')

        print(title, text, price, is_active)
        # step 2: Create product
        with transaction.atomic():
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


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.prefetch_related('products').all() # queryset (list of data from DB)
    serializer_class = CategorySerializer # serializer_class  (Serializer inherited by ModelSerializer)
    pagination_class = CustomPagination

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class SearchWordViewSet(ModelViewSet):
    queryset = SearchWord.objects.all()
    serializer_class = SearchWordSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

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
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.text = serializer.validated_data.get('text')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.search_words.set(serializer.validated_data.get('search_words'))
        product.save()
        return Response(data=ProductItemSerializer(product).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        # destroy
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect all products from DB (QuerySet)
        products = Product.objects.select_related('category').prefetch_related('search_words', 'reviews').all()

        # step 2: Reformat (Serialize) QuerySet to list of dictionary
        list = ProductSerializer(instance=products, many=True).data

        # step 3: Return response as data and status (200)
        return Response(data=list)
    elif request.method == 'POST':

        # step 0: Validation (Existing, Typing and Extra)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        print(request.data)
        print(serializer.validated_data)
        # step 1: Receive data from RequestBody
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        search_words = serializer.validated_data.get('search_words')

        print(title, text, price, is_active)
        # step 2: Create product
        with transaction.atomic():
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
