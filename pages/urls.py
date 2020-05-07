from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('amplificadores/', views.amplifiers, name='amplificadores'),
    path('sobre/', views.about, name='sobre'),
    path('novo_amplificador/', views.novo_amplificador, name='novo_amplificador'),
    path('novo_modelo/', views.novo_modelo, name='novo_modelo'),
    path('detail_amplifier/<int:id>', views.detail_amplifier, name='detail_amplifier'),
    path('result/<int:id>/<str:x>/<str:y>', views.result, name='result'),
    path('compare/<int:id>/<str:x>/<str:y>/<int:doc>', views.compare, name='compare'),   
    path('treino/', views.treino, name='treino'),
    path('visualize_erro/<int:id>', views.visualize_erro, name = 'visualize_erro'),
    path('download/h5files/<str:file_name>', views.download, name = 'download'),
]
