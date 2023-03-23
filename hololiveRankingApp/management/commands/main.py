from googleapiclient.discovery import build
from django.db.models import Q
from hololiveRankingApp.models import VideoInfo, hololiveSongsResult,\
    VideoInfo,AutoChannel,hololiveChannel2,videoTypeJudgement,\
    Lyricist, Composer, Arranger, Mixer, Musician, VideoEditor,\
    Illustrator, CoStar, OriginalSinger, hololiveChannel2, AutoChannel
from django.core.exceptions import ObjectDoesNotExist
import datetime, pickle, re, os, operator, math
import numpy as np
import pandas as pd
from tqdm import tqdm
from django.db.models import Max, Min

dt = datetime.date.today()  # ローカルな現在の日付と時刻を取得
dtstr = dt.strftime("%Y-%m-%d")
with open('./TXT/AmanualInputVideoIds.txt', 'r', encoding='UTF-8') as f:
    videoId_Lists = f.read().splitlines()

# path = "./CSV/"+dtstr
# if os.path.exists(path) != 1:
#     os.makedirs(path)

def countAndLikes(API_KEY, videoId):
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    statistics = youtube.videos().list(
    part = "statistics", 
    id = videoId,
    ).execute()["items"][0]["statistics"]

    return statistics

def countAndLikes3(API_KEY, videoId):
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    statistics = youtube.videos().list(
    part = "snippet,statistics", 
    id = videoId,
    ).execute()["items"][0]#["statistics"]

    return statistics

def autoDetail(channelId, API_KEY):
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.search().list(
    part = "snippet",
    channelId = channelId,
    order="date",
    type="video",
    maxResults = 50
    ).execute()
    return response["items"]

def videoDetail(videoId, API_KEY):#tag取得用
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.videos().list(
    part = "snippet",
    id = videoId,
    ).execute()
    return response["items"][0]["snippet"]

def details(maxResults, keyword, channelId, API_KEY, videoDuration, publishedAfter):
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.search().list(
    part = "snippet",
    channelId = channelId,
    q = keyword,
    order="date",
    type="video",
    maxResults = maxResults,
    videoDuration=videoDuration,
    publishedAfter=publishedAfter,
    ).execute()

    return response["items"]

def details2(API_KEY, channelId, maxResults, publishedAfter):
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.search().list(
        part = "snippet",
        channelId = channelId,
        order="date",
        type="video",
        maxResults=maxResults,
        publishedAfter=f"{publishedAfter}T00:00:00Z",
        ).execute()
    return response

def newRanking(API_KEY, keyword, maxresults, performers, performer2, publishedAfter):#新着動画の登録＆当日の情報記入
    orderAgeList =[]
    for dat in performers:#個々のVtuberの最新歌動画の日付を取得
        orderAgeList.append([dat.title,dat.videoId,dat.videoAge])
        updateDate = pd.DataFrame(data = orderAgeList,
                            columns = ["title","videoId","投稿日"])\
                            .sort_values("投稿日", ascending=False)\
                            .reset_index(drop=True)\
                            .iloc[0,2]
        
        settedDate = datetime.datetime.strptime(publishedAfter, '%Y-%m-%d').date()
        if (updateDate - settedDate)/datetime.timedelta(days=1) <= 0:
            # print(updateDate)#設定日以降に動画が投稿されている！
            updateDate = publishedAfter
        else: pass
    keyword = keyword
    channelId = performer2.channelId
    # videoList =[]
    videoLength =["short","medium"]
    for length in videoLength:
        tests = details(maxresults, keyword, channelId, API_KEY, length,f"{updateDate}T00:00:00Z")
        with open(f"./TXT/temporarily-test.txt", "wb") as f:
            pickle.dump(tests, f)
        with open(f"./TXT/temporarily-test.txt", "rb") as p:
            listData = pickle.load(p)

        for i, listDat in enumerate(listData):
            liveVideo = countAndLikes(API_KEY, listData[i]["id"]["videoId"])
            # print(listData[i]["id"]["videoId"])
            try:
                if liveVideo["viewCount"] != "0":#生放送予約動画を除外
                    if VideoInfo.objects.filter(videoId=listData[i]["id"]["videoId"]).exists():pass
                    else:VideoInfo.objects.create(
                        title=listData[i]["snippet"]["title"],
                        videoId=listData[i]["id"]["videoId"],
                        videoAge=listData[i]["snippet"]["publishedAt"][:10],
                        description=listData[i]["snippet"]["description"])
                        # videoList.append([listData[i]["snippet"]["title"],listData[i]["id"]["videoId"],listData[i]["snippet"]["publishedAt"][:10],listData[i]["snippet"]["description"]])
                        
            except KeyError:
                print(listData[i]["id"]["videoId"])#メンバーシップの可能性
    # print(videoList)
    
    
