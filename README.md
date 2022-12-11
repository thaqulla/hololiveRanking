echo "テキトーに入力" >> メアド #入力  
git add . #全データステージ反映  
git commit -m YourDataOnTheStageCommited #ローカルリポジトリに反映  
git push -u origin main #パスワードも入力してリモートリポジトリに反映  

git fetch
git merge origin/main

プロジェクト名:rankingProject  
アプリ名:hololiveRankingApp  
20220522未明に登録  
  
202205551609にgit push -f origin main コマンドで強制的にプッシュ

パスワードなしでログイン

Superuser:thaqulla
Password:p.112に書いた

cd .. && source venv/bin/activate && cd rankingProject/ && python3 manage.py runserver

VScodeで黄色い波線のエラーが出た場合:https://startlab.jp/learning-python/vscode-settings/

python manage.py totalizeで自分のオリジナルpythonファイルを実行する

YOUTUBE APIは日本時間16時にリセットされる。

gitにプッシュした際は
```
git pull
python manage.py collectstatic
sudo systemctl restart httpd.service
```

SECRETの中にAPI_KEYとDBのパスワードを設定するファイルを配置する必要があります
SECRET/API_KEYs.txt
SECRET/AWS_PASSWORD2.txt


テストユーザー名：Test_user01
テストパスワード：ABCDEF1234
<!-- テストパスワード：qwerty1111 -->

検索かけたいディレクトリに移動
cd path/to/my/dir/
ディレクトリ配下のすべてのファイルで スペルミスの文字列 (Lylic) を検索
grep -r Lylic ./