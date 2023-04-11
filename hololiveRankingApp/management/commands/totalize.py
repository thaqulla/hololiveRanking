from googleapiclient.discovery import build
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
    videoItitleLists = f.read().splitlines()

dt = datetime.date.today()  # ローカルな現在の日付を取得
dtstr = dt.strftime("%Y-%m-%d")
dt1 = dt - datetime.timedelta(days=1)
dtstr1 = dt.strftime("%Y-%m-%d")
dt7 = dt - datetime.timedelta(days=7)
dtstr7 = dt7.strftime("%Y-%m-%d")

path = "./CSV"
if os.path.exists(path) != 1:
    os.makedirs(path)

dt0 = (dt - datetime.date(1899, 12, 31)).days + 1 #serial値　int型

maxPkRslt = hololiveSongsResult.objects.exclude(viewCount30=0)\
                                       .aggregate(Max("pk"))["pk__max"]
maxInfo = VideoInfo.objects.all().aggregate(Max("pk"))["pk__max"]

class Command(BaseCommand):
    help = "テストコマンド"
    keyword = "music|オリジナル|歌|歌ってみた|cover|踊ってみた|song|sing|MV|Original|曲|official"
    maxresults = 50#数字に限らず一回で200超のAPIリクエストが行われた
    moduleNumber = 3
    autoModuleNumber = 3

    def add_arguments(self, parser):
        pass
    
    
    def handle(self, *args, **options):#handleは変えては駄目。
                                    #前後に何があっても一番初めに実行される
        
        
        existCheck = hololiveSongsResult.objects.filter(aggregationDate=dt)
        if existCheck.count() != 0:
            maxPkRslt2 = existCheck.exclude(Q(viewCount30=0)|\
                                            Q(viewCount=0, likeCount=0))\
                                   .aggregate(Max("pk"))["pk__max"]
            try:                       
                dat2 = hololiveSongsResult.objects.get(pk=maxPkRslt2)
                print(dat2.pk, dat2.info,
                    f"集計日:{dat2.aggregationDate}",
                    f"総合:{dat2.viewCount}",
                    f"週間:{dat2.viewCount7}",
                    f"月間:{dat2.viewCount30} is uploaded")
            
                # main.makeCompleteData2(API_KEY)
                main.manualAdd(API_KEY)#95s7KabUo8A 以降が一部不完全
                print("manualAdd2")
                # main.getData7AndData30Old()
                # print("makeCompleteData")
                # main.makeCompleteData(maxPkRslt,API_KEY)
                # print("flyingStartVideo")
                # main.flyingStartVideo_plusDescription(API_KEY)
                # print("ObjectDoesNotExist")
            except ObjectDoesNotExist:
                print("ObjectDoesNotExist")
                main.getRanking3(5, API_KEY)
                print("complementer0v3")
                main.complementer0v3()#存在しない日付に0補完
                print("complementerAve")
                main.complementerAve(maxPkRslt,1)#0:古い順1:新しい順2:ABC順3:ZYX順 新しいものしか埋められていない
                print("getData7AndData30")
                main.getData7AndData30(maxPkRslt)
                print("getData7AndData30Old")
                main.getData7AndData30Old()
                print("makeCompleteData")
                main.makeCompleteData(maxPkRslt,API_KEY)
                print("flyingStartVideo")
                main.flyingStartVideo_plusDescription(API_KEY)
                print("ObjectDoesNotExist")
                
        #     #進捗状況の確認(「木の芽時の空 - 路地裏ロジック」を選択中)
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
            # main.getRankingTXT2(API_KEY)
            main.collectVideoInfo(API_KEY, dt0, self.keyword,
                                    self.autoModuleNumber, self.moduleNumber,
                                    self.maxresults, maxPkRslt)
            main.manualAdd(API_KEY)
            
        ##########################################################
        #TODO:ボトルネックの調査
        ##########################################################
        import cProfile
        import pstats
        c_profile = cProfile.Profile()
        c_profile.enable()
        ##########################################################
        
        # dataAge = hololiveSongsResult.objects.select_related('info')\
        #     .filter(viewCount30=0)\
        #     .order_by("pk")\
        #     .values_list('info__videoId', 'info__title', 'info__videoAge', flat=False)
        # dataAgg = hololiveSongsResult.objects.select_related('info')\
        #     .filter(viewCount30=0)\
        #     .order_by("pk")\
        #     .values_list('info__videoId', 'info__title', "aggregationDate",  flat=False)
            
        
        # print(len(list(set(dataAge))))
        # print(len(list(set(dataAgg))))
        
        # setData = set(list(dataAge)) ^ set(list(dataAgg))
        # print(len(setData))
        
        
        # vids = VideoInfo.objects.exclude(lastUpdateDate=dt).order_by("-pk")\
        #     .values_list('videoId', 'title', flat=False)#flat=True
        # print(vids)

        getVideoInfo = VideoInfo.objects.get(videoId="NjtIAuZQN_E")
        condition = getVideoInfo.videoCondition2
        print(condition)
        
        # videoIds = VideoInfo.objects.filter(videoCondition2=True).exclude(lastUpdateDate=dt)\
        #         .values_list('videoId', flat=True)
        ##########################################################    
            
        # getData7AndData30(maxPkRslt)
        # print("getData7AndData30Old")
        # getData7AndData30Old()
        # print("makeCompleteData")
        # makeCompleteData(maxPkRslt,API_KEY)
        # print("flyingStartVideo")
        # flyingStartVideo_plusDescription(API_KEY)
        
        
            
        #TODO:ボトルネックの調査
        ##########################################################
        c_profile.disable()
        c_stats = pstats.Stats(c_profile)
        c_stats.sort_stats('tottime').print_stats(3)
        ##########################################################


        