# def createData(channelModels, modNum, maxResults):
#     for channel in tqdm(channelModels.objects.all()):
#         modPk = operator.mod(channel.pk, modNum)#チャンネルのPK値でMOD計算
#         modSerial = operator.mod(dt0, modNum)#日付のシリアル値をMOD計算
#         if modPk == modSerial & channel.lastUpdateDate != dt:
#             listData = details2(API_KEY, channel.channelId, maxResults, dtstr7)

#             def createNew(x):
#                 dList = listData['items']
#                 videoId = dList[x]["id"]["videoId"]
#                 title = dList[x]["snippet"]["title"]
#                 default = dList[x]["snippet"]["thumbnails"]["default"]["url"]#wxh=120x90
#                 medium = dList[x]["snippet"]["thumbnails"]["medium"]["url"]#wxh=320x180
#                 high = dList[x]["snippet"]["thumbnails"]["high"]["url"]#wxh=480x360
#                 publishedAt = dList[x]["snippet"]["publishedAt"][:10]
                
#                 omitCheck = dList[x]["snippet"]["description"][-4:]
                
#                 if omitCheck == " ...":
#                     description = main.videoDetail(videoId, API_KEY)["description"]
#                 else:
#                     description = dList[x]["snippet"]["description"]
                    
#                 existence = VideoInfo.objects.filter(videoId=videoId).count()
#                 exclusions = ["(Instrumental","（Instrumental","(instrumental","（instrumental"]
#                 songType = True #True:歌 False:Instrumental
                
#                 for exc in exclusions:
#                     songType = songType and (exc not in title)
                    
#                 if songType is True and existence==0:#ここで新規を登録
#                     VideoInfo.objects.create(title=title,
#                                             videoId=videoId,
#                                             videoAge=publishedAt,
#                                             lastUpdateDate=dtstr,
#                                             description=description)
#                 # vInfo = [videoId, title, publishedAt, description, default, medium, high]
                
#                 # return vInfo
                        
#             cList = int(listData['pageInfo']['totalResults'])
#             vList = list(map(createNew, range(0, cList)))
#             #[videoId, title, publishedAt, description, default, medium, high]
#             img = thumbnails(channel.channelId, API_KEY)
#             channel.thumbnailDefault = img["default"]["url"]
#             channel.thumbnailMedium = img["medium"]["url"]
#             channel.thumbnailHigh = img["high"]["url"]
#             channel.lastUpdateDate = dt
#             channel.save()
#     return vList

