from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('amplificadores/', views.amplifiers, name='amplifiers'),
    path('sobre/', views.about, name='sobre'),
    path('new_amplifier/', views.new_amplifier, name='new_amplifier'),
    path('new_model/', views.new_model, name='new_model'),
    path('detail_amplifier/<int:id>', views.detail_amplifier, name='detail_amplifier'),
    path('prediction/<int:id>/<int:doc>', views.prediction, name='prediction'),
    path('result/<int:id>/<str:x>/<str:y>', views.result, name='result'),
    path('compare/<int:id>/<str:x>/<str:y>/<int:doc>', views.compare, name='compare'),   
    path('train/', views.train, name='train'),
    path('visualize_erro/<int:id>', views.visualize_erro, name = 'visualize_erro'),
    #path('download/h5files/<str:file_name>', views.download, name = 'download'),
]
