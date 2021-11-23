from django.urls import path
from knowledge import views


urlpatterns = [
    path('', views.ArticleListUserView.as_view(), name='knowledge-root'),
    path('article/<int:article_id>', views.article_detail, name='article-detail'),
    path('user-articles/', views.ArticleListUserView.as_view(),name='user-articles'),
]