def getRankingTXT(API_KEY):#日別結果の取得
    videoData = VideoInfo.objects.all()
    for dat in tqdm(videoData):   
        vInfo = VideoInfo.objects.filter(videoId=dat.videoId)
        for i in vInfo:
            if hololiveSongsResult.objects.filter(info=i,aggregationDate=dtstr).exists():
                i.lastUpdateDate=dtstr
                i.save()
            else:
                if i.videoCondition2==False and i.lastUpdateDate==dtstr:pass
                else:
                    try:
                        likeCountResult = countAndLikes3(API_KEY, dat.videoId)
                        with open(f"./TXT/temporarily-likeCountResult.txt", "wb") as f:
                            pickle.dump(likeCountResult, f)
                        with open(f"./TXT/temporarily-likeCountResult.txt", "rb") as p:
                            l = pickle.load(p)
                            try:    
                                hololiveSongsResult.objects.create(
                                    aggregationDate=dtstr,
                                    viewCount=l["statistics"]["viewCount"],
                                    likeCount=l["statistics"]["likeCount"],
                                    info=VideoInfo.objects.get(videoId=dat.videoId),
                                    )
                            except KeyError:#高評価ボタンのカウントが非表示になっている動画
                                hololiveSongsResult.objects.create(
                                    aggregationDate=dtstr,
                                    viewCount=0,
                                    likeCount=l["statistics"]["likeCount"],
                                    info=VideoInfo.objects.get(videoId=dat.videoId))
                        i.videoCondition2=True
                        i.lastUpdateDate=dtstr
                        i.save()
                    except IndexError:#そもそも非公開か削除されている動画
                        i.videoCondition2=False
                        i.lastUpdateDate=dtstr
                        i.save()
                    except KeyError:#高評価ボタンのカウントが非表示になっている動画
                        hololiveSongsResult.objects.create(
                            aggregationDate=dtstr,
                            viewCount=l["statistics"]["viewCount"],
                            likeCount=0,
                            info=VideoInfo.objects.get(videoId=dat.videoId))
                        i.videoCondition2=True
                        i.lastUpdateDate=dtstr
                        i.save()

def getRankingTXT2(API_KEY):
    vids = VideoInfo.objects.exclude(lastUpdateDate=dt).order_by("-pk")#flat=True
    for dat in tqdm(vids):
        if dat.videoCondition2==False and dat.lastUpdateDate==dt:
            pass
        # elif hololiveSongsResult.objects.select_related('info')\
        #         .filter(info__videoId=dat.videoId, aggregationDate=dt)\
        #         .count()==0:
        #     dat.lastUpdateDate=dt
        #     dat.save()
        else:
            try:
                vAndL = countAndLikes(API_KEY, dat.videoId)
                viewCount = vAndL["viewCount"]
                try:
                    likeCount = vAndL["likeCount"]
                except KeyError:#高評価ボタンのカウントが非表示になっている動画
                    likeCount = 0
                    
                hololiveSongsResult.objects.create(
                    aggregationDate=dtstr,
                    viewCount=viewCount,
                    likeCount=likeCount,
                    info=VideoInfo.objects.get(videoId=dat.videoId))
                dat.videoCondition2=True
                
            except IndexError:#そもそも非公開か削除されている動画
                dat.videoCondition2=False
            except ObjectDoesNotExist:#メン限
                dat.videoCondition2=False
            except KeyError:
                dat.videoCondition2=False    
            dat.lastUpdateDate=dtstr
            dat.save()

def getAutoResult2(API_KEY, dt0, autoModuleNumber):
    autos = AutoChannel.objects.all()
    for auto in tqdm(autos):
        modPk = operator.mod(auto.pk, autoModuleNumber)#チャンネルのPK値でMOD計算
        modSerial = operator.mod(dt0, autoModuleNumber)#日付のシリアル値をMOD計算
        if modPk == modSerial:
            if auto.lastUpdateDate == dt:pass
            else:
                detail = autoDetail(auto.channelId,API_KEY)
                with open(f"./TXT/temporarily-AutoChannel.txt", "wb") as f:
                    pickle.dump(detail, f)
                with open(f"./TXT/temporarily-AutoChannel.txt", "rb") as p:
                    data = pickle.load(p)
                for dat in data:
                    if ("(Instrumental)" not in dat["snippet"]["title"]) and\
                        ("（Instrumental）" not in dat["snippet"]["title"]) and\
                        ("(instrumental)" not in dat["snippet"]["title"]) and\
                        ("（instrumental）" not in dat["snippet"]["title"]):
    
                        if VideoInfo.objects.filter(videoId=dat["id"]["videoId"]).exists():pass
                        else:
                            VideoInfo.objects.create(title=dat["snippet"]["title"],
                                                    videoId=dat["id"]["videoId"],
                                                    videoAge=dat["snippet"]["publishedAt"][:10],
                                                    lastUpdateDate=dtstr,
                                                    description=dat["snippet"]["description"])
                auto.lastUpdateDate = dtstr
                auto.save()

def thumbnails(channelId, API_KEY):#チェックボックスの画像取得
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.channels().list(
        part = "snippet",
        id = channelId,
        ).execute()["items"][0]["snippet"]["thumbnails"]

    return response

