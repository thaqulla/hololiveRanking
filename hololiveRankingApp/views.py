from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min
from django.db.models import Q
from django import forms

from .forms import LoginForm
from .forms import VideoInfoForm, AdminVideoInfoForm, AdminTitleForm, \
  LyricistAddForm, ComposerAddForm, ArrangerAddForm, MixerAddForm, MusicianAddForm,\
  VideoEditorAddForm, IllustratorAddForm, CoStarAddForm, OriginalSingerAddForm
from .models import VideoInfo, hololiveChannel2, hololiveSongsResult, AutoChannel,\
  videoTypeJudgement, Lyricist,Composer,Arranger,Mixer,Musician,VideoEditor,\
  Illustrator,CoStar,OriginalSinger,AnotherPerson

from io import BytesIO
from matplotlib import pyplot
from matplotlib.ticker import ScalarFormatter

import base64
import datetime
import japanize_matplotlib
import numpy as np
import pandas as pd
import random
import requests as re

# TODO: N+1問題が解決されていないため全体的にコードの見直しが必須
# TODO: リファクタリング
# TODO: pep8に基づいたコードの書き方に変更予定

dt = datetime.date.today()  # ローカルな現在の日付と時刻を取得
dtstr = dt.strftime("%Y-%m-%d")

def get_header_context_data(context):
  # context = super().get_context_data(**kwargs)
  context["JPall_1"] = hololiveChannel2.objects.filter(Q(category__GenName="０期生")\
                                          |Q(category__GenName="１期生")\
                                          |Q(category__GenName="２期生")\
                                          |Q(category__GenName="ホロライブゲーマーズ")).distinct()
  
  context["JPall_2"] = hololiveChannel2.objects.filter(Q(category__GenName="３期生")\
                                          |Q(category__GenName="４期生")\
                                          |Q(category__GenName="５期生")\
                                          |Q(category__GenName="秘密結社holoX")).distinct()
  
  context["ENall"] =  hololiveChannel2.objects.filter(Q(category__GenName="Myth")\
                                          |Q(category__GenName="Project: HOPE")\
                                          |Q(category__GenName="Council")).distinct()
  
  context["IDall"] = hololiveChannel2.objects.filter(Q(category__GenName="１期生(ID)")\
                                          |Q(category__GenName="２期生(ID)")\
                                          |Q(category__GenName="３期生(ID)")).distinct()
  
  exTalents = hololiveChannel2.objects.filter(category__GenName="卒業生()").distinct()
  
  context["autoTest"] = AutoChannel.objects.all()#.filter(category__GenName="Auto0期生")
  
  context["exTalents"] = exTalents
  context["exChannelId"] = [ex.channelId for ex in exTalents]

  return context

