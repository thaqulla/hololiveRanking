from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Login, Logout, UserCreateView  #HomeView
from . import views

urlpatterns = [
  path('', views.TopView.as_view(), name="top"),
  # path('', views.RankingView.as_view(), name="appHome"),
  path('search_result/', views.SearchResultView.as_view(), name='searchResult'),
  path('performer_info/', views.PerformerInfoView.as_view(), name='performerInfo'),
  # path('<int:pk>/video_info/total/<int:ranking>/', views.VideoInfoView.as_view(),name='video_info'),
  path('<int:pk>/video_info/', views.VideoInfoView.as_view(),name='video_info'),
  
  
  path('create/', views.VideoInfoCreateView.as_view(), name='create'),
  path('list/', views.VideoInfoListView.as_view(), name='list'),
  path('<int:pk>/work/', views.WorkListView.as_view(), name='work'),
  path('<int:pk>/update/', views.VideoUpdateView.as_view(), name='update'),
  # path('<int:redirectPk>/addOld/<int:concerned>', views.ConcernedAddView.as_view(), name='addOld'),#<slug:concerned>/
  # path('<int:redirectPk>/addOld/<int:concerned>/', views.ConcernedAddView.as_view(), name='addOld'),#<slug:concerned>/
  path('<int:redirectPk>/addOld/Lyricist/', views.LyricistAddView.as_view(), name='lyricist'),
  path('<int:redirectPk>/addOld/Composer/', views.LyricistAddView.as_view(), name='composer'),
  path('<int:redirectPk>/addOld/Arranger/', views.LyricistAddView.as_view(), name='arranger'),
  path('<int:redirectPk>/addOld/Mixer/', views.LyricistAddView.as_view(), name='mixer'),
  path('<int:redirectPk>/addOld/Musician/', views.LyricistAddView.as_view(), name='musician'),
  path('<int:redirectPk>/addOld/VideoEditor/', views.LyricistAddView.as_view(), name='videoEditor'),
  path('<int:redirectPk>/addOld/Illustrator/', views.LyricistAddView.as_view(), name='illustrator'),
  path('<int:redirectPk>/addOld/CoStar/', views.LyricistAddView.as_view(), name='coStar'),
  path('<int:redirectPk>/addOld/OriginalSinger/', views.LyricistAddView.as_view(), name='originalSinger'),
  # path('<int:redirectPk>/addNew/', views.ConcernedCreateView.as_view(), name='addNew'),
  path('addNew/', views.ConcernedCreateView.as_view(), name='addNew'),
  
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('user_create/', UserCreateView.as_view(), name="user_create"), #会員登録ページへのパス
]