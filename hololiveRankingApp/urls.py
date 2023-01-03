from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Login, Logout, UserCreateView  #HomeView
from . import views

urlpatterns = [
  path('', views.TopView.as_view(), name="top"),
  # path('', views.RankingView.as_view(), name="appHome"), 
  # path('performer_info/', views.PerformerInfoView.as_view(), name='performerInfo'),
  # path('<int:pk>/video_info/total/<int:ranking>/', views.VideoInfoView.as_view(),name='video_info'),
  
  path('video/create', views.VideoInfoCreateView.as_view(), name='create'),
  path('video/', views.VideoInfoListView.as_view(), name='list'),
  path('video/ranking/', views.SearchResultView.as_view(), name='searchResult'),
  path('video/<int:pk>/', views.VideoInfoView.as_view(),name='video_info'),
  path('video/<int:pk>/work/', views.WorkListView.as_view(), name='work'),
  path('video/<int:pk>/update/', views.VideoUpdateView.as_view(), name='update'),
  path('video/<int:pk>/update/Performer/', views.AdminVideoUpdateView.as_view(), name='adminUpdate'),
  path('video/<int:pk>/update/title/', views.AdminTitleView.as_view(), name='title'),
  #<slug:concerned>/
  path('video/<int:redirectPk>/Lyricist/', views.LyricistAddView.as_view(), name='Lyricist'),
  path('video/<int:redirectPk>/Composer/', views.ComposerAddView.as_view(), name='Composer'),
  path('video/<int:redirectPk>/Arranger/', views.ArrangerAddView.as_view(), name='Arranger'),
  path('video/<int:redirectPk>/Mixer/', views.MixerAddView.as_view(), name='Mixer'),
  path('video/<int:redirectPk>/Musician/', views.MusicianAddView.as_view(), name='Musician'),
  path('video/<int:redirectPk>/VideoEditor/', views.VideoEditorAddView.as_view(), name='VideoEditor'),
  path('video/<int:redirectPk>/Illustrator/', views.IllustratorAddView.as_view(), name='Illustrator'),
  path('video/<int:redirectPk>/CoStar/', views.CoStarAddView.as_view(), name='CoStar'),
  path('video/<int:redirectPk>/OriginalSinger/', views.OriginalSingerAddView.as_view(), name='OriginalSinger'),
  path('video/<int:redirectPk>/addNew/', views.ConcernedCreateView.as_view(), name='addNew'),
  
  
  path('video/admin/addNew/', views.ConcernedCreateView.as_view(), name='adminAddNew'),
  
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='logout'),
  path('create/user', UserCreateView.as_view(), name="user_create"), #会員登録ページへのパス
]