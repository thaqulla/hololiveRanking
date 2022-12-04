from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from .models import VideoInfo, Lyricist


class LoginForm(AuthenticationForm):
  
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['placeholder'] = field.label
  #全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する
  
# class VideoInfoForm(forms.ModelForm):
#   lyricist = forms.ModelMultipleChoiceField(queryset=Lyricist.objects,
#                                             widget=forms.CheckboxSelectMultiple
#                                             )
#   class Meta:
#     model   = VideoInfo
#     fields  = "__all__"
    