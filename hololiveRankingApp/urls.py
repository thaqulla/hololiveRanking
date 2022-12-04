from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Login, Logout, UserCreateView  #HomeView
from . import views

urlpatterns = [
  path('hololiveRankingApp/', views.TopView.as_view(), name="top"),
  # path('hololiveRankingApp/', views.RankingView.as_view(), name="appHome"),
  path('hololiveRankingApp/search_result/', views.SearchResultView.as_view(), name='searchResult'),
  path('hololiveRankingApp/performer_info/', views.PerformerInfoView.as_view(), name='performerInfo'),
  # path('hololiveRankingApp/<int:pk>/video_info/total/<int:ranking>/', views.VideoInfoView.as_view(),name='video_info'),
  path('hololiveRankingApp/<int:pk>/video_info/', views.VideoInfoView.as_view(),name='video_info'),
  
  
  path('hololiveRankingApp/create/', views.VideoInfoCreateView.as_view(), name='create'),
  path('hololiveRankingApp/list/', views.VideoInfoListView.as_view(), name='list'),
  path('hololiveRankingApp/<int:pk>/work/', views.WorkListView.as_view(), name='work'),
  path('hololiveRankingApp/<int:pk>/update/', views.VideoUpdateView.as_view(), name='update'),
  
  
  path('hololiveRankingApp/login/', Login.as_view(), name='login'),
  path('hololiveRankingApp/logout/', Logout.as_view(), name='logout'),
  path('hololiveRankingApp/user_create/', UserCreateView.as_view(), name="user_create"), #会員登録ページへのパス
]