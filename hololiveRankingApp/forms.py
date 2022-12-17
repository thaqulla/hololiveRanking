from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from .models import VideoInfo, Lyricist, Composer,Arranger,Mixer,Musician,VideoEditor,\
  Illustrator,CoStar,OriginalSinger,AnotherPerson


class LoginForm(AuthenticationForm):
  
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['placeholder'] = field.label
          
class VideoInfoForm(forms.ModelForm):
  lyricist = forms.ModelMultipleChoiceField(
    queryset=Lyricist.objects.all().order_by('lyricist__name'),
    label='作詞家',
    widget=forms.CheckboxSelectMultiple,)
  composer = forms.ModelMultipleChoiceField(
    queryset=Composer.objects.all().order_by('composer__name'),
    label='作曲家',
    widget=forms.CheckboxSelectMultiple,)
  arranger = forms.ModelMultipleChoiceField(
    queryset=Arranger.objects.all().order_by('arranger__name'),
    label='編曲家',
    widget=forms.CheckboxSelectMultiple,)
  mix = forms.ModelMultipleChoiceField(
    queryset=Mixer.objects.all().order_by('mixer__name'),
    label='ミックス',
    widget=forms.CheckboxSelectMultiple,)
  inst = forms.ModelMultipleChoiceField(
    queryset=Musician.objects.all().order_by('musician__name'),
    label='楽器担当',
    widget=forms.CheckboxSelectMultiple,)
  movie = forms.ModelMultipleChoiceField(
    queryset=VideoEditor.objects.all().order_by('videoEditor__name'),
    label='動画編集者',
    widget=forms.CheckboxSelectMultiple,)
  illust = forms.ModelMultipleChoiceField(
    queryset=Illustrator.objects.all().order_by('illustrator__name'),
    label='イラストレーター',
    widget=forms.CheckboxSelectMultiple,)
  coStar = forms.ModelMultipleChoiceField(
    queryset=CoStar.objects.all().order_by('coStar__name'),
    label='共演者',
    widget=forms.CheckboxSelectMultiple,)
  originalSinger = forms.ModelMultipleChoiceField(
    queryset=OriginalSinger.objects.all().order_by('originalSinger__name'),
    label='原曲歌い手',
    widget=forms.CheckboxSelectMultiple,)
  
  class Meta:
    model = VideoInfo
    fields = ["lyricist","composer","arranger","mix","inst","movie","illust","coStar","originalSinger"]
  #全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する
  
class ConcernedCreateForm(forms.ModelForm):
  
  class Meta:
    model = AnotherPerson
    fields = '__all__'