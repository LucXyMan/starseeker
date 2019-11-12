# StarSeeker

## 概要
RPG+カード+パズルゲーム。

**Japanese version only.**

## 動作環境
本プログラムはPythonで書かれています。
以下のインストールが必要です。

- python 2.7.15: https://www.python.org
- pygame 1.9.3: https://www.pygame.org

Ubuntu 18.04.1 で動作確認しています。

## ファイル構成
- starseeker
	- README.md: このテキスト。
	- LICENSE.md: ライセンス。
	- MANUAL.md: 説明書。
	- install.py: Linux用インストーラ。以下をインストールする。
		- startup.sh: 起動シェルスクリプト。
		- icon.png: ゲームのアイコン。
		- Source: ソースコード。
		- Entry.desktop: デスクトップエントリ。

## 設定ファイル
- /home/*user*/.config/starseeker
	- savedata: ゲームのセーブデータ。
	- backup: セーブデータのバックアップ。
	- keyconf.txt: キーコンフィグ用ファイル。

## ゲームの始め方
操作方法は*MANUAL.md*を参照してください。
以下の操作は全て*starseeker*ディレクトリ内部で行います。

	$ cd starseeker
	
### 簡単な起動法
ソースコードからプログラムを起動します。
端末で以下のコードを実行します。

	$ python Source

### インストール
ゲームをメニューに登録します。
端末で以下のコードを実行します。

	$ sudo python install.py

#### アンインストール
ゲームをメニューから削除します。
端末で以下のコードを実行します。

	$ sudo python install.py -u

## 更新履歴
- 2019年11月12日: ゲームを公開。

## ライセンス
**まだ用意していない**

## 作った人
Copyright(c)2019 黒尾幸男
