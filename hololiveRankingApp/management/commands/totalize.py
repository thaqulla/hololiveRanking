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
                print("manualAdd")
            except ObjectDoesNotExist:
                print("ObjectDoesNotExist")
                main.getRankingTXT2(API_KEY)
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
        
        dataAge = hololiveSongsResult.objects.select_related('info')\
            .filter(viewCount30=0)\
            .order_by("pk")\
            .values_list('info__videoId', 'info__title', 'info__videoAge', flat=False)
        dataAgg = hololiveSongsResult.objects.select_related('info')\
            .filter(viewCount30=0)\
            .order_by("pk")\
            .values_list('info__videoId', 'info__title', "aggregationDate",  flat=False)
            
        
        print(len(list(set(dataAge))))
        print(len(list(set(dataAgg))))
        
        setData = set(list(dataAge)) ^ set(list(dataAgg))
        print(len(setData))
        
        trueIds = VideoInfo.objects\
                    .filter(videoCondition2=True)\
                    .values_list('videoId', flat=True)
        
        # for trueId in tqdm(trueIds):
        #     youtubeData = main.videoDetail2(trueId, API_KEY)
        #     getPrivacyStatus = youtubeData["status"]["privacyStatus"]
            
        #     if getPrivacyStatus == "unlisted":#限定公開なので非公開と同義と判断
        #         getVideoInfo = VideoInfo.objects.get(videoId=trueId)
        #         getVideoInfo.videoCondition2=False
        #         getVideoInfo.save()
        #         print("unlisted")

        print(trueIds)
            
        # print(list(trueIds))
        
        # test = [datum.composer.name for datum in Composer.objects.all()]
        # print(test)
        
        # test2 = Composer.objects.values_list('composer__name', flat=True)
        # print(list(test2))
        
        
        # print("getAutoResult2")
        # main.getAutoResult2(API_KEY, dt0, self.autoModuleNumber)
        # print("getDjangoResult2")
        # main.getDjangoResult2(self.keyword, self.maxresults, API_KEY, dt0, self.moduleNumber)

            #     starts = []
            #     for dat in noDataDate:
            #         if dat-1 not in noDataDate:
            #             start = dat - 1
            #         starts.append(start)
            #     # starts = [start for dat in noDataDate if dat-1 not in noDataDate:start=dat-1]
            #     ends = []
            #     for dat in reversed(noDataDate):
            #         if dat+1 not in noDataDate:
            #             end = dat + 1
            #         ends.insert(0,end)
            #     dfN = pd.DataFrame(noDataDate)
            #     dfS = pd.DataFrame(starts)
            #     dfE = pd.DataFrame(ends)
            #     df = pd.concat([dfN,dfS,dfE], axis=1)

            #     for dat in df.itertuples():
            #         x0 = vAge + datetime.timedelta(days=dat[1])
            #         x1 = vAge + datetime.timedelta(days=dat[2])
            #         x2 = vAge + datetime.timedelta(days=dat[3])
            #         x = (x2 - x1)/datetime.timedelta(days=1)
                    
            #         try:
            #             y1 = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x1)
            #             y2 = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x2)
            #         except ObjectDoesNotExist:
            #             dataAll = hololiveSongsResult.objects\
            #                 .filter(info__videoId=vid).order_by("aggregationDate")
            #             for i in dataAll:
            #                 print(i.pk, i.info.title,i.aggregationDate,i.viewCount,i.likeCount)
            #                 #おかしなデータを手動で削除
            #         except UnboundLocalError:
            #             errorVideo = VideoInfo.objects.get(videoId=vid)
            #             print(errorVideo.title,vid)
            #         Vaskew = (y2.viewCount - y1.viewCount)/x
            #         Laskew = (y2.likeCount - y1.likeCount)/x
            #         Vave = int(Vaskew*(dat[1]-dat[2])+y1.viewCount)
            #         Lave = int(Laskew*(dat[1]-dat[2])+y1.likeCount)
            #         # print(y1.pk, y1.info.title,y1.info.videoId,x0)
            #         songData = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x0)
            #         print(songData.pk, y1.info.title,y1.info.videoId,x0)
            #         if songData.viewCount == 0:
            #             songData.viewCount = Vave
            #             songData.likeCount = Lave
            #             songData.save()
        ##########################################################    
            
        # getData7AndData30(maxPkRslt)
        # print("getData7AndData30Old")
        # getData7AndData30Old()
        # print("makeCompleteData")
        # makeCompleteData(maxPkRslt,API_KEY)
        # print("flyingStartVideo")
        # flyingStartVideo_plusDescription(API_KEY)
        
        
        
    # print(videoList)
        
        
        
        
                    
                    
                    
                    
                    
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
        #TODO:ボトルネックの調査
        ##########################################################
        c_profile.disable()
        c_stats = pstats.Stats(c_profile)
        c_stats.sort_stats('tottime').print_stats(3)
        ##########################################################


        
