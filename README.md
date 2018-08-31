flask for wep portfolio
# 「【学生限定】初心者歓迎！はじめてのWebアプリ開発 ハンズオン【Python】」勉強会のためのWebポートフォリオ作成用のFlask App Builder実装

元記事： https://qiita.com/yoppe/items/651a9ce8a7c655299eda

本ハンズオンチュートリアルは [findlabの勉強会](https://findlab.connpass.com/event/98271/)用の資料です。
一応、勉強会に参加していなくて使えるように作っています。

今回のチュートリアルによって作れるWebポートフォリオの完成品が以下のようなのページになります。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/85658363-6db9-dbf5-2e7a-06eae273d787.png)



**今回のチュートリアルで話すこと**
- 開発環境の構築方法
- Webアプリの作り方
  - Flask
  - Jinja2
  - DBアクセスライブラリ
- Webサーバの基本
- Webアプリの公開方法

**今回のチュートリアルで話さないこと**
- バージョン管理ツール(Git)の使い方
- Pythonの書き方
- HTMLの書き方
- CSSの書き方
- ログイン認証周りの技術

このチュートリアルではプログラムの細かい書き方がわからなくても、コピペでWebアプリを作れるようにしています。

プログラムの書き方については、チュートリアル後このアプリをベースに技術勉強を進めていただければと思います。

---

## 事前準備

ハンズオンでは 「AWS Cloud9」というブラウザで使えるコードエディタを使用します。

事前に，AWS Cloud9とHerokuのアカウント登録を行なっておいてください。

**参考:**