class TopView(ListView):#トップVideoInfoページのView LoginRequiredMixin, 
  template_name = 'hololiveRankingApp/top.html'
  # login_url = 'login'
  model = hololiveChannel2
  context_object_name = "channelLists"
  queryset=hololiveChannel2.objects.all()
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    context["months"] = [x+1 for x in range(0,12)]
    context["years"] = [x for x in range(2017,int(dtstr[0:4])+1)]
  
    context["JPall"] = hololiveChannel2.objects.filter(Q(category__GenName="０期生")\
                                            |Q(category__GenName="１期生")\
                                            |Q(category__GenName="２期生")\
                                            |Q(category__GenName="ホロライブゲーマーズ")\
                                            |Q(category__GenName="３期生")\
                                            |Q(category__GenName="４期生")\
                                            |Q(category__GenName="５期生")\
                                            |Q(category__GenName="秘密結社holoX")).distinct()
    
    context["ENall"] =  hololiveChannel2.objects.filter(Q(category__GenName="Myth")\
                                            |Q(category__GenName="Project: HOPE")\
                                            |Q(category__GenName="Council")).distinct()
    
    context["IDall"] = hololiveChannel2.objects.filter(Q(category__GenName="１期生(ID)")\
                                            |Q(category__GenName="２期生(ID)")\
                                            |Q(category__GenName="３期生(ID)")).distinct()
    
    context["gen0JPs"] = hololiveChannel2.objects.filter(category__GenName="０期生")
    context["gen1JPs"] = hololiveChannel2.objects.filter(category__GenName="１期生")
    context["gen2JPs"] = hololiveChannel2.objects.filter(category__GenName="２期生")
    context["gameJPs"] = hololiveChannel2.objects.filter(category__GenName="ホロライブゲーマーズ")
    context["gen3JPs"] = hololiveChannel2.objects.filter(category__GenName="３期生")
    context["gen4JPs"] = hololiveChannel2.objects.filter(category__GenName="４期生")
    context["gen5JPs"] = hololiveChannel2.objects.filter(category__GenName="５期生")
    context["holoXs"] = hololiveChannel2.objects.filter(category__GenName="秘密結社holoX")
    
    context["myths"] = hololiveChannel2.objects.filter(category__GenName="Myth")
    context["projectHOPEs"] = hololiveChannel2.objects.filter(category__GenName="Project: HOPE")
    context["councils"] = hololiveChannel2.objects.filter(category__GenName="Council")
    context["gen1IDs"] = hololiveChannel2.objects.filter(category__GenName="１期生(ID)")
    context["gen2IDs"] = hololiveChannel2.objects.filter(category__GenName="２期生(ID)")
    context["gen3IDs"] = hololiveChannel2.objects.filter(category__GenName="３期生(ID)")
    
    
    
    
    context["channnels"] = hololiveChannel2.objects.all()#.order_by("")
    context["lyricists"] = Lyricist.objects.all().order_by("lyricist__name")[0:]
    context["composers"] = Composer.objects.all().order_by("composer__name")[0:]
    context["arrangers"] = Arranger.objects.all().order_by("arranger__name")[0:]
    context["mixers"] = Mixer.objects.all().order_by("mixer__name")[0:]
    context["musicians"] = Musician.objects.all().order_by("musician__name")[0:]
    context["videoEditors"] = VideoEditor.objects.all().order_by("videoEditor__name")[0:]
    context["illustrators"] = Illustrator.objects.all().order_by("illustrator__name")[0:]
    context["coStars"] = CoStar.objects.all().order_by("coStar__name")[0:]
    context["originalSingers"] = OriginalSinger.objects.all().order_by("originalSinger__name")[0:]
    
    dtLatest = hololiveSongsResult.objects.all()\
      .aggregate(Max("aggregationDate"))["aggregationDate__max"]

    weeklyKanji = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]
    weekEnglish = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    def minusCalcDt(base, x):#
      minusDt = base - datetime.timedelta(days=x)
      DOW_ja = weeklyKanji[minusDt.weekday()]
      DOW_en = weekEnglish[minusDt.weekday()]
      
      return minusDt, DOW_ja, DOW_en

    baseDt = dt
    weekList = []        
    for i in range(0,7):
      minusDt, DOW_ja, DOW_en = minusCalcDt(dtLatest, i)
      minusDtStr = minusDt.strftime("%Y-%m-%d")
      if minusDt == baseDt:
        weekList.append(["今日", minusDt, DOW_ja, DOW_en, f"{minusDtStr}{DOW_en}", minusDtStr])
      elif minusDt == baseDt - datetime.timedelta(days=1):
        weekList.append(["昨日", minusDt, DOW_ja, DOW_en, f"{minusDtStr}{DOW_en}", minusDtStr])
      elif minusDt == baseDt - datetime.timedelta(days=2):
        weekList.append(["一昨日", minusDt, DOW_ja, DOW_en, f"{minusDtStr}{DOW_en}", minusDtStr])
      else:
        weekList.append(["最新", minusDt, DOW_ja, DOW_en, f"{minusDtStr}{DOW_en}", minusDtStr])
        
    context["weekList"] = weekList
    
    # context['results'] = hololiveSongsResult.objects.filter(info=self.get_object()).order_by("aggregationDate")[0:50]
    return context
  
class Login(LoginView):
  template_name = 'hololiveRankingApp/user/login.html'
  form_class = LoginForm
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context
    
