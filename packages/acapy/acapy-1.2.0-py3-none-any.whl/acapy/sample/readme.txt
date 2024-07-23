AcaPyはAcapLib2のPythonバインディングとなります。

■ 動作環境
・Windows 10/11 64bit
・AcapLib2(Ver.8.3.1以降)がインストールされていること

■ AcaPy(Python)の動作環境
・Python3.8以降
・必要モジュール:tkinter, numpy
　OpenCVのサンプルプログラムは別途、OpenCVのインストールが必要となります。

■ インストール方法
AcaPyはPyPIのサイト（https://pypi.org/project/acapy/）に公開しています。
Windowsのコマンドラインからのインストールは以下のように行います。

・pipのアップグレード
py -m pip install -U pip
・acapyのインストール
py -m pip install acapy

■ サンプルプログラムについて
・acapy_callback_sample.py
　コールバック関数を使ったSnapとGrabのサンプル
・acapy_capture_camera_setting.py
　画像入力ボードとカメラの設定を取得・設定を行うサンプル
・acapy_gige.py
　ACALDATA製GigEカメラの画像を取得し設定を取得・設定を行うサンプル
　※GigEカメラを使用する際はファイアウォールを無効にしてください
・acapy_simple_snap.py
　OpenCVのGUIを使ったSnapのみのシンプルなサンプル
・acapy_simple_grab.py
　OpenCVのGUIを使ったGrabのみのシンプルなサンプル
・acapy_tkinter_sample.py
　TkinterのGUIを使ったSnapとGrabのサンプル
・acapy_gige.py
　GigEカメラの設定を取得・設定を行い画像の撮影を行うサンプル

■ 参照
https://pypi.org/project/acapy/