- AWS Cloud9の登録方法 ⇛ [高機能のクラウドIDE，AWS Cloud9の登録方法を丁寧に解説！](https://www.yukisako.xyz/entry/aws-cloud9)
- Herokuの登録方法 ⇛ [Heroku（ヘロク）の登録方法](https://hajipro.com/heroku/heroku-install)


### AWS Cloud9について

- ブラウザさえあれば利用できる統合開発環境(IDE)
- AWS Cloud9の元となったサービスであるCloud9は2016年にAmazonに買収され、名称もAWS Cloud9に変わっている
- 現在はAWSからしか登録できなくなっている
- 旧Cloud9とAWS版のAWS Cloud9は見た目も機能もかなり違う
- 昔の記事は旧Cloud9関連のものが多く参考にならないことが多いので注意


#### AWS Cloud9のメリット・デメリット

##### メリット

- 環境構築不要で始められる
- MacやWindowsなどPCのOSに依存しない
- 開発環境の再構築が容易
- チームで１つのファイルをリアルタイムに共同編集が可能

##### デメリット

- 環境構築のノウハウが得られない
- スペックが低い
- クラウドIDE特有のクセに翻弄される
- 無料枠を超えるとお金がかかる

ちゃんとした開発を始める際は自力での環境構築をおすすめします。

参考： [クラウドIDEを使うメリットとデメリット](https://qiita.com/tsuemura/items/7540211aa73f22e3cbe1)


#### チュートリアル用のコードをDL

ターミナルで以下を実行

```bash
ec2-user:~/environment (master) $ git clone https://github.com/yoppe/flask_for_wep_portfolio.git
```

#### Cloneしてきたコードの説明
```
.
├── README.md
├── app
│   ├── indexview.py    -- トップページ用のViewModel
│   ├── models.py       -- DBに接続するためのモデル
│   ├── templates
│   │   ├── 404.html   -- Not Foundページ用のHTML
│   │   └── index.html -- トップページページ用のHTML
│   ├── translations    -- 多言語化対応用(今回は触れない)
│   └── views.py        -- トップページ以外のViewモデル
├── babel                -- 多言語化対応用(今回は触れない)
├── config.py            -- 設定ファイル
├── demo_app             -- デモ用のアプリ
│   ├── demo.py
│   └── templates
│       ├── demo.html
│       └── layout.html
├── requirements.txt     -- アプリの作成に必要ライブラリのリスト
├── run.py               -- 起動用のスクリプト
├── Procfile             -- Heroku起動時の起動コマンド指定
├── runtime.txt          -- Heroku起動時のPythonバージョン指定用
└── setup_aws_cloud9_for_py3.sh -- Cloud9環境設定用
```

#### AWS Cloud9 の簡単な使い方

- 「＋」マーク ⇛ 「new file」でファイル作れ、閉じてしまったタブも復元できる
![Aug-27-2018 17-45-10.gif](https://qiita-image-store.s3.amazonaws.com/0/7885/ee10cd9b-b82b-2caf-070d-bba5460616eb.gif)
- ImmediateタブではJavaScriptを即時実行できる
![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/7743afae-ba72-d46a-88d1-e16ec8b68a3d.png)
- Preferencesでコード保管機能の設定など、エディタ自体の設定をいじれる
- bashタブは現在起動しているEC2にログインしている状態のターミナルになっている
  - aws --version 。AWS CLI のバージョン情報を出力します。
  - pwd 現在のディレクトリへのパスを出力します。
  - ls -l 現在のディレクトリについての情報を出力します。
- プログラムは「Run」ボタン(![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/57651be5-3c3b-7986-60a9-f21bbfa2e415.png))により実行可能（ターミナル上で実行すると終了できなくなる場合がある）
- ターミナル上で終了できないプログラムは、メニューの「Tools」⇛「Process List」⇛対象プログラム選択⇛「Kill」で強制終了

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/95cfd47c-75c8-fb72-357b-adc25b326b0d.png)


#### Debuggerの使い方

- 確認したい行の左をチェックし、ブレークポイント（赤い印）を付ける
- 実行画面の右上にある![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/e6fed7df-80f9-8412-1d80-a77c2b0f98b2.png)をチェックし、デバッグモードにする
- 「Run」ボタンで通常通り実行。Debuggerウィンドウが開き、Debuggerが起動する

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/aa7644c7-57f3-c915-b939-a7376a291f49.png)


参考： [AWS Cloud9 の IDE チュートリアル](https://docs.aws.amazon.com/ja_jp/cloud9/latest/user-guide/tutorial.html)

### 開発環境セットアップ

**やること**

- Pythonのバージョンアップ
- Herokuのインストール


#### Pythonのバージョンアップ

「AWS Cloud9」⇛「Preferences」⇛「Project Settings」⇛「Python Support」のPythonのバージョンを２から３に変更

参考： [AWS Cloud9でPython3を使う方法](https://qiita.com/sho-hitomi/items/3ca8409d9f6dd0c6a658)

##### setup_aws_cloud9_for_py3.sh実行

```bash
$ python -V
Python 2.7.14
$ cd flask_for_wep_portfolio/
$ pwd
/home/ec2-user/environment/flask_for_wep_portfolio
$ ./setup_aws_cloud9_for_py3.sh
```

> **setup_aws_cloud9_for_py3内の挙動:**
・python2.7に割り当てられているエイリアスをpython3.6に変更( `$sed -i 's/python27/python36/g' ~/.bashrc` )
・システムが使うPythonをpython3.6に変更(`$sudo alternatives --set python /usr/bin/python3.6`)
> ※本記事ではPythonの環境設定に、このスクリプトを使用しているが、Pythonのバージョンアップが適切に行えればいいので自身で設定できれば使う必要はない（むしろCloud9の環境パスが変わったら使えなくなるので自力で切るようになっておいたほうがいい）


##### bashrcの再読込み

```bash
$ source ~/.bashrc
```

##### 環境確認

```bash
$ /etc/alternatives/python -V
Python 3.6.5
$ python -V
Python 3.6.5
$ pip -V
pip 9.0.3 from /usr/lib/python3.6/dist-packages (python 3.6)
```

pipとは、Pythonのパッケージ管理ツールです。（[pip - Wikipedia](https://ja.wikipedia.org/wiki/Pip)）

以上、これでPythonの開発環境は整いました。

---

## FlaskでのWebアプリ開発

### Flaskとは

- 手軽で軽量なウェブアプリケーションフレームワーク
- RubyでいうSinatra
- 最小のコード量でWebアプリを開発できる
- シンプルな分、大規模だったり複雑なアプリケーションには不向き
- [公式ドキュメント](http://flask.pocoo.org/)

### Flaskを動かすための環境整備＆実行

#### Pythonライブラリのインストール

必要なパッケージ(ライブラリ)群は、 `requirements.txt` にすべて記述されているので、 `pip` コマンドを使ってすべてインストールします。

```bash
$ sudo pip install -r requirements.txt
```

#### Hello World用のデモアプリ実行

##### demo_appのディレクトリ構成

```
├── demo_app             -- デモ用のアプリ
│   ├── demo.py
│   └── templates
│       ├── demo.html
│       └── layout.html
```

最低限の実装しかないデモ用のアプリ(demo_app/demo.py)を実行

```python
from flask import Flask # Flaskモジュールをインポート

app = Flask(__name__) # Flaskアプリのインスタンス生成

@app.route("/")            # URLのパス
def hello():               # ”/” にアクセスされたときに実行される関数
    return "Hello World! "  # テキストを返却

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) # ビルドインサーバー起動
```

##### 実行＆アプリ画面表示

1. demo.pyを開く
1. 「Run」で実行
1. 「Preview」⇛「Preview Running Application」で実行画面表示

![Aug-26-2018 19-41-58.gif](https://qiita-image-store.s3.amazonaws.com/0/7885/51ca8df3-cf37-46b2-87fb-6e0cb64a981c.gif)


##### 変更を反映させるために

1. demo.pyを編集したら、必ず保存（保存と同時に自動ビルドが実行される）
1. ![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/0be24b27-fdf5-fb63-e9f7-e29cacb308fa.png)で実行画面をリロード

##### デモアプリに画面を追加

デモアプリを実行したことで、「Hello World」を表示できました。

しかし、実際のWebアプリではプレーンなテキストではなく、ブラウザが理解できるHTMLやJavaScriptで扱いやすいJSON形式のレスポンスを返してあげる必要があります。

今回はJavaScriptは使わないので、HTMLでの出力できるようにします。

Flask には [Jinja2](http://jinja.pocoo.org/docs/dev/) というテンプレートエンジンがデフォルトで組み込まれています。

Jinja2の細かい使い方は、公式を確認してください。
[Jinja2 - 公式]([Jinja2](http://jinja.pocoo.org/docs/dev/))

###### テンプレートエンジンとは

>テンプレートと呼ばれるHTMLのひな形を元にプログラムで加工し、画面に出力するためのライブラリ。プログラマーとWebデザイナーとの分業を目的とし、特別なタグを解釈して実行することで処理を行う
引用：https://www.weblio.jp/content/%E3%83%86%E3%83%B3%E3%83%97%E3%83%AC%E3%83%BC%E3%83%88%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%B3


###### 基本的な使い方

Pythonプログラムでは、HTMLテンプレートをレンダリングするための `render_template` を使用します。

```python
from flask import render_template # render_templateをインポート

@app.route('/')
def index():
    title = "ようこそ"
    return render_template('demo.html', title=title) # 第一引数にテンプレート名、第二引数にテンプレートに渡す値
```

##### HTMLテンプレート内で使える基本的な構文

**if文**

```html
{% if title %}
  <title>{{ title }}</title>
{% else %}
  <title>No title</title>
{% endif %}
```

**for文**

```html
{% for user in users %}
  <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
```

**他のビューの埋め込み**

```html
<!-- 子テンプレート(demo.html) -->
{% extends "layout.html" %}
{% block content %}
  <h1>Hello world</h1>
{% endblock %}
```

```html
<!-- 親テンプレート(layout.html) -->
{% block content %}{% endblock %}
```

##### デモアプリにテンプレートエンジン追加

###### templatesフォルダにdemo.html追加

```html
<!-- demo.html -->
{% extends "layout.html" %}
{% block content %}
  <h1>{{ message }}</h1>
  ようこそ、デモアプリへ
{% endblock %}
```

###### demo.pyを修正

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    message = "Hello world" # ← 画面に表示するテキスト
    return render_template('demo.html', message=message) # ← HTMLをレンダリング(動的に変更されるmessageを引数に入れている)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
```

###### 実行
アプリの実行画面をリロードすると、下記のように追加したHTMLを出力できるかと思います。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/7791f2ee-ecde-25ea-e144-744b5a03d9e1.png)



### Webポートフォリオ開発

今回、作成するWebポートフォリオは自身のスキルを登録し、一覧表示できるCMSです。

>コンテンツ管理システム（英: content management system, CMS）は、
ウェブコンテンツを構成するテキストや画像などのデジタルコンテンツを統合・体系的に管理し、配信など必要な処理を行うシステムの総称。2005年頃より一般的に普及したといわれる。コンテンツマネージメントシステムとも呼ばれる。

#### Webポートフォリオの仕様

実現したい細かい仕様は以下になります。

- ユーザには訪問者と管理者がいる
- 訪問者はトップページの１ページのみを閲覧可能
- トップページでは、自己紹介とスキル一覧をかっこよく表示できる
  - スキルの登録項目は：①スキル名，②習熟度合い，③説明
- 管理者は、システムにログインし管理画面を閲覧可能
- 管理画面では、ユーザ管理、登録スキルの管理行える
- 自己紹介
- スキル情報
- コンタクト情報

##### Webポートフォリオの開発について

Git Cloneしたリポジトリ内にすでに、完成品が入っているので動かくのみです。

Flask-AppBuilderを使うので、開発時に書かないといけないコードもごく最小になっています。

###### Flask-AppBuilderとは

- データベースへの接続周りの機能
- セキュリティを対策されたログイン機能
- CRUDの自動生成機能
- フォーム生成機能
- 管理画面自動生成

などWeb開発で必要な様々な機能をFlaskに付けることができるモジュール

[Flask-AppBuilder - GitHub](https://github.com/dpgaspar/Flask-AppBuilder)


##### アプリのディレクトリ構成

```
├── app
│   ├── indexview.py    -- トップページ用のViewModel
│   ├── models.py       -- DBに接続するためのモデル
│   ├── templates
│   │   ├── 404.html   -- Not Foundページ用のHTML
│   │   └── index.html -- トップページページ用のHTML
│   ├── translations    -- 多言語化対応用(今回は触れない)
│   └── views.py        -- トップページ以外のViewモデル
```

##### DB接続の設定

Cloud9上ではSQLiteを使用し、公開するサーバー上ではPostgreSQLを使います。
使い分けの設定は、config.py内で行っています。

**config.py**

```python
if os.environ.get('DATABASE_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
```

##### 主要な実装コード

models.pyはDBにデータを格納するためのモデルを置く箇所になります。
今回、定義するモデルはスキルを保存するMySkillのみ

**models.py**

```python
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text


class MySkill(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    learning_level = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return str(self.id) + ": " + self.name
```

**views.py**

```
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, app, db
from .models import MySkill

from flask_appbuilder.forms import DynamicForm

from wtforms import SelectField, TextAreaField, TextField, validators


"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

"""
    MySkill登録用のForm
"""
class MySkillForm(DynamicForm):
    MY_CHOICES = [
        ('5', 'Level5: その道では専門家と呼ばれてます'),
        ('4', 'Level4: 人に教えることができる程度'),
        ('3', 'Level3: 普通に使える程度'),
        ('2', 'Level2: ちょっと使ったことある程度'),
        ('1', 'Level1: ちょっと知っている程度'),
    ]
    learning_level = SelectField('習得レベル', [validators.required()], choices=MY_CHOICES)
    name = TextField('スキル名', [validators.required(), validators.length(max=50)], description='例：Python, 機械学習, 英語 など')
    description = TextAreaField('説明', [validators.required(), validators.length(max=200)], description='スキルの習熟度合いを200字以内で説明してください')

"""
    MySkill登録・編集用のModelView
"""
class MySkillModelView(ModelView):
    datamodel = SQLAInterface(MySkill)
    edit_form=MySkillForm
    add_form=MySkillForm
    list_columns=['learning_level', 'name', 'description']

appbuilder.add_view(MySkillModelView,
                    'Skills',
                    icon = 'fa-envelope',
                    category = 'My Skills')

db.create_all()
```

**indexview.py**

```python
from flask_appbuilder import IndexView, expose
from .models import MySkill
from . import db


class IndexView(IndexView):

    @expose('/')
    def index(self):
        mySkills=db.session.query(MySkill).all()

        self.update_redirect()
        return self.render_template(
            'index.html',
            appbuilder=self.appbuilder,
            skills=mySkills)
```


#### 実行

**run.py**

```python
from app import app, db

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

```

demo.pyでは、ファイルを直接実行したが、今回は run.py という実行用のスクリプトを使用する

1. run.pyを開く
1. ![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/31527aed-b81e-446f-979d-80c761016859.png)で実行


初回実行時はDBが作成されるので、少し時間がかかる

※このとき、前のデモアプリがまだ実行中だった場合、下記のようなエラーが発生する

```
Traceback (most recent call last):
  File "/home/ec2-user/environment/flask_for_wep_portfolio/run.py", line 4, in <module>
    app.run(host='0.0.0.0', port=8080, debug=True)
  File "/usr/local/lib/python3.6/site-packages/flask/app.py", line 841, in run
    run_simple(host, port, self, **options)
  File "/usr/local/lib/python3.6/site-packages/werkzeug/serving.py", line 795, in run_simple
    s.bind(get_sockaddr(hostname, port, address_family))
OSError: [Errno 98] Address already in use
```

**画面**

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/cff00b79-254a-a386-4452-48e0682151c1.png)



#### 管理ユーザーの作成

ターミナルで管理ユーザーの作成

```
$ fabmanager create-admin
Username [admin]:  
User first name [admin]:
User last name [user]:
Email [admin@fab.org]:
Password:
Repeat for confirmation:
```

作成した管理ユーザーのUsernameとPasswordで管理画面にログインできます。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/be927802-dd67-fe1b-b6d6-18befc91af9c.png)


スキル追加一覧画面で、スキルを登録できるようになりました。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/3f277815-d75f-756d-1a42-7c43986ca5f4.png)

スキルを登録したり、index.htmlをいじってみよう。

参考：
- [Flask-AppBuilder](https://flask-appbuilder.readthedocs.io/en/latest/index.html)
- [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [WTForms](https://wtforms.readthedocs.io/en/stable/)


---

## Webアプリの公開

### Webサーバーについて

Webサーバーの解説については長くなるので下記リンクを参照ください。
[【初心者向け解説】Webサーバーとは？ & Webコンテナとは？](https://eng-entrance.com/java-servlet-server)

**PythonでWebアプリを動かすのに必要なサーバー**

- Webサーバー(nginx)
　⇛ ユーザ（クライアント）からのリクエストを受け取り、静的なコンテンツを返す
- WSGIサーバー(gunicorn)
　⇛ Webサーバー飛ばされてきた（リバースプロキシ）リクエストを元にPythonアプリを実行。動的なコンテンツを生成して返す

**リクエストの流れ**

1. Webサーバー(nginx)がリクエスト受け取り
1. 動的に表示する必要があるページに関してはWSGIサーバー(gunicorn)に飛ばす
1. Pythonアプリ(Flask)を実行。HTMLやJSONといったコンテンツを生成＆返却する

![Webサーバーの構成](https://codingnetworker.com/post/2016/01/24-deploy-the-network-configuration-generator-using-ansible-and-vagrant/server_side_python-web.png#floatright "Webサーバーの構成")
引用：[Deploy the Network Configuration Generator on a Server](https://codingnetworker.com/2016/01/deploy-the-network-configuration-generator-using-ansible-and-vagrant/)



#### 備考

##### gunicorn以外のWSGIサーバーについて

ApacheやnginxといったWebサーバーには、外部モジュールを組み込む機能がついており、mod_wsgiやuwsgiというモジュールを組み込めば、gunicornをインストールしなくてもPythonを実行可能です。

しかし、mod_wsgiやuwsgiは導入の際にハマることが多いため素直にgunicornを使うことをお勧めします。


##### 開発環境以外でビルドインサーバを使わない方がいい理由

Flaskにはデフォルトのサーバーが組み込まれている(ビルドインサーバ)。開発時はこちらを使いますが開発時以外では使うべきではありません。理由としては以下になります。
- シングルスレッドなので、CSSやJavaScript，画像と言った多くのレスポンスを返す必要のあるWebサーバの用途には向いていない
- 開発環境で使われることを主として作られているので、セキュリティ的に脆弱
- 長期実行に耐えれるように設計されていないため、予期せぬ原因で停止する可能性がある

参考：[What are the limitations of the flask built-in web server](https://stackoverflow.com/questions/20843486/what-are-the-limitations-of-the-flask-built-in-web-server)



### Herokuについて

Herokuの解説については長くなるので下記リンクを参照ください。
[PaaSの基礎知識とHerokuで開発を始める準備](https://codezine.jp/article/detail/8051)

- Webサーバーを始めとするアプリケーションインフラのことをあまり意識しなくていいので、その分アプリ開発に集中できる
- １dyno(インスタンス)であれば、無料
- 無料版では、30分アクセスがないor一日18時間以上動くとスリープモードに入る
- 18時間以内ならアクセスが来ると毎回立ち上がるが、スリープ後だと立ち上げ処理入るので若干重い
引用：[heroku で python 動かすチュートリアルをやったメモ](https://qiita.com/cfiken/items/0715bb945389bc9ca682)

#### Heroku CLIのインストール

公式には載っていないがコマンドでAWS Cloud9にインストール可能

```bash
$ source <(curl -sL https://cdn.learnenough.com/heroku_install)
$ heroku version
heroku/7.9.3 linux-x64 node-v10.9.0
```

参考：[https://railstutorial.jp/chapters/beginning?version=5.1#sec-heroku_setup](https://railstutorial.jp/chapters/beginning?version=5.1#sec-heroku_setup)


#### Herokuにログイン&デプロイ先登録

```bash
$ heroku login
heroku: Enter your login credentials
Email: [heroku登録時のメールアドレス]
Password: [heroku登録時のパスワード]

$ heroku apps
You have no apps. # まだ何もない

$ heroku create # Heroku上にアプリを作成
Creating app... done, ⬢ desolate-citadel-77691 # ユニークなアプリ名が設定される

$ heroku apps
=== [heroku登録時のメールアドレス] Apps
desolate-citadel-77691

$ heroku git:remote --app desolate-citadel-77691 # gitにプッシュ(デプロイ)先のHerokuアプリを登録(アプリ名は異なるので注意)
set git remote heroku to https://git.heroku.com/desolate-citadel-77691.git
```

### heroku上にDBを用意
https://postgres.heroku.com/databases にアクセスし、Postgresを選択。
![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/a432722c-0c0f-483c-9d6f-69945586014b.png)
「Install Heroku Postgres」を選択。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/7885/da2f7e89-a45c-723f-7baf-393fca97bb95.png)
上記のように設定し、「Provision add-on」で追加

## ターミナル上からもちゃんとインストールされていることを確認

```bash
$ heroku pg
=== DATABASE_URL
Plan:                  Hobby-dev
Status:                Available
Connections:           0/20
PG Version:            10.4
Created:               2018-08-30 05:31 UTC
Data Size:             7.7 MB
Tables:                0
Rows:                  0/10000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-triangular-55171
```


#### 開発したWebアプリをHerokuへデプロイ

```bash
$ pip freeze > requirements.txt # ライブラリに変更があれば、requirements.txtを更新

$ git add .

$ git commit -m"init commit"
[master (root-commit) dd857bf] init commit

$ git push heroku master # コードをHerokuにプッシュ(デプロイ)

# FlaskAppBuilderにはDBの自動構築機能がないため、手動で作る必要がある
# 以下は、初回のみ実行が必要
$ heroku run bash # Herokuサーバ内にログイン

~ $ fabmanager create-db # モデルを元にDBの構築

~ $ fabmanager create-admin # 管理者ユーザの登録

~ $ exit # Herokuサーバからログアウト

$ heroku ps:scale web=1 # herokuのインスタンス１個で起動
Scaling dynos... done, now running web at 1:Free
```

下記URLにアクセスすることで、デプロイしたアプリを確認できる。

**https://[Herokuのアプリケーション名].herokuapp.com/**

#### アプリケーションログの確認

下記コマンドにて、リアルタイムにサーバーのログを確認できる。終了はctrl+C。

```bash
ec2-user:~/environment (master) $ heroku logs --tail
```

参考：
- [Heroku コマンド・設定 メモメモ](https://qiita.com/pugiemonn/items/0e69b7a29a384b356e65)

## 最後に

### 環境のクリーンアップ

AWS Cloud9は使わなければ勝手にインスタンス落としてくれるが、使用しているストレージに関しては課金される。（１年間は無料枠がある）

課金も微々たるものですが、気になる方は下記手順にて環境を削除しよう。

1. IDE のメニューバーの[AWS Cloud9]⇛[Go To Your Dashboard (ダッシュボードを開く)] で、ダッシュボードを開く
1. 「Delete」にて、環境を削除

参考：[AWS 無料利用枠](https://aws.amazon.com/jp/free/?awsf.Free%20Tier%20Types=categories%2312monthsfree)


## 参考：

- [Re:ゼロからFlaskで始めるHeroku生活 〜環境構築とこんにちは世界〜](https://qiita.com/ymgn_ll/items/96cac1dcf388bc7a8e4e)
- [ウェブアプリケーションフレームワーク Flask を使ってみる](https://qiita.com/ynakayama/items/2cc0b1d3cf1a2da612e4)
