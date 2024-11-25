# urls.py
from django.urls import path
from . import views


urlpatterns = [
        path('create_review/', views.create_review, name='create_review'),
        path('reviews-list/', views.reviews, name='reviews'),
        path('create_review/<int:order_id>/', views.create_review_orders, name='create_review_orders'),
        path('review/<int:review_id>/detail/', views.review_detail, name='review_detail'),
        path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
        path('update/<int:review_id>/', views.update_review, name='update_review'),
        path('search_review/', views.search_review, name='search_review'),
]