class Logout(LogoutView):
  template_name = 'hololiveRankingApp/user/logout.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context
  
class UserCreateView(CreateView):
  template_name = 'hololiveRankingApp/user/create.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('top')

##########################################

class VideoInfoCreateView(CreateView):
  model = VideoInfo
  template_name = 'hololiveRankingApp/video/create.html'
  
  fields = ["performer","title","videoId"] #"fields = '__all__'
  success_url = reverse_lazy("list")
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context

class AdminVideoInfoCreateView(CreateView):
  model = VideoInfo
  template_name = 'hololiveRankingApp/video/create.html'
  
  fields = '__all__'
  success_url = reverse_lazy("list")
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context

class LyricistAddView(CreateView):
  model = Lyricist
  form_class = LyricistAddForm
  concerned = "Lyricist"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class ComposerAddView(CreateView):
  model = Composer
  form_class = ComposerAddForm
  concerned = "Composer"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class ArrangerAddView(CreateView):
  model = Arranger
  form_class = ArrangerAddForm
  concerned = "Arranger"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context

class MixerAddView(CreateView):
  model = Mixer
  form_class = MixerAddForm
  concerned = "Mixer"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class MusicianAddView(CreateView):
  model = Musician
  form_class = MusicianAddForm
  concerned = "Musician"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class VideoEditorAddView(CreateView):
  model = VideoEditor
  form_class = VideoEditorAddForm
  concerned = "VideoEditor"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class IllustratorAddView(CreateView):
  model = Illustrator
  form_class = IllustratorAddForm
  concerned = "Illustrator"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class CoStarAddView(CreateView):
  model = CoStar
  form_class = CoStarAddForm
  concerned = "CoStar"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class OriginalSingerAddView(CreateView):
  model = OriginalSinger
  form_class = OriginalSingerAddForm
  concerned = "OriginalSinger"
  template_name = 'hololiveRankingApp/concerned/create.html'
  
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["concerned"] = self.concerned
    return context
  
