from django import template
import cnum#兆億万一分厘毛忽

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.filter
def mixedKanji(origin):
  strOrigin = str(origin)
  cnumOrigin = cnum.jp(strOrigin)#兆億万一分厘毛忽
  if len(strOrigin)==5:
    return f"{strOrigin[0]}.{strOrigin[1]}万 "
  elif len(strOrigin)==9:
    return f"{strOrigin[0]}.{strOrigin[1]}億 "
  elif len(strOrigin)==13:
    return f"{strOrigin[0]}.{strOrigin[1]}兆 "
  elif "兆"  in cnumOrigin:
    NumSystem = cnumOrigin.split("兆")[0]
    return f"{NumSystem}兆 "
  elif "億"  in cnumOrigin:
    NumSystem = cnumOrigin.split("億")[0]
    return f"{NumSystem}億 "
  elif "万"  in cnumOrigin:
    NumSystem = cnumOrigin.split("万")[0]
    return f"{NumSystem}万 "
  else:
    return cnumOrigin