def getPlaylists(channelId, API_KEY):#チェックボックスの画像取得
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.playlists().list(
        part = "snippet",
        channelId = channelId,
        maxResults = 50,
        ).execute()["items"]
    return response

def getPlaylistItems(pagetoken,playlistId, API_KEY):#チェックボックスの画像取得
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    response = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlistId,
        pageToken = pagetoken,
        maxResults = 50,
        ).execute()
    try:
        nextPagetoken =  response["nextPageToken"] 
        # print(nextPagetoken)
        getPlaylistItems(nextPagetoken, playlistId, API_KEY)
    except:
        return response

def getDjangoResult2(keyword, maxresults, API_KEY, dt0, moduleNumber):
    dt2 = dt - datetime.timedelta(days=7)
    dtstr2 = dt2.strftime("%Y-%m-%d")
    publishedAfter = dtstr2
    # mod7List = []
    cInfo = hololiveChannel2.objects.all()
    for dat in tqdm(cInfo):
        # counter = VideoInfo.objects.filter(performer__name=dat.name).count()
        modPk = operator.mod(dat.pk, moduleNumber)#チャンネルのPK値でMOD計算
        modSerial = operator.mod(dt0, moduleNumber)#日付のシリアル値をMOD計算
        if modPk == modSerial:
            if str(dat.lastUpdateDate) == dt:pass
            else:
                # print("aa")
                performer2 = hololiveChannel2.objects.get(name=dat.name)
                performers = VideoInfo.objects.filter(performer=performer2)
                try:                        
                    newRanking(API_KEY, keyword, maxresults, performers, performer2, publishedAfter)
                    img = thumbnails(dat.channelId, API_KEY)
                    dat.thumbnailDefault = img["default"]["url"]
                    dat.thumbnailMedium = img["medium"]["url"]
                    dat.thumbnailHigh = img["high"]["url"]
                    dat.lastUpdateDate = dt
                    dat.save()
                except IndexError:pass
                    
def complementer0v3():#データとして存在しない日時のものを０補完してくれる関数
    dataSelected = VideoInfo.objects\
                    .filter(lastUpdateDate=dt,videoCondition2=True)\
                    .order_by("pk")
    for dat in tqdm(dataSelected):
        vid = dat.videoId
        aggDay = dt
        vAge = VideoInfo.objects.get(videoId=vid).videoAge
        dayDifference = int((aggDay - vAge)/datetime.timedelta(days=1)) + 1
        calcDates = list(hololiveSongsResult.objects.select_related('info')\
                            .filter(info__videoId=vid)\
                            .values_list('aggregationDate', flat=True)\
                            .order_by("-aggregationDate"))
        trueDates = list(map(
            lambda n: dt - datetime.timedelta(days=n), range(0, dayDifference)))

        if set(calcDates) != set(trueDates):
            diff_list = list(set(trueDates) - set(calcDates))#集計していない日を抽出

            for diff in diff_list:
                hololiveSongsResult.objects\
                    .create(aggregationDate=diff,
                            viewCount=0,
                            likeCount=0,
                            info=VideoInfo.objects.get(videoId=vid))   
                        
