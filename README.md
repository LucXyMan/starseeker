# Star Seeker

![main](https://raw.githubusercontent.com/LucXyMan/storage/master/starseeker/main.png)

Version1.1.0

## 概要
RPG+カード+パズルゲーム。

## 動作環境
本プログラムはPythonで書かれています。
以下のインストールが必要です。

- python 2.7.15: https://www.python.org
- pygame 1.9.3: https://www.pygame.org

Windows 7, Ubuntu 18.04.1 で動作確認しています。

## ファイル構成
- starseeker
	- LICENSE: ライセンス。
	- MANUAL.md: 説明書。
	- README.md: このテキスト。
	- Source: ソースコード。
	- install.py: Linux用インストーラ。
	- linux: Linux用インストールファイルディレクトリ。
		- startup.sh: 起動シェルスクリプト。
		- icon.png: ゲームのアイコン。
		- Entry.desktop: デスクトップエントリ。
	- install.exe: windows用インストーラ。

## 設定ファイル
ゲーム起動時に生成されます。

- savedata: ゲームのセーブデータ。
- backup: セーブデータのバックアップ。
- keyconf.txt: キーコンフィグ用ファイル。

### ファイルの場所

#### Windows
C:\Users\userdir\AppData\Local\Star Seeker

#### Linix
/home/userdir/.config/starseeker

## ゲームの始め方
操作方法は[*MANUAL.md*](/MANUAL.md)を参照してください。

### 簡単な起動法
ソースコードからプログラムを起動します。
*starseeker*ディレクトリに入り、端末かコマンドプロンプトで、
以下のコードを実行します。

	$ python Source
	
### Windows

#### インストール
*install.exe*をダブルクリックで起動した後、
ウィザードに従って操作してください。

#### アンインストール
コントロールパネルの「プログラムのアンインストール」から削除してください。

### Linux
以下の操作は全て*starseeker*ディレクトリで行います。

	$ cd starseeker
	
#### インストール
ゲームをメニューに登録します。
端末で以下のコードを実行します。

	$ sudo python install.py

#### アンインストール
ゲームをメニューから削除します。
端末で以下のコードを実行します。

	$ sudo python install.py -u

## 更新履歴
- 2019年11月12日: 1.0.0 ゲームを公開。
- 2019年11月26日: 1.0.2 Windowsに対応。
- 2019年12月26日: 1.0.3 サポートカード実装。

## ライセンス
[BSD 3-Clause License](/LICENSE)

## 作った人
Copyright (c) 2019 [黒尾幸男](https://github.com/LucXyMan)
