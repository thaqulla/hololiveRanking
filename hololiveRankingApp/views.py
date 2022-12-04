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

from .forms import LoginForm
from .models import VideoInfo, hololiveChannel2, hololiveSongsResult, \
  videoTypeJudgement, Lyricist,Composer,Arranger,Mixer,Musician,VideoEditor,\
  Illustrator,CoStar,OriginalSinger

from io import BytesIO
from matplotlib import pyplot
from tqdm import tqdm

import base64
import datetime
import japanize_matplotlib
import numpy as np
import pandas as pd
import random

dt = datetime.date.today()  # ローカルな現在の日付と時刻を取得
dtstr = dt.strftime("%Y-%m-%d")
  
def get_header_context_data(context):
  # context = super().get_context_data(**kwargs)
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
  
  exTalents = hololiveChannel2.objects.filter(category__GenName="卒業生()").distinct()
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
    
    context["months"] = [f"{x+1}月" for x in range(0,12)]
    context["years"] = [f"{x}年" for x in range(2017,int(dtstr[0:4])+1)]
  
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
    # context['results'] = hololiveSongsResult.objects.filter(info=self.get_object()).order_by("aggregationDate")[0:50]
    return context
  
class Login(LoginView):
  template_name = 'hololiveRankingApp/login.html'
  form_class = LoginForm
    
class Logout(LogoutView):
  template_name = 'hololiveRankingApp/logout.html'
  
class UserCreateView(CreateView):
  template_name = 'hololiveRankingApp/user_create.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('top')

##########################################

class VideoInfoCreateView(CreateView):
  
  model = VideoInfo
  template_name = 'hololiveRankingApp/create.html'
  
  fields = ["performer","title","videoId"]#"__all__"
  success_url = reverse_lazy("list") 

class VideoInfoListView(ListView):
  model = VideoInfo
  template_name = 'hololiveRankingApp/list.html'
  
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    
    # nameList = self.model.objects.get(pk=5266).performer.values("name")
    # context["performer"] = [dat["name"] for dat in nameList]
    # context["performers"] = self.model.objects.get(pk=5266).performer.values("name")
    return context

class WorkListView(ListView):#DetailView
  template_name = 'hololiveRankingApp/work.html'
  model = VideoInfo
  
  # context_object_name = "works"
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    context['lyricist'] = self.request.GET.get("lyricist")
    context['composer'] = self.request.GET.get("composer")
    context['arranger'] = self.request.GET.get("arranger")
    context['mix'] = self.request.GET.get("mix")
    context['inst'] = self.request.GET.get("inst")
    context['movie'] = self.request.GET.get("movie")
    context['illust'] = self.request.GET.get("illust")
    context['coStar'] = self.request.GET.get("coStar")
    context['originalSinger'] = self.request.GET.get("originalSinger")
    
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
      return queryset
    elif composer is not None:
      queryset = self.model.objects.filter(composer__composer__name=composer)
      return queryset
    elif arranger is not None:
      queryset = self.model.objects.filter(arranger__arranger__name=arranger)
      return queryset
    elif mix is not None:
      queryset = self.model.objects.filter(mix__mixer__name=mix)
      return queryset
    elif inst is not None:
      queryset = self.model.objects.filter(inst__musician__name=inst)
      return queryset
    elif movie is not None:
      queryset = self.model.objects.filter(movie__videoEditor__name=movie)
      return queryset
    elif illust is not None:
      queryset = self.model.objects.filter(illust__illustrator__name=illust)
      return queryset
    elif coStar is not None:
      queryset = self.model.objects.filter(coStar__coStar__name=coStar)
      return queryset
    elif originalSinger is not None:
      queryset = self.model.objects.filter(originalSinger__originalSinger__name=originalSinger)
      return queryset
    
class VideoUpdateView(UpdateView):
  model = VideoInfo
  fields = ["lyricist","composer","arranger","mix","inst","movie","illust","coStar","originalSinger"]
  template_name = 'hololiveRankingApp/update.html'
  
  ordering = '-name'
  # def get_success_url(self):
    # return reverse("video_info", kwargs={"pk": self.kwargs["pk"]})
    # def get_absolute_url(self):
    #   return reverse('video_info', kwargs={'pk' : self.kwargs["pk"]})
  success_url = reverse_lazy('list')
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    return context

class VideoInfoView(DetailView):#個々の動画情報を表示する
  template_name = 'hololiveRankingApp/video_info.html'
  model = VideoInfo
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    
    video_id = self.get_object().videoId
    path = self.request.path
    datetype = path.split("/")[-1]

    video_info = VideoInfo.objects.get(videoId=video_id)
    
    # latestCheck = hololiveSongsResult.objects.filter(aggregationDate=dt).count()
    # if latestCheck != 0:#本日分が計算されている場合
    #   toDate = dt
    # else:#本日分が計算されていない場合昨日分を基準に算出される
    #   toDate = dt-datetime.timedelta(days=1)
    
    toDate = dt
    latestCheck = hololiveSongsResult.objects.filter(aggregationDate=dt).count()
    if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
      thaDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      toDate = thaDayBefore
      
    def makeGraph(x):
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
      # like_counts = [song_result.likeCount for song_result in song_results]
      
      return date, view_counts
    
    context['results'] = hololiveSongsResult.objects.filter(info=self.get_object())\
                                                    .order_by("-aggregationDate")[0:50]
    
    date, view_counts = makeGraph(0)
    context['mygraph'] = self.create_graph(date, view_counts, video_info.title)
    
    date7, view_counts7 = makeGraph(7)
    context['mygraph7'] = self.create_graph_bar(date7, view_counts7, video_info.title)
    
    date30, view_counts30 = makeGraph(30)
    context['mygraph30'] = self.create_graph_bar(date30, view_counts30, video_info.title)
    
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
    pyplot.title(f"View Count Graph {videoTitle}", fontsize=15)
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
    pyplot.title(f"View Count Graph {videoTitle}")
    pyplot.xlabel("Date")
    pyplot.ylabel("ViewCount")
    pyplot.tight_layout()
    graph = self.output_graph()
    return graph

