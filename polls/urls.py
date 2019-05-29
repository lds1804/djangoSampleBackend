from django.urls import path

from . import views

urlpatterns = [
    path('provider', views.providerCreate, name='providerCreate'),

     # ex: /polls/5/


    path('provider/<int:id>/', views.providerRUD, name='providerRUD'),


    path('polygon', views.polygonCreate, name='polygonCreate'),

    path('polygon/<int:id>/', views.polygonRUD, name='polygonRUD'),


    # path('<int:id>/', views.polygonRUD, name='polygonRUD'),

    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),



]