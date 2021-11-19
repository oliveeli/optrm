from django.urls import path
from resourcemanager import views


urlpatterns = [
    path('', views.ServerListUserView.as_view(), name='user-servers/'),
    path('server/<int:server_id>', views.server_detail, name='server-detail'),
    path('user-servers/', views.ServerListUserView.as_view(),name='user-servers'),
    path('user-servers-download/', views.server_list_download,name='user-servers-download'),
    path('update-server-ips/', views.update_ips,name='update-server-ips'),
    
    
    
    
]
