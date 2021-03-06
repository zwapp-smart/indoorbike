# indoorbike
プログラミング可能なサイクルトレーナーで楽しもう。

# パワー計算と負荷レベル計算

zwapp-smartのindoorbikeは、速度や斜度からパワーや負荷レベルの計算をプログラミングで行っています。
ソースコードは、MicroPython言語でプログラミングされており、ファイル名は、`simu.py`です(`src`フォルダ内)。

## simu.speedAndWatt - 速度とパワーの計算

速度とパワーの計算は、`speedAndWatt`関数でプログラミングされています。  
引数から結果を返します。

```simu.py
def speedAndWatt(args):
    speed100 = c.convSpeed(args[0])
    watt = c.calcPower(speed100, args[1])
    debug("SPEED AND WATT: {} => {}".format(args, (speed100, watt,)))
    return (speed100, watt,)

```

**【引数】**

| # | 引数 | 説明 | 単位 | 備考 |
|---|------|------|------|------|
| 1 | args[0] | 速度 | 0.01km/h | 100倍された値 |
| 2 | args[1] | 負荷レベル | レベル | 1～24の整数 |
| 3 | args[2] | ハートレート | bpm | 常にゼロ |
| 4 | args[3] | ケイデンス | rpm | ゼロまたは1 |
| 5 | args[4] | パワー | watt | 常にゼロ |
<br>

**【結果】**

| # | 変数 | 説明 | 単位 | 備考 |
|---|------|------|------|------|
| 1 | speed100 | 速度 | 0.01km/h | 100倍された値 |
| 2 | watt | パワー | watt |  |
<br>

## simu.simulateBike - 負荷レベルの計算

負荷レベルの計算は、`simulateBike`関数でプログラミングされています。  
引数から結果を返します。

```simu.py
def simulateBike(args):
    incline = g.calcIncline(args[1], args[4])
    return (incline,)
```

**【引数】**

| # | 引数 | 説明 | 単位 | 備考 |
|---|------|------|------|------|
| 1 | args[0] | 風速 | 0.001 m/sec | 1000倍された値 |
| 2 | args[1] | 斜度 | 0.01% | 100倍された値 |
| 3 | args[2] | Crr | 0.0001 | 10000倍された値 |
| 4 | args[3] | Cw | 0.01 kg/m | 100倍された値 |
| 5 | args[4] | 速度 | 0.01 km/h | 100倍された値 |
<br>

> **Note:**  
> **Crr** - Coefficient of Rolling Resistance  
> **Cw** - Wind Resistance Coefficient  
<br>

**【結果】**

| # | 変数 | 説明 | 単位 | 備考 |
|---|------|------|------|------|
| 1 | incline | 負荷レベル | レベル | 1～24の整数 |
<br>

# プログラムの更新

USBデータ通信ケーブルで接続したマイコンに`ampy`コマンドで`simu.py`ファイルを転送します。

## 準備

`ampy`コマンドを実行するには、`Python3`と`adafruit-ampy`のインストールが必要です。

1. [Python3をダウンロード](https://www.python.org/downloads/)し、インストールします
1. `pip install -y adafruit-ampy`コマンドで、`adafruit-ampy`をインストールします


## ソースコードの入手

ソースコードの入手方法には、3つの方法があります。いずれかの方法で入手します。

1. git clone コマンドで、gitクローンとしてダウンロードする  
   → 詳細は、インターネットで検索して調べてください。
1. ZIP形式ファイルでダウンロードする  
   → 右上の**「CODE」（緑色）**をクリックし、DOWNLOAD ZIPでダウンロードします。
1. 必要なファイルだけをダウンロードする  
   → 例えば、[/src/simu.py](/src/simu.py)を開き、コード右上の「Raw」を「名前を付けてリンク先を保存」します。


## 更新（ファイル転送）

マイコンとPCとをUSBデータ通信ケーブルで接続し、次のコマンドで`simu.py`ファイルを転送します。

```
cd src
ampy --port=/dev/ttyS8 put simu.py

```
<br>

> Note:  
> `/dev/ttyS8` の部分は、各PCの環境に合わせます  
<br>

# 汎用スマホアプリの使い方

スマホなどに次のアプリをインストールしてください。

**【Android】**  
[nRF Connect for Mobile](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=ja&gl=US)  

**【App Store】**  
[nRF Connect: Bluetooth App](https://apps.apple.com/jp/app/nrf-connect/id1054362403)

`Zwapp-SMART`に接続すると、速度やパワーを表示ししたり、負荷を制御したりできます。  
負荷の制御方法は、動画を参照してください。→ [nRF_zwapp_level.mp4](https://drive.google.com/file/d/16X56UKOughl4k4ioNAlPbwCuKAxUZBo4/view?usp=sharing)  