def complementerAve(maxPkRslt,x):
    if x==0:videoIds = VideoInfo.objects.all().order_by("pk")#古い順に調査
    if x==1:videoIds = VideoInfo.objects.all().order_by("-pk")#新しい順に調査
    if x==2:videoIds = VideoInfo.objects.all().order_by("videoId")#ABC順に調査
    if x==3:videoIds = VideoInfo.objects.all().order_by("-videoId")#ZYX順に調査
    # videoIds = VideoInfo.objects.all()
    for v in tqdm(videoIds):
        vid = v.videoId
        # print(vid)
        dataAll = hololiveSongsResult.objects.filter(info__videoId=vid, pk__gt=maxPkRslt).order_by("aggregationDate")
        if dataAll.first() is None:continue
        
        vAge = VideoInfo.objects.get(videoId=vid).videoAge
        
        noDataDate = []
        for i in dataAll:
            dayToInt = int((i.aggregationDate-vAge)/datetime.timedelta(days=1))
            if i.viewCount != 0 or (i.viewCount == 0 and i.aggregationDate==vAge):pass
            else:noDataDate.append(dayToInt)
        starts = []
        for dat in noDataDate:
            if dat-1 not in noDataDate:start=dat-1
            starts.append(start)
        # starts = [start for dat in noDataDate if dat-1 not in noDataDate:start=dat-1]
        ends = []
        for dat in reversed(noDataDate):
            if dat+1 not in noDataDate:end=dat+1
            ends.insert(0,end)
        dfN = pd.DataFrame(noDataDate)
        dfS = pd.DataFrame(starts)
        dfE = pd.DataFrame(ends)
        df = pd.concat([dfN,dfS,dfE], axis=1)

        for dat in df.itertuples():
            x0 = vAge + datetime.timedelta(days=dat[1])
            x1 = vAge + datetime.timedelta(days=dat[2])
            x2 = vAge + datetime.timedelta(days=dat[3])
            x = (x2 - x1)/datetime.timedelta(days=1)
            
            try:
                y1 = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x1)
                y2 = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x2)
                Vaskew = (y2.viewCount - y1.viewCount)/x
                Laskew = (y2.likeCount - y1.likeCount)/x
                Vave = int(Vaskew*(dat[1]-dat[2])+y1.viewCount)
                Lave = int(Laskew*(dat[1]-dat[2])+y1.likeCount)
                # print(y1.pk, y1.info.title,y1.info.videoId,x0)
                songData = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=x0)
                print(songData.pk, y1.info.title,y1.info.videoId,x0)
                if songData.viewCount == 0:
                    songData.viewCount = Vave
                    songData.likeCount = Lave
                    songData.save()
                    
            except ObjectDoesNotExist:
                dataAll = hololiveSongsResult.objects\
                    .filter(info__videoId=vid).order_by("aggregationDate")
                for i in dataAll:
                    print(i.pk, i.info.title,i.aggregationDate,i.viewCount,i.likeCount)
                    #おかしなデータを手動で削除
            except UnboundLocalError:
                errorVideo = VideoInfo.objects.get(videoId=vid)
                print(errorVideo.title,vid)
            
                
def songTypeJudge(API_KEY,maxPkInfo):
    dataAll = VideoInfo.objects.filter(pk__gt=maxPkInfo)
    for dat in tqdm(dataAll):
        vid = dat.videoId
        datType = VideoInfo.objects.get(videoId=vid).videoType
        if datType.count() == 0:#分類未定をあぶりだし
            # print(dat.videoId,dat.title)
            try:
                songResult = videoDetail(vid,API_KEY)
                originalTitle = songResult["title"]
                if ("cover" in originalTitle)or\
                    ("Cover" in originalTitle)or\
                    ("COVER" in originalTitle)or\
                    ("カバー" in originalTitle)or\
                    ("歌ってみた" in originalTitle)or\
                    ("歌って踊ってみた" in originalTitle):
                    datType.add(videoTypeJudgement.objects.get(judge="歌ってみた"))
                    # datType.save()
                elif ("MV" in originalTitle)or\
                    ("original" in originalTitle)or\
                    ("Original" in originalTitle)or\
                    ("ORIGINAL" in originalTitle)or\
                    ("オリジナル" in originalTitle):
                    datType.add(videoTypeJudgement.objects.get(judge="オリジナルソング"))
                else:
                    if "Provided to YouTube by " in songResult["description"]:
                        datType.add(videoTypeJudgement.objects.get(judge="オリジナルソング"))
                    else:
                        datType.add(videoTypeJudgement.objects.get(judge="未分類"))
            except IndexError:
                datType.add(videoTypeJudgement.objects.get(judge="その他"))
            
def dateSubtraction(x):
    result = datetime.date.today() - datetime.timedelta(days=x)#当日データ
    return result

