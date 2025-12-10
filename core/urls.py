from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/wiki/', views.topic_api, name='topic_api'),
    path('favorite/add/', views.add_favorite, name='add_favorite'),
    path('favorite/delete/<int:topic_id>/', views.delete_favorite, name='delete_favorite'),
    path('favorite/update/<int:topic_id>/', views.update_favorite, name='update_favorite'),
    path('favorite/load/<int:topic_id>/', views.load_mind_map, name='load_mind_map'),
]