###########################################
class RankingView(ListView):#
  template_name = 'hololiveRankingApp/hololivechannel_list.html'
  model = hololiveChannel2

class PerformerInfoView(DetailView):#
  template_name = 'hololiveRankingApp/performer_info.html'
  model = hololiveSongsResult
  context_object_name = "performerSongLists"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context = get_header_context_data(context)
    if "total" in self.request.GET.getlist("dateType"):
      context["dateType"] = "total"
    return context
  # def get_queryset(self):
  #   return 
    # queryset = 

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
    
    baseDate = dt
    latestCheck = self.model.objects.filter(aggregationDate=dt).count()
    if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
      thaDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      baseDate = thaDayBefore
    x,y=40,70
    xDay = baseDate - datetime.timedelta(days=x)#日前
    yDay = baseDate - datetime.timedelta(days=y)#日前
    xData = Q_SongType.filter(aggregationDate=xDay).values().order_by("-info_id")
    yData = Q_SongType.filter(aggregationDate=yDay).values().order_by("-info_id")
    
    xxxs = list(xData)
    yyys = list(yData)
    x_VandL = [[xxx["info_id"], xxx["viewCount"], xxx["likeCount"]] for xxx in xxxs]#データ多い
    y_VandL = [[yyy["info_id"], yyy["viewCount"], yyy["likeCount"]] for yyy in yyys]#データ少ない
    x_info_id = [xxx["info_id"] for xxx in xxxs]#info_id多い
    y_info_id = [yyy["info_id"] for yyy in yyys]#info_id少ない
    
    diff_list = list(set(x_info_id) ^ set(y_info_id))#info_id差分抽出
    addZero = [[info_id, 0, 0] for info_id in diff_list]#info_id差分0補完     
    z_VandL =sorted(addZero + y_VandL, reverse=True)#7391 7384 7373 7372...
    
    diff_matrix = np.array(x_VandL) - np.array(z_VandL)#NumPyで計算高速化 7391 7384 7373 7372...

    video_id_list = [xxx["info_id"] for xxx in xxxs]
    # df_title = pd.DataFrame(list(map(lambda num: VideoInfo.objects.get(pk=num).title, video_id_list)),columns=["title"],index=video_id_list)
    # df_videoId = pd.DataFrame(list(map(lambda num: VideoInfo.objects.get(pk=num).videoId, video_id_list)),columns=["videoId"],index=video_id_list)
    # df_diff = pd.DataFrame(diff_matrix,columns=["info0", "viewCount", "likeCount"],index=video_id_list)
    
    # df = pd.concat([df_title,df_videoId,df_diff], axis=1)
    # if "viewCountDesc" in self.request.GET.getlist("orderType"):
    #     df = df.sort_values("viewCount", ascending=False)#True:昇順、False:降順
    # elif "likeCountDesc" in self.request.GET.getlist("orderType"):
    #     df = df.sort_values("likeCount", ascending=False)
    # print(df)
    # context["titleRange"] = list(df["title"])
    # context["viewCountRanges"] = list(df["viewCount"])
    # context["likeCountRanges"] = list(df["likeCount"])
    
    resultMount=5
    baseDate = dt
    latestCheck = self.model.objects.filter(aggregationDate=dt).count()
    if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
      thaDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      baseDate = thaDayBefore
    
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
    # context["randomVid"] = ["abc","def","ghi"]
    context["randomVideos"] = randomVideos
    
    # context["doubleCheck"] = self.get_queryset(self)#重複を除外したい
    context["oneWeekAgo"] = baseDate - datetime.timedelta(days=7)
    ##############################################    
    
    return context
  
  def get_queryset(self):
    targetIdLists = self.request.GET.getlist("targetChannelId")
    Q_Performer = self.model.objects.filter(info__performer__channelId__in=targetIdLists).distinct()
    latestCheck = Q_Performer.filter(aggregationDate=dt).count()
    
    original = videoTypeJudgement.objects.get(judge="オリジナルソング")
    covered = videoTypeJudgement.objects.get(judge="歌ってみた")
    festival = videoTypeJudgement.objects.get(judge="記念祭")
    
    today = dt
    
    latestCheck = Q_Performer.filter(aggregationDate=dt).count()
    if latestCheck != 0:
      Q_Date = Q_Performer.filter(aggregationDate=today)
    else:
      # yesterday = dt-datetime.timedelta(days=1)
      thaDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
      Q_Date = Q_Performer.filter(aggregationDate=thaDayBefore)         
                                                
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
    
    # queryset = Q_DateType
    # return queryset
  
    queryset = Q_DateType.select_related(
      'info'
    ).prefetch_related(
      'info__performer'
    ).prefetch_related(
      'info__lyricist__lyricist'
    ).prefetch_related(
      'info__composer__composer'
    ).prefetch_related(
      'info__arranger__arranger'
    ).prefetch_related(
      'info__mix__mixer'
    ).prefetch_related(
      'info__inst__musician'
    ).prefetch_related(
      'info__movie__videoEditor'
    ).prefetch_related(
      'info__illust__illustrator'
    ).prefetch_related(
      'info__coStar__coStar'
    ).prefetch_related(
      'info__originalSinger__originalSinger'
    )
    return queryset