class ConcernedCreateView(CreateView):
  model = AnotherPerson
  template_name = 'hololiveRankingApp/video/add.html'
  fields = '__all__'
  # success_url = reverse_lazy("list")
  def get_success_url(self):
    return reverse('update', kwargs={'pk': self.kwargs['redirectPk']})#成功
      
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["redirectPk"]
    vInfo = VideoInfo.objects.get(pk=self.kwargs["redirectPk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    return context

class VideoInfoListView(ListView):
  model = VideoInfo
  template_name = 'hololiveRankingApp/admin/list.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context

class WorkListView(ListView):#DetailView
  template_name = 'hololiveRankingApp/video/work.html'
  model = VideoInfo

  # context_object_name = "works"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    lyricist = self.request.GET.get("lyricist")
    composer = self.request.GET.get("composer")
    arranger = self.request.GET.get("arranger")
    mix = self.request.GET.get("mix")
    inst = self.request.GET.get("inst")
    movie = self.request.GET.get("movie")
    illust = self.request.GET.get("illust")
    coStar = self.request.GET.get("coStar")
    originalSinger = self.request.GET.get("originalSinger")
    
    if lyricist is not None:
      context["name"] = lyricist
      context["charge"] = "作詞家"
    elif composer is not None:
      context["name"] = composer
      context["charge"] = "作曲家"
    elif arranger is not None:
      context["name"] = arranger
      context["charge"] = "編曲家"
    elif mix is not None:
      context["name"] = mix
      context["charge"] = "ミックス"
    elif inst is not None:
      context["name"] = inst
      context["charge"] = "楽器担当"
    elif movie is not None:
      context["name"] = movie
      context["charge"] = "編集者"
    elif illust is not None:
      context["name"] = illust
      context["charge"] = "イラストレーター"
    elif coStar is not None:
      context["name"] = coStar
      context["charge"] = "共演者"
    elif originalSinger is not None:
      context["name"] = originalSinger
      context["charge"] = "歌い手"

    return context
  
  def get_queryset(self):
    lyricist = self.request.GET.get("lyricist")
    composer = self.request.GET.get("composer")
    arranger = self.request.GET.get("arranger")
    mix = self.request.GET.get("mix")
    inst = self.request.GET.get("inst")
    movie = self.request.GET.get("movie")
    illust = self.request.GET.get("illust")
    coStar = self.request.GET.get("coStar")
    originalSinger = self.request.GET.get("originalSinger")
    
    if lyricist is not None:
      queryset = self.model.objects.filter(lyricist__lyricist__name=lyricist) 
    elif composer is not None:
      queryset = self.model.objects.filter(composer__composer__name=composer)
    elif arranger is not None:
      queryset = self.model.objects.filter(arranger__arranger__name=arranger)
    elif mix is not None:
      queryset = self.model.objects.filter(mix__mixer__name=mix)
    elif inst is not None:
      queryset = self.model.objects.filter(inst__musician__name=inst)
    elif movie is not None:
      queryset = self.model.objects.filter(movie__videoEditor__name=movie)
    elif illust is not None:
      queryset = self.model.objects.filter(illust__illustrator__name=illust)
    elif coStar is not None:
      queryset = self.model.objects.filter(coStar__coStar__name=coStar)
    elif originalSinger is not None:
      queryset = self.model.objects.filter(originalSinger__originalSinger__name=originalSinger)
    return queryset
    
class VideoUpdateView(UpdateView):
  model = VideoInfo
  form_class = VideoInfoForm
  template_name = 'hololiveRankingApp/update.html'
  def get_success_url(self):
    return reverse("video_info", kwargs={"pk": self.kwargs["pk"]})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["pk"]
    vInfo = self.model.objects.get(pk=self.kwargs["pk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["people"] = AnotherPerson.objects.all().order_by("name")
    
    return context
  
class AdminVideoUpdateView(UpdateView):
  model = VideoInfo
  form_class = AdminVideoInfoForm
  template_name = 'hololiveRankingApp/admin/update.html'

  def get_success_url(self):
    return reverse("list")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["pk"]
    vInfo = self.model.objects.get(pk=self.kwargs["pk"])
    context["title"] = vInfo.title
    context["description"] = vInfo.description
    context["people"] = AnotherPerson.objects.all().order_by("name")
    
    return context
  
class AdminTitleView(UpdateView):
  model = VideoInfo
  form_class = AdminTitleForm
  template_name = 'hololiveRankingApp/admin/title.html'

  def get_success_url(self):
    return reverse("list")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    context["pk"] = self.kwargs["pk"]
    vInfo = self.model.objects.get(pk=self.kwargs["pk"])
    context["title"] = vInfo.title

    return context

class VideoInfoView(DetailView):#個々の動画情報を表示する
  template_name = 'hololiveRankingApp/video/info.html'
  model = VideoInfo
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    video_id = self.get_object().videoId
    path = self.request.path
    datetype = path.split("/")[-1]

    video_info = VideoInfo.objects.get(videoId=video_id)
    
    toDate = dt
    latestCheck = hololiveSongsResult.objects.filter(aggregationDate=dt).count()
    if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
      theDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      toDate = theDayBefore
      
    def makeGraph(x,y):
      if x == 0:
        fromDate = video_info.videoAge
      else:
        fromDate = toDate - datetime.timedelta(days=x)
      song_results = hololiveSongsResult.objects.filter(info=video_info,\
                                                        aggregationDate__gt=fromDate,\
                                                        aggregationDate__lt=toDate)\
                                                .order_by('aggregationDate')
      date = [song_result.aggregationDate for song_result in song_results]
      view_counts = [song_result.viewCount for song_result in song_results]
      like_counts = [song_result.likeCount for song_result in song_results]
      view_counts7 = [song_result.viewCount7 for song_result in song_results]
      like_counts7 = [song_result.likeCount7 for song_result in song_results]
      view_counts30 = [song_result.viewCount30 for song_result in song_results]
      like_counts30 = [song_result.likeCount30 for song_result in song_results]
      if x == 0:
        if y == "view": 
          return date, view_counts
        if y == "like":
          return date, like_counts
      elif x == 7:
        if y == "view": 
          return date, view_counts7
        if y == "like":
          return date, like_counts7
      elif x == 30:
        if y == "view": 
          return date, view_counts30
        if y == "like":
          return date, like_counts30
    
    context['results'] = hololiveSongsResult.objects.filter(info=self.get_object())\
                                                    .order_by("-aggregationDate")[0:50]
    
    date, view_counts = makeGraph(0,"view")
    context['viewgraph'] = self.create_graph(date, view_counts, video_info.title)
    date, like_counts = makeGraph(0,"like")
    context['likegraph'] = self.create_graph(date, like_counts, video_info.title)
    date7, view_counts7 = makeGraph(7,"view")
    context['viewgraph7'] = self.create_graph_bar(date7, view_counts7, video_info.title)
    date, like_counts7 = makeGraph(7,"like")
    context['likegraph7'] = self.create_graph_bar(date, like_counts7, video_info.title)
    date30, view_counts30 = makeGraph(30,"view")
    context['viewgraph30'] = self.create_graph_bar(date30, view_counts30, video_info.title)
    date, like_counts30 = makeGraph(30,"like")
    context['likegraph30'] = self.create_graph_bar(date, like_counts30, video_info.title)
    return context
    
  def output_graph(self):#グラフ画像の文字コードや拡張子ファイル設定
    buffer = BytesIO()
    pyplot.savefig(buffer, format="png")
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


  def create_graph(self, x, y, videoTitle):#描図や軸ラベル、デザイン等の設定
    #Anti-Grain Geometry (AGG) is a 2D rendering graphics library written in C++.
    #We must specify Filetypes by png
    pyplot.switch_backend("AGG")
    # 描画先を作成
    # pyplot.figure(figsize=(8, 6))#800x600 デフォルトで640x480
    pyplot.plot(x,y)
    # pyplot.text(x,y)
    pyplot.xticks(rotation=20)
    pyplot.title(f"{videoTitle}", fontsize=15)
    pyplot.xlabel("日にち(直線部分は平均値)", fontsize=15)
    pyplot.ylabel("ViewCount", fontsize=15)
    
    pyplot.grid()
    pyplot.tight_layout()
    graph = self.output_graph()
    return graph
  
  def create_graph_bar(self, x, y, videoTitle):#描図や軸ラベル、デザイン等の設定
    pyplot.switch_backend("AGG")
    # pyplot.figure(figsize=(10,5))
    pyplot.bar(x,y)
    pyplot.xticks(rotation=20)
    pyplot.title(f"{videoTitle}", fontsize=15)
    pyplot.xlabel("日にち", fontsize=15)
    pyplot.ylabel("Count", fontsize=15)
    pyplot.tight_layout()
    graph = self.output_graph()
    return graph


class SearchResultView(ListView):

  model = hololiveSongsResult
  template_name = "hololiveRankingApp/rankingResult.html"
  context_object_name = "songLists"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    if "total" in self.request.GET.getlist("dateType"):
      context["dateType"] = "total"
    elif "weekly" in self.request.GET.getlist("dateType"):
      context["dateType"] = "weekly"
    elif "monthly" in self.request.GET.getlist("dateType"):
      context["dateType"] = "monthly"
  ########################################################################
    targetIdLists = self.request.GET.getlist("targetChannelId")
    Q_Performer = self.model.objects.filter(info__performer__channelId__in=targetIdLists).distinct()
    original = videoTypeJudgement.objects.get(judge="オリジナルソング")
    covered = videoTypeJudgement.objects.get(judge="歌ってみた")
    festival = videoTypeJudgement.objects.get(judge="記念祭")
    
    Q_SongType = Q_Performer
    context["SongType"] = []                                   
    if "original" in self.request.GET.getlist("targetSongType"):
      #オリジナル
      Q_SongType = Q_Performer.filter(info__videoType=original)
      context["SongType"].append("オリジナルソング")
    if "covered" in self.request.GET.getlist("targetSongType"):
      #歌ってみた
      Q_SongType = Q_Performer.filter(info__videoType=covered)
      context["SongType"].append("カバーソング")
      #withオリジナル
      if "original" in self.request.GET.getlist("targetSongType"):
        Q_Original = Q_Performer.filter(info__videoType=original)
        Q_SongType = Q_SongType|Q_Original
        
    if "festival" in self.request.GET.getlist("targetSongType"):
      #記念祭
      context["SongType"].append("記念祭")
      Q_SongType = Q_Performer.filter(info__videoType=festival)
      #withオリジナル
      if "original" in self.request.GET.getlist("targetSongType"):
        Q_Original = Q_Performer.filter(info__videoType=original)
        Q_SongType = Q_SongType|Q_Original
      #with歌ってみた
      if "covered" in self.request.GET.getlist("targetSongType"):
        Q_Covered = Q_Performer.filter(info__videoType=covered)
        Q_SongType = Q_SongType|Q_Covered

    resultMount=5
    baseDate = dt
    
    latestCheck = self.model.objects.filter(aggregationDate=dt).count()
    if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
      theDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      baseDate = theDayBefore
    
    randomInfos = hololiveSongsResult.objects.filter(aggregationDate=baseDate).values("info")
    
    HttpVideo = "https://www.youtube.com/watch?v="
    HttpsJPG = "https://i.ytimg.com/vi/"
    baseJPG = "/hqdefault.jpg"
    randomLists = [dat["info"] for dat in randomInfos]
    randomVideos = [{"title":VideoInfo.objects.get(id=randomInfo).title,
                     "videoId":VideoInfo.objects.get(id=randomInfo).videoId,
                     "videoURL":HttpVideo+VideoInfo.objects.get(id=randomInfo).videoId,
                     "videoJPG":HttpsJPG+VideoInfo.objects.get(id=randomInfo).videoId+baseJPG}\
                    for randomInfo in random.sample(randomLists, resultMount)]

    context["randomVideos"] = randomVideos
    context["oneWeekAgo"] = baseDate - datetime.timedelta(days=7)   
    
    return context
  
  def get_queryset(self):
    targetIdLists = self.request.GET.getlist("targetChannelId")
    Q_Performer = self.model.objects.filter(info__performer__channelId__in=targetIdLists).distinct()
    
    original = videoTypeJudgement.objects.get(judge="オリジナルソング")
    covered = videoTypeJudgement.objects.get(judge="歌ってみた")
    festival = videoTypeJudgement.objects.get(judge="記念祭")

    Days = self.request.GET.getlist("DOW")
    
    if dtstr in Days:
      Q_Date = Q_Performer.filter(aggregationDate=dt)
    else:
      Q_Date = Q_Performer.filter(aggregationDate=Days[0])    
                                                
    Q_SongType = Q_Date                                   
    if "original" in self.request.GET.getlist("targetSongType"):
      #オリジナル
      Q_SongType = Q_Date.filter(info__videoType=original)
    if "covered" in self.request.GET.getlist("targetSongType"):
      #歌ってみた
      Q_SongType = Q_Date.filter(info__videoType=covered)
      #withオリジナル
      if "original" in self.request.GET.getlist("targetSongType"):
        Q_Original = Q_Date.filter(info__videoType=original)
        Q_SongType = Q_SongType|Q_Original
    if "festival" in self.request.GET.getlist("targetSongType"):
      #記念祭
      Q_SongType = Q_Date.filter(info__videoType=festival)
      #withオリジナル
      if "original" in self.request.GET.getlist("targetSongType"):
        Q_Original = Q_Date.filter(info__videoType=original)
        Q_SongType = Q_SongType|Q_Original
      #with歌ってみた
      if "covered" in self.request.GET.getlist("targetSongType"):
        Q_Covered = Q_Date.filter(info__videoType=covered)
        Q_SongType = Q_SongType|Q_Covered
      
    if "total" in self.request.GET.getlist("dateType"):
      
      if "likeCountDesc" in self.request.GET.getlist("orderType"):#Like987654321
        Q_DateType = Q_SongType.order_by("likeCount").reverse().distinct()
      elif "likeCountAsc" in self.request.GET.getlist("orderType"):#Like123456789
        Q_DateType = Q_SongType.order_by("likeCount").distinct()
      elif "viewCountDesc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount").reverse().distinct()
      elif "viewCountAsc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount").distinct()
      
    if "weekly" in self.request.GET.getlist("dateType"):
      
      if "likeCountDesc" in self.request.GET.getlist("orderType"):#Like987654321
        Q_DateType = Q_SongType.order_by("likeCount7").reverse().distinct()
      elif "likeCountAsc" in self.request.GET.getlist("orderType"):#Like123456789
        Q_DateType = Q_SongType.order_by("likeCount7").distinct()
      elif "viewCountDesc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount7").reverse().distinct()
      elif "viewCountAsc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount7").distinct()
      
    if "monthly" in self.request.GET.getlist("dateType"):
      
      if "likeCountDesc" in self.request.GET.getlist("orderType"):#Like987654321
        Q_DateType = Q_SongType.order_by("likeCount30").reverse().distinct()
      elif "likeCountAsc" in self.request.GET.getlist("orderType"):#Like123456789
        Q_DateType = Q_SongType.order_by("likeCount30").distinct()
      elif "viewCountDesc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount30").reverse().distinct()
      elif "viewCountAsc" in self.request.GET.getlist("orderType"):
        Q_DateType = Q_SongType.order_by("viewCount30").distinct()
        
    
    
    Q_optimization = Q_DateType.select_related('info')\
                              .prefetch_related('info__performer')\
                              .prefetch_related('info__lyricist__lyricist')\
                              .prefetch_related('info__composer__composer')\
                              .prefetch_related('info__arranger__arranger')\
                              .prefetch_related('info__mix__mixer')\
                              .prefetch_related('info__inst__musician')\
                              .prefetch_related('info__movie__videoEditor')\
                              .prefetch_related('info__illust__illustrator')\
                              .prefetch_related('info__coStar__coStar')\
                              .prefetch_related('info__originalSinger__originalSinger')
    
    targetLyricist = self.request.GET.getlist("checkbox_lyricist")
    targetComposer = self.request.GET.getlist("checkbox_composer")
    targetArranger = self.request.GET.getlist("checkbox_arranger")
    targetMixer = self.request.GET.getlist("checkbox_mixer")
    targetMusician = self.request.GET.getlist("checkbox_musician")
    targetVideoEditor = self.request.GET.getlist("checkbox_videoEditor")
    targetIllustrator = self.request.GET.getlist("checkbox_illustrator")
    targetCoStar = self.request.GET.getlist("checkbox_coStar")
    targetOriginalSinger = self.request.GET.getlist("checkbox_originalSinger")

    Q_Concerned = Q_optimization.exclude(info__lyricist__pk__in=targetLyricist)\
                                .exclude(info__composer__pk__in=targetComposer)\
                                .exclude(info__arranger__pk__in=targetArranger)\
                                .exclude(info__mix__pk__in=targetMixer)\
                                .exclude(info__inst__pk__in=targetMusician)\
                                .exclude(info__movie__pk__in=targetVideoEditor)\
                                .exclude(info__illust__pk__in=targetIllustrator)\
                                .exclude(info__coStar__pk__in=targetCoStar)\
                                .exclude(info__originalSinger__pk__in=targetOriginalSinger)
    Q_year = Q_Concerned
    
    years = [str(x) for x in range(2017,int(dtstr[0:4])+1)]
    for year in years:
      if year in self.request.GET.getlist("checkbox_year"):
        Q_year = Q_year.exclude(info__videoAge__year=year)
    
    Q_month = Q_year
      
    months = [str(x+1) for x in range(0,12)]
    for month in months:
      if month in self.request.GET.getlist("checkbox_month"):
        Q_month = Q_month.exclude(info__videoAge__month=month)
    
    queryset = Q_month
    
    return queryset