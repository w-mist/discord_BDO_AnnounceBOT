## BDO world boss/world leader announcement tool for Discord
MMORPG「黒い砂漠」のワールドボス・ワールドリーダーの出現時間をお知らせするDiscord用BOTです。

ボスの出現時間を忘れがちなあなたに。


### 更新履歴
2019/10/30 ver 1.0.1_191030 update<br>
issue #2, #3 fix

2019/10/26 ver 1.0.0_191026 release<br>
initial

### 動作例
> \[18:30] ボット: ギュント・ムラカ出現30分前<br>
> \[18:40] ボット: ギュント・ムラカ出現20分前<br>
> \[18:50] ボット: ギュント・ムラカ出現10分前<br>
> \[22:30] ボット: カランダ・クツム出現30分前<br>
> \[22:40] ボット: カランダ・クツム出現20分前<br>
> \[22:50] ボット: カランダ・クツム出現10分前<br>
> \[01:00] ボット: オピン出現30分前<br>
> \[01:10] ボット: オピン出現20分前<br>
> \[01:20] ボット: オピン出現10分前


### 機能概要
各ワールドボス・ワールドリーダーの出現30分前・20分前・10分前と各3回アナウンスします。

BDOで実装されている「～出現！」はアナウンスを見てからでは移動が間に合わないので実装していません。

ワールドボス・ワールドリーダーは、2019年10月26日現在実装のものに対応しています。


### 実装
非同期処理として10分おきにループが走り、実行マシンのMMが 10\*n(n=0,1...5) のときにアナウンス処理判定が行われます。

初回起動時にMMが00でない場合、次のMMが 10\*n(n=0,1...5) になるまで待機します。

起動後は10分おきにNTPサーバから時刻を取得し、下記条件の場合に次のMMが 10\*n(n=0,1...5) になるまで待機します。

* MMが00ではないとき
* MMが00であるが HH:MM が下記の時間かつ実行マシンとNTPサーバの時刻差が1秒以上あるとき  
00:00, 03:00, 06:00, 09:00, 12:00, 14:00, 17:00, 21:00

NTPサーバは下記3サーバを数字順で優先して利用しており、3サーバともすべて通信に失敗した場合はExceptionとして終了します。

1. ntp.nict.jp
1. ntp.jst.mfeed.ad.jp
1. time.cloudflare.com


### 動作環境
* Python 3.5.3 or later
* pip (latest)
* discord.py (latest)


#### 確認済み動作環境
* python 3.7.3 for Windows
* pip 19.2.3
* discord.py 1.2.3


### 動作環境構築
#### Pythonのインストール・DiscordでBOTを作成する云々
掲題についてはこの辺に詳しく書いてあるので割愛します。

[Pythonで実用Discord Bot(discordpy解説)](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)

[Discord Botアカウント初期設定ガイド for Developer](https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf)

#### 定数パラメータ編集
announcementToolForBDO_pub.py 内の定数である

1. s_TOKEN をBOTのアクセストークンに

1. n_CHANNEL_ID をBOT常駐先のテキストチャンネルのIDに

1. s_BOTNAME をBOTの名前に（おまけ）

にそれぞれ書き換えてください。

#### インストール
announcementToolForBDO_pub.py を任意のディレクトリに配置するだけです。

PATHが通っていればWindowsなら

`> ./announcementToolForBDO_pub.py`

で動きます。PATHが通ってない場合は適宜通したりとかしてください。


### 注意点
デフォルトではループ間隔 (f_INTERVAL) が600秒のためNTPサーバへのポーリング間隔も同じになっていますが、アクセス過多とならないようポーリング間隔は問い合わせ先のNTPサーバの利用規約に準じてください。


### 補足
個人的にログ監査を兼ねてprint文で色々吐かせてますが、気に入らない人は ifdef でも使って非表示にしてください。


### 作成者・連絡先
IGN(家名): tmp

Discord ID: la1n#6395


### ライセンス
GNU/GPLv3とします。
[GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)

