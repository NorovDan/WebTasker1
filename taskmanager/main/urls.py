from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index,name ="home"),
    path("about",views.about,name = "about"),
    path("create",views.create,name = "create"),
    path("<int:task_id>/delete/",views.delete,name= "delete"),
    path('search/', views.search, name='search'),
    path("wikipedia_search",views.wikipedia_search,name="wikipedia_search"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)