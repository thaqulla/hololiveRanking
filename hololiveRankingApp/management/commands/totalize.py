from django.core.management.base import BaseCommand
from hololiveRankingApp.models import VideoInfo, hololiveSongsResult,\
    videoTypeJudgement, Lyricist, Composer, Arranger, Mixer, Musician, VideoEditor,\
    Illustrator, CoStar, OriginalSinger, hololiveChannel2, AutoChannel,AnotherPerson
from hololiveRankingApp.management.commands import main
import datetime
import pandas as pd
import numpy as np
from django.db.models import Max, Min
import operator, os
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm
import pickle
from django.db.models import Q
import random
import cnum#兆億万一分厘毛忽

with open('./SECRET/API_KEYs.txt', 'r', encoding='UTF-8') as f:
    API_KEY_Lists = f.read().splitlines()
API_KEY = API_KEY_Lists[0]
with open('./TXT/AmanualInputVideoIds.txt', 'r', encoding='UTF-8') as f:
    videoId_Lists = f.read().splitlines()

dt = datetime.date.today()  # ローカルな現在の日付を取得
dtstr = dt.strftime("%Y-%m-%d")
dt7 = dt - datetime.timedelta(days=7)

path = "./CSV"
if os.path.exists(path) != 1:
    os.makedirs(path)

dt0 = (dt - datetime.date(1899, 12, 31)).days + 1 #serial値　int型

maxPkRslt = hololiveSongsResult.objects.exclude(viewCount30=0)\
                                       .aggregate(Max("pk"))["pk__max"]
maxInfo = VideoInfo.objects.all().aggregate(Max("pk"))["pk__max"]

class Command(BaseCommand):
    help = "テストコマンド"
    keyword = "music|オリジナル|歌|歌ってみた|cover|踊ってみた|song|sing|MV|strOriginal|曲|official"
    maxresults = 50#数字に限らず一回で200超のAPIリクエストが行われた
    moduleNumber = 3
    autoModuleNumber = 3

    def add_arguments(self, parser):
        pass
    
    
    def handle(self, *args, **options):#handleは変えては駄目。
                                    #前後に何があっても一番初めに実行される
        ##########################################################
        existCheck = hololiveSongsResult.objects.filter(aggregationDate=dt)
        if existCheck.count() != 0:
            maxPkRslt2 = existCheck.exclude(Q(viewCount30=0)|\
                                            Q(viewCount=0, likeCount=0))\
                                   .aggregate(Max("pk"))["pk__max"]#
            dat2 = hololiveSongsResult.objects.get(pk=maxPkRslt2)
            print(dat2.pk, dat2.info,
                  f"集計日:{dat2.aggregationDate}",
                  f"総合:{dat2.viewCount}",
                  f"週間:{dat2.viewCount7}",
                  f"月間:{dat2.viewCount30} is uploaded")
            try:
                # main.makeCompleteData2(API_KEY)
                main.manualAdd(API_KEY)#95s7KabUo8A 以降が一部不完全
                
            #進捗状況の確認(「木の芽時の空 - 路地裏ロジック」を選択中)
            except KeyboardInterrupt:
                selectDataAll = hololiveSongsResult.objects.filter(
                    info__videoId="BvlCYJ1XZ3Y").order_by("aggregationDate")
                for selectDat in selectDataAll:
                    print(selectDat.pk,selectDat.aggregationDate,
                        selectDat.info.title,selectDat.info.videoId,
                        selectDat.viewCount,selectDat.likeCount,
                        selectDat.viewCount7,selectDat.likeCount7,
                        selectDat.viewCount30,selectDat.likeCount30)
        else:
            #動画のデータ収集&整理
            main.collectVideoInfo(API_KEY, dt0, self.keyword,
                                  self.autoModuleNumber, self.moduleNumber,
                                  self.maxresults, maxPkRslt)
            
        ##################今は絶対回すな###########################
        # main.songTypeJudge(API_KEY_Lists[0],maxPkInfo)
        ##########################################################
        incomp = VideoInfo.objects.prefetch_related("performer").get(id=7617)#7617
        all = incomp.performer.all()
        # if all.count()==0:
        #     print("aa")
        # incompC = VideoInfo.objects.prefetch_related("composer").get(id=5266)#7617
        # cll = incompC.composer.all()
        print([datum.name for datum in all])
        # print([datum.composer.name for datum in cll])
        
        # baseDate = dt
        # latestCheck = hololiveSongsResult.objects.filter(aggregationDate=dt).count()
        # if latestCheck == 0: #本日分が計算されていない場合最新分を基準に算出される
        #     thaDayBefore = hololiveSongsResult.objects.all().aggregate(Max('aggregationDate'))["aggregationDate__max"]
        #     baseDate = thaDayBefore
        # test = hololiveSongsResult.objects.filter(aggregationDate=baseDate,info__lyricist__lyricist__pk=7).distinct()
        
        # print(test)
        
        # querysetAll = VideoInfo.objects.filter(composer__composer__pk=7).distinct().order_by("-pk")
        # print([[datum.title,datum.videoId] for datum in querysetAll])
        

       
        #not_inputed = SakushikaModlel.objects.get(pk=[0:未記入の作詞家モデルとしてのpk(not AnotherPersonのpk)])
        #VideoInfo.objects.sakusika.remove(not_inputed)
        
        
        # double01 = VideoInfo.objects.filter(mix__pk=4)
        # double02 = VideoInfo.objects.filter(mix__pk=14)
        # for mi in double01:
        #     print(mi.title,mi.pk)
        # print("2222222222222222222")
        # for mi in double02:
        #     print(mi.title,mi.pk)

        # 検索かけたいディレクトリに移動
        # cd path/to/my/dir/
        # ディレクトリ配下のすべてのファイルで スペルミスの文字列 (Lylic) を検索
        # grep -r Lylic ./
        