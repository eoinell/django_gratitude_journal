from django.urls import path

from . import views

app_name = 'logger'
urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log, name='log'),
    path('submitted/', views.submitted, name='submitted')
    
    # path('<int:pk>/', views.DetailView. as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]