from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer, ReviewSerializer, ProductValidateSerializer
from product.models import Product, Review
from rest_framework import status
from django.db.models import Avg, Count
from .serializers import ManagerSerializer




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





@api_view(['GET', 'POST'])
def product_api_view(request):
    if request.method == 'GET':
        product_list = Product.objects.select_related('manager').prefetch_related('reviews', 'color').all()

        data = ProductSerializer(instance=product_list, many=True).data

        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product_detail = Product.objects.get(id=id)

    except Product.DoesNotExist:
        return Response(data={'error_message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        data = ProductSerializer(product_detail, many=False).data

        return Response(data=data)
    elif request.method == 'PUT':
        product_detail.title = request.data.get('title')
        product_detail.description = request.data.get('description')
        product_detail.price = request.data.get('price')
        product_detail.category = request.data.get('category')
        product_detail.manager_id = request.data.get('manager_id')
        product_detail.color.set(request.data.get('color'))
        product_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'product_id': product_detail.id})

    else:
        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    data = ProductSerializer(product_detail, many=False).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def review_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.select_related('product').all()
        serializer = ReviewSerializer(reviews, many=True)


        return Response(serializer.data)
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')


        Review.objects.create(text=text, stars=stars)

        return Response()




@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review_detail = Review.objects.get(id=id)

    except Review.DoesNotExist:
        return Response(data={'error_message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        data = ReviewSerializer(review_detail, many=False).data

        return Response(data=data)
    elif request.method == 'POST':
        review_detail.text = request.data.get('text')
        review_detail.stars = request.data.get('stars')
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'review_id': review_detail.id})

    else:
        review_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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



@api_view(['POST'])
def create_product(request):
    tags_data = request.data.get('tags', [])
    tags_objects = []

    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags_objects.append(tag)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        product.tags.set(tags_objects)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

