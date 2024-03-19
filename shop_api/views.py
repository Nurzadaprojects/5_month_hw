from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer, ReviewSerializer
from product.models import Product, Review
from rest_framework import status
from django.db.models import Avg, Count


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
    product_list = Product.objects.select_related('manager').prefetch_related('reviews', 'color').all()
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

@api_view(['GET'])
def products_with_reviews(request):
    products = Product.objects.prefetch_related('reviews').all()
    products_data = []
    for product in products:
        reviews_data = [{'text': review.text, 'stars': review.stars} for review in product.reviews.all()]
        average_rating = product.reviews.aggregate(avg_rating=Avg('stars'))['avg_rating']
        products_data.append({
            'id': product.id,
            'title': product.title,
            'reviews': reviews_data,
            'average_rating': average_rating
        })
    return Response(products_data)

@api_view(['GET'])
def categories_with_product_counts(request):
    categories = Product.objects.values('category').annotate(products_count=Count('id'))
    categories_data = [{'category': category['category'], 'products_count': category['products_count']} for category in categories]
    return Response(categories_data)