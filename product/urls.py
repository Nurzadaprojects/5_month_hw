from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.review_api_view),
    path('', views.product_api_view),
    path('<int:id>/', views.product_detail_api_view),

]