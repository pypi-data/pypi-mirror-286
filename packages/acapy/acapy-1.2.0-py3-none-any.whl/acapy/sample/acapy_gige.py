import sys

import cv2      # OpenCV
import acapy    # AcaPy

# ※GigEカメラを使用する際は、ファイアウォールを無効にするか、ファイアウォールによるアプリケーションの許可を行ってください

# -------------------------------------------------------
# GigEカメラ一覧の取得
cameras = acapy.AcaPy.get_camera_list()
print(cameras)
# [('169.254.7.41', 1, 'ABA-001IR-GE', 1234568790), ('169.254.7.42', 1, 'ABA-001IR-GE', 1234568791)]

if len(cameras) < 1:
    # カメラがみつからなかったとき
    print("No Camera")
    sys.exit(0)

# -------------------------------------------------------
# AcaPyクラスのGigEカメラを指定したインスタンス
capture = acapy.AcaPy(cameras[0])       # GigEカメラを最初に見つけたカメラ
#capture = acapy.AcaPy('169.254.7.41')  # 固定IP指定のとき

# -------------------------------------------------------
# カメラ設定例
camera = capture.camera_control         # CameraControlクラスオブジェクトの取得
print(camera.get_camera_category_feature_text())    # カメラ設定値一覧の取得、表示
_, width, _ = camera.get_value('Width') # カメラの幅の画素数の取得
camera.set_value('Width', 640)          # カメラの幅の画素数の設定

# -------------------------------------------------------
# AcaPyクラス設定例（カメラの設定に合わせて取込サイズを設定する）
capture.width = 640     # 取込画像の幅を合わせる
capture.reflect_param() # 設定値の反映

# -------------------------------------------------------
# Snap（カメラ画像１枚の取得）
ret, frame = capture.snap()
# 画像表示
cv2.imshow("Image", frame)

cv2.waitKey()
