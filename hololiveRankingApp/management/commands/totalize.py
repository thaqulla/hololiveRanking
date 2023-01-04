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
            main.manualAdd(API_KEY)
            
        ##################今は絶対回すな###########################
        # main.songTypeJudge(API_KEY_Lists[0],maxPkInfo)
        ##########################################################
        test = [datum.composer.name for datum in Composer.objects.all()]
        print(test)
        
        test2 = Composer.objects.values_list('composer', flat=True)
        print(list(test2))
        
        

        # concerned = VideoInfo.objects.prefetch_related('lyricist__lyricist')\
        #                             .prefetch_related('composer__composer')\
        #                             .prefetch_related('arranger__arranger')\
        #                             .prefetch_related('mix__mixer')\
        #                             .prefetch_related('inst__musician')\
        #                             .prefetch_related('movie__videoEditor')\
        #                             .prefetch_related('illust__illustrator')\
        #                             .prefetch_related('coStar__coStar')\
        #                             .prefetch_related('originalSinger__originalSinger')
        # anotherAll = AnotherPerson.objects.all()
        # anotherPk = [datum.pk for datum in anotherAll]
        # print(anotherPk)
        # x = 61
        # anotherL = concerned.filter(Q(lyricist__lyricist__pk=x)|\
        #                           Q(composer__composer__pk=x)|\
        #                           Q(arranger__arranger__pk=x)|\
        #                           Q(mix__mixer__pk=x)|\
        #                           Q(inst__musician__pk=x)|\
        #                           Q(movie__videoEditor__pk=x)|\
        #                           Q(illust__illustrator__pk=x)|\
        #                           Q(coStar__coStar__pk=x)|\
        #                           Q(originalSinger__originalSinger__pk=x))
        # print(anotherL)#.count()==0
        # ageData = VideoInfo.objects.filter(videoAge__year="2017").order_by("-videoAge")
        # print(ageData)


        