def viewsAndLikes(vid, dAnchor, dBefore, dBranch):
    try:
        songResultsNew = hololiveSongsResult.objects.get(
            info__videoId=vid,\
            aggregationDate=dateSubtraction(dAnchor))#本日のデータ
        # print(songResultsNew)
        if hololiveSongsResult.objects.filter(
            info__videoId=vid,\
            aggregationDate=dateSubtraction(dBranch)).exists():#〇〇日前のデータがあれば引き算実行
            
            songResultsOld = hololiveSongsResult.objects.get(
            info__videoId=vid,\
            aggregationDate=dateSubtraction(dBefore))#●●日前のデータ
            viewCount = songResultsNew.viewCount - songResultsOld.viewCount
            likeCount = songResultsNew.likeCount - songResultsOld.likeCount
        else:#11日前のデータがなければ計測時点での再生回数と高評価数を返す
            viewCount = songResultsNew.viewCount
            likeCount = songResultsNew.likeCount
    except ObjectDoesNotExist:
        viewCount = 0
        likeCount = 0
    return viewCount, likeCount

def viewsAndLikesOld(vid, baseDate, dBefore, dBranch):
    try:
        songResultsNew = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=baseDate)#本日OR前日のデータ
        # print(songResultsNew)
        judgeDate = baseDate - datetime.timedelta(days=dBranch)#〇〇日前のデータがあれば引き算実行
        if hololiveSongsResult.objects.filter(info__videoId=vid,aggregationDate=judgeDate).exists():
            cfDate = baseDate - datetime.timedelta(days=dBefore)
            songResultsOld = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=cfDate)#●●日前のデータ
            viewCount = songResultsNew.viewCount - songResultsOld.viewCount
            likeCount = songResultsNew.likeCount - songResultsOld.likeCount
            
        else:#11日前のデータがなければ計測時点での再生回数と高評価数を返す
            viewCount = songResultsNew.viewCount
            likeCount = songResultsNew.likeCount
    except ObjectDoesNotExist:
        viewCount = 0
        likeCount = 0
    return viewCount, likeCount

def getData7AndData30(maxPkRslt):
    all0s = hololiveSongsResult.objects.filter(pk__gt=maxPkRslt+1)
    view30Is0 = all0s.aggregate(Min("pk"))["pk__min"]
    if all0s.count() == 0:pass
    else:#view30Is0 == 0:#差日のデータが入力されていないため計算を行って代入する
        dataAll = VideoInfo.objects.all()
        for dat in tqdm(dataAll):
            vid = dat.videoId
            try:
                data = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=dt)
                viewCount7, likeCount7 = viewsAndLikes(vid, 0, 7, 10)
                data.viewCount7 = viewCount7
                data.likeCount7 = likeCount7
                data.save()
                viewCount30, likeCount30 = viewsAndLikes(vid, 0, 30, 33)
                data.viewCount30 = viewCount30
                data.likeCount30 = likeCount30
                data.save()
            except ObjectDoesNotExist:pass
            
def getData7AndData30Old():
    view30is0data = hololiveSongsResult.objects.filter(viewCount30=0).order_by("-aggregationDate")
    if view30is0data.count() <= 1:pass#動画公開日の日差データは除外
    else:
        for view30is0dat in tqdm(view30is0data):
            # print(view30is0dat.info.videoId, view30is0dat.aggregationDate)
            title = view30is0dat.info.title
            vid = view30is0dat.info.videoId
            baseDate = view30is0dat.aggregationDate
            try:
                data = hololiveSongsResult.objects.get(info__videoId=vid,aggregationDate=baseDate)
                viewCount7, likeCount7 = viewsAndLikesOld(vid, baseDate, 7, 10)
                viewCount30, likeCount30 = viewsAndLikesOld(vid, baseDate, 30, 33)
                data.viewCount7 = viewCount7
                data.likeCount7 = likeCount7
                data.viewCount30 = viewCount30
                data.likeCount30 = likeCount30
                data.save()
            except ObjectDoesNotExist:pass
            except KeyError:pass

def flyingStartVideo_plusDescription(API_KEY):#予約投稿等で高評価が事前に押されてしまった動画データの削除。
    dataAll = VideoInfo.objects.all()#公開日に合算させる。
    for datum in dataAll:
        if datum.description[-4:]==" ...":
                vid = datum.videoId
                try:
                    songResult = videoDetail(vid,API_KEY)
                    datum.description = songResult["description"]
                    datum.save()
                except IndexError:
                    print(datum.title,datum.videoId,"is IndexError")
        
        
        flies = hololiveSongsResult.objects.filter(info__videoId=datum.videoId,
                                                   aggregationDate__lt=datum.videoAge)
        if flies.count() != 0:
            for fly in flies:
                print(fly.pk, fly.info.title, fly.info.videoId,
                        fly.aggregationDate, datum.videoAge,
                        fly.viewCount, fly.likeCount,
                        "←を\
                        hololiveSongsResult.objects.get(pk=).delete()\
                        コマンドで削除してください")

