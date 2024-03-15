from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer

@api_view(['GET'])
def category_api_view(request):
    dict_ = {
        'name': 'Nurzada',
        'age': 20,
        'gpa': 3.7,
        'married': False,
        'friends': ['Kana', 'Aiza']
    }
    return Response(data=dict_)

@api_view(['GET'])
def category_detail_api_view(request, id):
    dict_ = {
        'name': 'Nurzada',
        'age': 20,
        'gpa': 3.7,
        'married': False,
        'friends': ['Kana', 'Aiza']
    }
    data = ProductSerializer(category_detail, many=False).data
    return Response(data=dict_)



@api_view(['GET'])
def product_api_view(request):
    product_list = Product.objects.all()
    data = ProductSerializer(product_list, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)

    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product_detail, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_api_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)

    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review_detail, many=False).data
    return Response(data=data)