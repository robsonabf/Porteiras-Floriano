from django.urls import path
from .views import home, login, contate, informatica, galeria, visualizar_mensagens

urlpatterns = [
    path('', home),
    path('login/', login),
    path('contate/', contate),
    path('informatica/', informatica),
    path('galeria/', galeria),
    path('area/', visualizar_mensagens, name='adm')
]