def manualAdd(API_KEY):#手動でvideoIdを追加するために回す
    for vid in videoId_Lists:
        if VideoInfo.objects.filter(videoId=vid).count() == 0:
            songResult = videoDetail(vid,API_KEY)
            VideoInfo.objects.create(
                title = songResult["title"],
                videoId = vid,
                lastUpdateDate = dtstr,
                videoAge = songResult["publishedAt"][:10],
                description = songResult["description"])
            TypeJudge = VideoInfo.objects.get(videoId=vid)
            if ("cover" in songResult["title"])or\
                ("Cover" in songResult["title"])or\
                ("COVER" in songResult["title"])or\
                ("カバー" in songResult["title"])or\
                ("歌ってみた" in songResult["title"])or\
                ("歌って踊ってみた" in songResult["title"]):
                TypeJudge.videoType.add(videoTypeJudgement.objects.get(judge="歌ってみた"))
            elif ("MV" in songResult["title"])or\
                ("original" in songResult["title"])or\
                ("Original" in songResult["title"])or\
                ("ORIGINAL" in songResult["title"])or\
                ("オリジナル" in songResult["title"]):
                TypeJudge.videoType.add(videoTypeJudgement.objects.get(judge="オリジナルソング"))
            else:
                TypeJudge.videoType.add(videoTypeJudgement.objects.get(judge="未分類"))
            for dat in hololiveChannel2.objects.all():
                if dat.name in songResult["title"]:
                    TypeJudge.performer.add(hololiveChannel2.objects.get(name=dat.name))
    maxInfo = VideoInfo.objects.all().aggregate(Max("pk"))["pk__max"]
    maxPkRslt = hololiveSongsResult.objects.exclude(viewCount30=0).aggregate(Max("pk"))["pk__max"]             
    try:#手動入力の動画情報の再生回数、高評価数を取得
        manualMaxDat = hololiveSongsResult.objects.get(info__pk=maxInfo, aggregationDate=dt)
        print(f"{manualMaxDat.info.title} is uploaded")
    except ObjectDoesNotExist:
        # print(f"{vid} under test") 
        getRankingTXT2(API_KEY)#再生回数、高評価数
        complementer0v3()
        complementerAve(maxPkRslt,1)
        
