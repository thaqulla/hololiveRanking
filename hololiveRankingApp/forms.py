from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from .models import VideoInfo, Lyricist, Composer,Arranger,Mixer,Musician,VideoEditor,\
  Illustrator,CoStar,OriginalSinger,AnotherPerson
  
from .widgets import CustomCheckboxSelectMultiple, CustomRadioSelect


class LoginForm(AuthenticationForm):
  
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['placeholder'] = field.label
          
class VideoInfoForm(forms.ModelForm):
  lyricist = forms.ModelMultipleChoiceField(
    queryset=Lyricist.objects.all().order_by('lyricist__name'),
    label='作詞家',
    widget=CustomCheckboxSelectMultiple,
    )
  composer = forms.ModelMultipleChoiceField(
    queryset=Composer.objects.all().order_by('composer__name'),
    label='作曲家',
    widget=CustomCheckboxSelectMultiple,
    )
  arranger = forms.ModelMultipleChoiceField(
    queryset=Arranger.objects.all().order_by('arranger__name'),
    label='編曲家',
    widget=CustomCheckboxSelectMultiple,
    )
  mix = forms.ModelMultipleChoiceField(
    queryset=Mixer.objects.all().order_by('mixer__name'),
    label='ミックス',
    widget=CustomCheckboxSelectMultiple,
    )
  inst = forms.ModelMultipleChoiceField(
    queryset=Musician.objects.all().order_by('musician__name'),
    label='楽器担当',
    widget=CustomCheckboxSelectMultiple,
    )
  movie = forms.ModelMultipleChoiceField(
    queryset=VideoEditor.objects.all().order_by('videoEditor__name'),
    label='動画編集者',
    widget=CustomCheckboxSelectMultiple,
    )
  illust = forms.ModelMultipleChoiceField(
    queryset=Illustrator.objects.all().order_by('illustrator__name'),
    label='イラストレーター',
    widget=CustomCheckboxSelectMultiple,
    )
  coStar = forms.ModelMultipleChoiceField(
    queryset=CoStar.objects.all().order_by('coStar__name'),
    label='共演者',
    widget=CustomCheckboxSelectMultiple,
    )
  originalSinger = forms.ModelMultipleChoiceField(
    queryset=OriginalSinger.objects.all().order_by('originalSinger__name'),
    label='原曲歌い手',
    widget=CustomCheckboxSelectMultiple,
    )
  
  class Meta:
    model = VideoInfo
    fields = ["lyricist","composer","arranger","mix","inst","movie","illust","coStar","originalSinger"]
  #全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する

anotherPerson = forms.ModelMultipleChoiceField(
  queryset=AnotherPerson.objects.all().order_by('name'),
  label='外部の方々',
  widget=CustomCheckboxSelectMultiple,
  )

class ConcernedCreateForm(forms.ModelForm):
  concerned = anotherPerson
  class Meta:
    model = AnotherPerson
    fields = '__all__'
    
class LyricistAddForm(forms.ModelForm):
  lyricist = anotherPerson
  class Meta:
    model = Lyricist
    fields = '__all__'
class ComposerAddForm(forms.ModelForm):
  composer = forms.ModelChoiceField(
    queryset=AnotherPerson.objects.exclude(
      name__in=[datum.composer.name for datum in Composer.objects.all()]).order_by('name'),
    widget=CustomRadioSelect,
    empty_label='------'
  )
  class Meta:
    model = Composer
    fields = '__all__'
class ArrangerAddForm(forms.ModelForm):
  arranger = anotherPerson
  class Meta:
    model = Arranger
    fields = '__all__'
class MixerAddForm(forms.ModelForm):
  mixer = anotherPerson
  class Meta:
    model = Mixer
    fields = '__all__'
class MusicianAddForm(forms.ModelForm):
  musician = anotherPerson
  class Meta:
    model = Musician
    fields = '__all__'
class VideoEditorAddForm(forms.ModelForm):
  videoEditor = anotherPerson
  class Meta:
    model = VideoEditor
    fields = '__all__'
class IllustratorAddForm(forms.ModelForm):
  illustrator = anotherPerson
  class Meta:
    model = Illustrator
    fields = '__all__'
class CoStarAddForm(forms.ModelForm):
  coStar = anotherPerson
  class Meta:
    model = CoStar
    fields = '__all__'
class OriginalSingerAddForm(forms.ModelForm):
  originalSinger = anotherPerson
  class Meta:
    model = OriginalSinger
    fields = '__all__'
  # def __init__( self, *args, **kwargs):
  #     super(LyricistAddForm, self).__init__(*args, **kwargs)
  #     id = kwargs.get("instance").user.id
  #     self.fields["lyricist"].queryset = AnotherPerson.objects.filter(user_id=id)
  
  #https://sleepless-se.net/2018/07/10/django%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E5%86%85%E3%81%AE%E9%96%A2%E9%80%A3%E3%83%86%E3%83%BC%E3%83%96%E3%81%AB%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC%E3%82%92%E3%81%8B%E3%81%91%E3%82%8B/