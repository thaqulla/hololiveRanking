from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.filter
def minusCalc(big, small):
  return big - small

@register.simple_tag
def plusCalc2(head, foot, x):
  if x == 0:
    return head + foot
  if x == 1:
    return foot + head 
  if x == 2:
    return head + str(foot) 

def plusCalc3(val1, val2, val3):
  return val1 + val2 + val3