def makeCompleteData(maxPkRslt,API_KEY):
    completeData = hololiveSongsResult.objects.get(pk=maxPkRslt)
    incompleteDataAll = VideoInfo.objects.filter(pk__gt=completeData.info.pk) 
    tentative = "!!調査中"
    for videoName in tqdm(incompleteDataAll):            
        if videoName.performer.count() == 0:
            try:
                youtubeData = videoDetail(videoName.videoId,API_KEY)
                # print(youtubeData["title"])
                if hololiveChannel2.objects.filter(channelId=youtubeData["channelId"]).count() != 0:
                    for performer in hololiveChannel2.objects.all():
                        if performer.name in youtubeData["title"]:
                            videoName.performer.add(hololiveChannel2.objects.get(name=performer.name))
                        if performer.channelId == youtubeData["channelId"]:#公式チャンネル
                            videoName.performer.add(hololiveChannel2.objects.get(channelId=performer.channelId))
                if AutoChannel.objects.filter(channelId=youtubeData["channelId"]).count() != 0:       
                    for autoPerformer in AutoChannel.objects.all():
                        if autoPerformer.channelId == youtubeData["channelId"]:#自動生成チャンネル
                            for info_name in autoPerformer.info.all():
                                videoName.performer.add(hololiveChannel2.objects.get(name=info_name))
                if videoName.videoType.count()==0:
                    if "Provided to YouTube by " in youtubeData["description"]:
                        videoName.videoType.add(videoTypeJudgement.objects.get(judge="オリジナルソング"))
            except IndexError:
                print(videoName.pk,videoName.title,videoName.videoId)
            
            for performer in hololiveChannel2.objects.all():
                if performer.name in videoName.title:
                    print(performer.name , videoName.title)
                    videoName.performer.add(hololiveChannel2.objects.get(name=performer.name))
        
        if videoName.lyricist.count() == 0:
            videoName.lyricist.add(Lyricist.objects.get(lyricist__name=tentative))
        if videoName.composer.count() == 0:
            videoName.composer.add(Composer.objects.get(composer__name=tentative))
        if videoName.arranger.count() == 0:
            videoName.arranger.add(Arranger.objects.get(arranger__name=tentative))
        if videoName.mix.count() == 0:
            videoName.mix.add(Mixer.objects.get(mixer__name=tentative))
        if videoName.inst.count() == 0:
            videoName.inst.add(Musician.objects.get(musician__name=tentative))
        if videoName.movie.count() == 0:
            videoName.movie.add(VideoEditor.objects.get(videoEditor__name=tentative))
        if videoName.illust.count() == 0:
            videoName.illust.add(Illustrator.objects.get(illustrator__name=tentative))
        if videoName.coStar.count() == 0:
            videoName.coStar.add(CoStar.objects.get(coStar__name=tentative))
        if videoName.originalSinger.count() == 0:
            videoName.originalSinger.add(OriginalSinger.objects.get(originalSinger__name=tentative))
        
        if videoName.videoType.count() == 0:
            if ("cover" in videoName.title)or\
            ("Cover" in videoName.title)or\
            ("COVER" in videoName.title)or\
            ("カバー" in videoName.title)or\
            ("歌って" in videoName.title):
                videoName.videoType.add(videoTypeJudgement.objects.get(judge="歌ってみた"))
            elif ("MV" in videoName.title)or\
            ("original" in videoName.title)or\
            ("Original" in videoName.title)or\
            ("ORIGINAL" in videoName.title)or\
            ("オリジナル" in videoName.title):
                videoName.videoType.add(videoTypeJudgement.objects.get(judge="オリジナルソング"))
           
def collectVideoInfo(API_KEY,dt0,keyword,autoModuleNumber,moduleNumber,maxresults,maxPkRslt):
    print("getAutoResult2")
    getAutoResult2(API_KEY, dt0, autoModuleNumber)
    print("getDjangoResult2")
    getDjangoResult2(keyword, maxresults, API_KEY, dt0, moduleNumber)
    print("getRankingTXT2")
    getRankingTXT2(API_KEY)#再生回数、高評価数
    print("complementer0v3")
    complementer0v3()#存在しない日付に0補完
    print("complementerAve")
    complementerAve(maxPkRslt,1)#0:古い順1:新しい順2:ABC順3:ZYX順 新しいものしか埋められていない
    print("getData7AndData30")
    getData7AndData30(maxPkRslt)
    print("getData7AndData30Old")
    getData7AndData30Old()
    print("makeCompleteData")
    makeCompleteData(maxPkRslt,API_KEY)
    print("flyingStartVideo")
    flyingStartVideo_plusDescription(API_KEY)

# if ("(Instrumental)" in dat["snippet"]["title"]) or ("instrumental）" in dat["snippet"]["title"]):
#     continue

# if VideoInfo.objects.filter(videoId=dat["id"]["videoId"]).exists():pass
# else:
#     VideoInfo.objects.create(title=dat["snippet"]["title"],
#                             videoId=dat["id"]["videoId"],
#                             videoAge=dat["snippet"]["publishedAt"][:10],
#                             lastUpdateDate=dtstr,
#                             description=dat["snippet"]["description"])


# ちなみにこれは早期リターンというテクニックです(正確にはその亜種、returnではなくcontinueを使っているため)。
# 一般にプログラムはネストが深くないほうが良いとされています。早期リターンはネストを浅くする手法の１つです。
# https://zenn.dev/media_engine/articles/early_return
# また、条件式を書くとき、notは使わないほうが理解しやすいとされています。可能な限りnotで書かない工夫をすると良いです。