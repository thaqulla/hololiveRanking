from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# from asyncio import mixins

class videoTypeJudgement(models.Model):
  judge = models.CharField(
    max_length=50,null=True)
  def __str__(self):
    return self.judge
  class Meta:
    verbose_name_plural = "動画の種類"
    
class ListOfJobTitles(models.Model):
  Position = models.CharField(
    max_length=50,null=True)
  def __str__(self):
    return self.Position
  class Meta:
    verbose_name_plural = "役職"

class hololiveGenerations(models.Model):
  GenName = models.CharField(
    max_length=50,null=True)
  def __str__(self):
    return self.GenName
  class Meta:
    verbose_name_plural = "何期生"

class hololiveChannel2(models.Model):
  name = models.CharField(max_length=100,null=True)#新チャンネル名
  age = models.DateField(null=True)
  channelId = models.CharField(max_length=100, null=True)
  thumbnailDefault = models.URLField(max_length=200, null=True)
  thumbnailMedium = models.URLField(max_length=200, null=True)
  thumbnailHigh = models.URLField(max_length=200, null=True)
  description = models.TextField(null=True)
  category = models.ManyToManyField(hololiveGenerations)
  lastUpdateDate = models.DateField(default="2022-08-03")
  def getChannelUrl(self):
    baseUrl = "https://www.youtube.com/channel/"
    return baseUrl + self.channelId
  # videoURL = models.URLField(max_length=200, default=)
  def __str__(self):
    return self.name
  class Meta:
    verbose_name_plural = "ホロライブチャンネル"

class AnotherPerson(models.Model):
  name = models.CharField(max_length=100,null=True)#新チャンネル名

  category = models.ManyToManyField(ListOfJobTitles)
  snsURL = models.URLField(max_length=200, default="https://www.youtube.com/")
  snsUserName = models.CharField(max_length=100, default="@Twitter")
  
  def __str__(self):
    return self.name
  class Meta:
    verbose_name_plural = "外部の方々"

class AutoChannel(models.Model):
  name = models.CharField(max_length=100,null=True)#新チャンネル名
  info = models.ManyToManyField(hololiveChannel2, related_name='auto_channel')
  channelId = models.CharField(max_length=100, null=True)
  lastUpdateDate = models.DateField(default="2022-08-20")

  def getChannelUrl(self):
    baseUrl = "https://www.youtube.com/channel/"
    return baseUrl + self.channelId
  
  def __str__(self):
    return self.name
  class Meta:
    verbose_name_plural = "ホロライブチャンネル(自動生成)"
    
class Lyricist(models.Model):
  lyricist = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.lyricist}"
  class Meta:
    verbose_name_plural = "0:作詞家" #こっちが正しい
    
class Composer(models.Model):
  composer = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.composer}"
  class Meta:
    verbose_name_plural = "1:作曲家"
  
class Arranger(models.Model):
  arranger = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.arranger}"
  class Meta:
    verbose_name_plural = "2:編曲家"
  
class Mixer(models.Model):
  mixer = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.mixer}"
  class Meta:
    verbose_name_plural = "3:ミックス"

class Musician(models.Model):
  musician = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.musician}"
  class Meta:
    verbose_name_plural = "4:音楽"
  
class VideoEditor(models.Model):
  videoEditor = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.videoEditor}"
  class Meta:
    verbose_name_plural = "5:動画"
  
class Illustrator(models.Model):
  illustrator = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.illustrator}"
  class Meta:
    verbose_name_plural = "6:イラスト"
  
class CoStar(models.Model):
  coStar = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
    return f"{self.coStar}"
  class Meta:
    verbose_name_plural = "7:共演者"
    
class OriginalSinger(models.Model):
  originalSinger = models.ForeignKey(AnotherPerson, null=True, on_delete=models.SET_NULL)
  def __str__(self):
      return f"{self.originalSinger}"
  class Meta:
      verbose_name_plural = "8:本家歌い手"

class VideoInfo(models.Model):
  performer = models.ManyToManyField(hololiveChannel2)
  title = models.CharField(max_length=100)#動画のタイトル
  baseUrl = "https://i.ytimg.com/vi/"
  videoId = models.CharField(max_length=100, null=True)
  videoAge = models.DateField(null=True)
  videoCheck = ((False, "非公開or削除"),(True, "公開"),)
  videoCondition2 = models.BooleanField(choices=videoCheck, default=True, help_text="一日一回チェックして公開か否か確認している")

  # lyricWriter = models.ManyToManyField(LylicWriter ,help_text="スペルミス")
  lyricist = models.ManyToManyField(Lyricist ,help_text="こっちが正しい")
  composer = models.ManyToManyField(Composer)
  arranger = models.ManyToManyField(Arranger)
  mix = models.ManyToManyField(Mixer)
  inst = models.ManyToManyField(Musician)
  movie = models.ManyToManyField(VideoEditor)
  illust = models.ManyToManyField(Illustrator)
  coStar = models.ManyToManyField(CoStar)
  originalSinger = models.ManyToManyField(OriginalSinger)
  
  videoType = models.ManyToManyField(videoTypeJudgement)
  description = models.TextField(null=True)
  tags = models.TextField(null=True,default="[]")
  
  lastUpdateDate = models.DateField(null=True)

  def getVideoUrl(self):
    baseUrl = "https://www.youtube.com/watch?v="
    return baseUrl + self.videoId
  
  def getThumbnailDefault(self):
    baseUrl = "/default.jpg"
    return self.baseUrl + self.videoId + baseUrl
  def getThumbnailMedium(self):
    baseUrl = "/mqdefault.jpg"
    return self.baseUrl + self.videoId + baseUrl
  def getThumbnailHigh(self):
    baseUrl = "/hqdefault.jpg"
    return self.baseUrl + self.videoId + baseUrl
  def getThumbnailStandard(self):
    baseUrl = "/sddefault.jpg"
    return self.baseUrl + self.videoId + baseUrl
  def getThumbnailMaxres(self):
    baseUrl = "/maxresdefault.jpg"
    return self.baseUrl + self.videoId + baseUrl

  def __str__(self):
    return f"{self.title}:{self.videoId}"
  class Meta:
    verbose_name_plural = "ホロ全曲情報"

class FalseNameCorrect(models.Model):
  falseName = models.CharField(max_length=100)
  trueName = models.CharField(max_length=100)
  def __str__(self):
    return f"{self.falseName}→{self.trueName}"
  class Meta:
    verbose_name_plural = "カンマ入りタイトル修正"

class hololiveSongsResult(models.Model):
  aggregationDate = models.DateField(null=True)
  viewCount = models.IntegerField(null=True)
  likeCount = models.IntegerField(null=True)
  viewCount7 = models.IntegerField(null=True,default=0)
  likeCount7 = models.IntegerField(null=True,default=0)
  viewCount30 = models.IntegerField(null=True,default=0)
  likeCount30 = models.IntegerField(null=True,default=0)

  info = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.info}:{self.aggregationDate}"
  class Meta:
    verbose_name_plural = "ホロ日別結果"

class OldResult(models.Model):#mainPCの過去のCSVデータ
  title = models.CharField(max_length=100)#動画のタイトル
  videoId = models.CharField(max_length=100, null=True)
  viewCount = models.IntegerField(null=True)
  likeCount = models.IntegerField(null=True)

  videoAge =  models.DateField(null=True)
  aggregationDate = models.DateField(null=True)
  def __str__(self):
    return f"{self.title}:{self.aggregationDate}"
  class Meta:
    verbose_name_plural = "ホロ日別結果(Old)"