'''GraphicsBox'''

from typing import Union, Tuple  # , List

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np  # アフィン変換行列演算用
# import os


__version__ = "1.2.0"

'''
////////////////////////////////////////////////////////////
//  Ver.1.1.0  (2023.08.18)     Python 3.8以降対応
////////////////////////////////////////////////////////////
●Warning部分の修正

////////////////////////////////////////////////////////////
//  Ver.1.0.0  (2021.06.8)     Python 3.8以降対応
////////////////////////////////////////////////////////////
●正式版初版

////////////////////////////////////////////////////////////
//  Ver.0.0.12  (2021.04.12) 
////////////////////////////////////////////////////////////
●プレビュー版
'''


class GraphicsBox(tk.Canvas):

    """GraphicsBox class （Image display widget）
    Option settings are the same as for the Canvas class
    """

    # def __init__(self, master, cnf={}, **kw):
    def __init__(self, master, **kw):
        super(GraphicsBox, self).__init__(master=master, **kw)
        self.master = master

        self.image = None
        self.disp_image = None

        # マウスイベント
        # MouseDown
        self.bind("<Button-1>", self._mouse_down_left)
        # MouseMove（左ボタンを押しながら移動）
        self.bind("<B1-Motion>", self._mouse_move_left)
        # MouseUp
        self.bind("<ButtonRelease-1>", self._mouse_up_left)
        # MouseDoubleClick
        self.bind("<Double-Button-1>", self._mouse_double_click_left)
        # MouseDoubleClick
        self.bind("<Double-Button-3>", self._mouse_double_click_right)
        # MouseWheel
        self.bind("<MouseWheel>", self._mouse_wheel)
        # MouseWheel(Linuxのとき)
        self.bind("<Button-4>", self._mouse_wheel_up)
        # MouseWheel(Linuxのとき)
        self.bind("<Button-5>", self._mouse_wheel_down)

        # 矢印キーでの移動
        self.displacement = 5  # キー入力１回あたりの移動量
        self.bind('<KeyPress>', self._key_press)
        # キャンバスのリサイズ
        self.bind("<Configure>", self._canvas_resize)

        # 初期アフィン変換行列
        self.reset_transform()

        # プロパティ値
        # self.__resample = Image.NEAREST     # 画像補間モード
        self.__resample = Image.Resampling.NEAREST     # 画像補間モード

        self.__grid_enabled = True          # グリッド線　表示／非表示
        self.__grid_disp_scale = 10.0       # グリッド線を表示するスケール
        self.__grid_color = "#006464"       # グリッド線色

        self.__min_scale = 0.01
        self.__max_scale = 200

        self.__bright_enabled = True        # 輝度値　表示／非表示

        self.__profile_enabled = False      # プロファイル　表示／非表示
        self.__profile_height = 120          # プロファイルのグラフの表示高さ
        self.__profile_x_color = "#64DC64"  # プロファイル線の色(X方向)
        self.__profile_y_color = "#64DC64"  # プロファイル線の色(Y方向)
        self.__cross_beam_color = "cyan"    # プロファイルの十字線の色
        self.__profile_x = 0                # プロファイル表示のX座標（ウィジェット座標）
        self.__profile_y = 0                # プロファイル表示のX座標（ウィジェット座標）

        self.__zoomup_direction = -1        # 画像拡大時のホイール回転方向（-1:下へ回転, 1:上へ回転）

        self.__old_event = None

    @property
    def grid_enabled(self):
        '''Shows/hides the grid lines.

        Parameters
        ----------
        value : bool
            True: Show
            False:Hide
        '''
        return self.__grid_enabled

    @grid_enabled.setter
    def grid_enabled(self, value):

        self.__grid_enabled = value

    @property
    def grid_disp_scale(self):
        ''' Minimum scale to display grid lines '''
        return self.__grid_disp_scale

    @grid_disp_scale.setter
    def grid_disp_scale(self, value):
        self.__grid_disp_scale = value

    @property
    def min_scale(self):
        ''' Minimum scale to display '''
        return self.__min_scale

    @min_scale.setter
    def min_scale(self, value):
        self.__min_scale = value

    @property
    def max_scale(self):
        ''' Maximum scale to display '''
        return self.__max_scale

    @max_scale.setter
    def max_scale(self, value):
        self.__max_scale = value

    @property
    def grid_color(self):
        ''' Gets/Sets the color of the grid lines. '''
        return self.__grid_color

    @grid_color.setter
    def grid_color(self, value):
        if self._check_color_name(value) is False:
            return
        self.__grid_color = value

    @property
    def profile_enabled(self):
        '''Shows/hides profiles.

        Parameters
        ----------
        value : bool
            True: Show
            False:Hide
        '''
        return self.__profile_enabled

    @profile_enabled.setter
    def profile_enabled(self, value):

        self.__profile_enabled = value

    @property
    def profile_x_color(self):    # プロファイル線の色(X方向)
        ''' Get/Set the color of the profile line (X direction). '''
        return self.__profile_x_color

    @profile_x_color.setter
    def profile_x_color(self, value):
        if self._check_color_name(value) is False:
            return
        self.__profile_x_color = value

    @property
    def profile_y_color(self):    # プロファイル線の色(Y方向)
        ''' Get/Set the color of the profile line (Y direction). '''
        return self.__profile_y_color

    @profile_y_color.setter
    def profile_y_color(self, value):
        if self._check_color_name(value) is False:
            return
        self.__profile_y_color = value

    @property
    def profile_x(self):
        ''' Get/Set the display coordinate of the profile (X coordinate of the widget).'''
        return self.__profile_x

    @profile_x.setter
    def profile_x(self, value):
        self.__profile_x = value

    @property
    def profile_y(self):
        ''' Get/Set the display coordinate of the profile (Y coordinate of the widget).'''
        return self.__profile_y

    @profile_y.setter
    def profile_y(self, value):
        self.__profile_y = value

    @property
    def profile_height(self):    # プロファイルグラフの高さ
        ''' Get/Set the Profile Graph Height'''
        return self.__profile_height

    @profile_height.setter
    def profile_height(self, value):
        self.__profile_height = value

    @property
    def bright_enabled(self):    # 輝度値　表示／非表示
        ''' Get/Set the height of the profile graph. '''
        return self.__bright_enabled

    @bright_enabled.setter
    def bright_enabled(self, value):
        self.__bright_enabled = value

    @property
    def cross_beam_color(self):    # プロファイルの十字線の色
        ''' Get/Set the color of the crosshairs in the profile. '''
        return self.__cross_beam_color

    @cross_beam_color.setter
    def cross_beam_color(self, value):
        if self._check_color_name(value) is False:
            return
        self.__cross_beam_color = value

    @property
    def affine_matrix(self):    # アフィン変換行列の取得
        ''' Get/Set affine transformation matrix. '''
        return self.__mat_affine

    @affine_matrix.setter
    def affine_matrix(self, value):
        self.__mat_affine = value

    @property
    def disp_scale(self):
        '''Get display magnification'''
        return self.__mat_affine[0, 0]

    @property
    def zoomup_direction(self):
        '''Get/Set the wheel rotation direction when enlarging an image.
        -1:Rotate downward
         1:Rotate upward
        '''
        return self.__zoomup_direction

    @zoomup_direction.setter
    def zoomup_direction(self, value):

        self.__zoomup_direction = value

    def open_image_file(
        self, filename: str,
        file_filter=None,
        disp_image: bool = True,
        zoom_fit: bool = True
    ):
        '''Open an image file

        Opens an image file (bmp, png, jpg) and returns the file name as PIL.Image.Image

        Parameters
        ----------
        filename : str
            Set the image file name.
        file_filter : str[]
            Set the list of image file formats to be displayed in the dialog.
        disp_image : bool
            Set the value to True to display the image, or False to not display the image.
        zoom_fit : bool
            Set to True to display the image in the entire widget, or False to not.

        Returns
        -------
        PIL.Image.Image
            PIL.Image.Image object
        filename
            Name of the opened image file

        '''
        if file_filter is None:
            file_filter = [("Bitmap", "*.bmp"),
                           ("PNG", "*.png"), ("JPEG", "*.jpg")]

        if filename is None:
            filename = filedialog.askopenfilename(
                filetypes=file_filter
            )
            if filename:
                im_ = Image.open(filename)
            else:
                return None, None
        else:
            im_ = Image.open(filename)

        # 画像の表示
        if disp_image is True:
            # 画像全体を表示する
            if zoom_fit is True:
                self.zoom_fit(im_.width, im_.height)

            # 画像の表示
            self.draw_image(im_)
        return im_, filename

    def _mouse_down_left(self, event):
        self.__old_event = event
        self.__profile_x = event.x
        self.__profile_y = event.y
        self.redraw_image()
        self.focus_force()

    def _mouse_move_left(self, event):
        if self.disp_image is None:
            return
        self.__profile_x = event.x
        self.__profile_y = event.y
        if self.__old_event is not None:
            self.translate(event.x - self.__old_event.x,
                           event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event

    def _mouse_up_left(self, event):
        # print("mouse_up_left", event.x, event.y)
        pass

    def _mouse_double_click_left(self, event=None):
        if self.disp_image is None:
            return
        if event is None:
            return
        self.zoom_fit(self.disp_image.width,
                      self.disp_image.height)  # type: ignore
        self.redraw_image()

    def _mouse_double_click_right(self, event=None):
        if self.disp_image is None:
            return
        if event is None:
            return
        self.scale_at(1.0/self.disp_scale, event.x, event.y)
        self.redraw_image()

    def _mouse_wheel(self, event):
        if self.disp_image is None:
            return

        scale = 1

        if self.__zoomup_direction < 0:
            if event.delta < 0:
                scale = 1.25
            else:
                scale = 0.8
        else:
            if event.delta < 0:
                scale = 0.8
            else:
                scale = 1.25

        self.scale_at(scale, event.x, event.y)
        self.redraw_image()

    def _mouse_wheel_up(self, event):
        if self.__zoomup_direction < 0:
            self.scale_at(0.8, event.x, event.y)
        else:
            self.scale_at(1.25, event.x, event.y)

        self.redraw_image()

    def _mouse_wheel_down(self, event):
        if self.__zoomup_direction < 0:
            self.scale_at(1.25, event.x, event.y)
        else:
            self.scale_at(0.8, event.x, event.y)

        self.redraw_image()

    # 矢印キーでの移動量
    def _key_press(self, event):
        if self.disp_image is None:
            return

        t_x, t_y = 0, 0

        if event.keysym == "Left":
            t_x = -self.displacement
        elif event.keysym == "Right":
            t_x = self.displacement
        elif event.keysym == "Up":
            t_y = -self.displacement
        elif event.keysym == "Down":
            t_y = self.displacement

        self.translate(t_x, t_y)
        self.redraw_image()

    def _canvas_resize(self, event):
        """ リサイズイベント """
        # print ("canvas_resize", event.width, event.height)
        if event is None:
            return
        self.redraw_image()

    def draw_image(self, image: Union[Image.Image, np.ndarray, None]):
        '''Display the image data.

        Parameters
        ----------
        image : PIL.Image.Image or np.ndarray
            Specify the image data.

        Returns
        -------
        create_image object

        '''

        if image is None:
            return None

        if "PIL" in str(type(image)):  # PIL.BmpImagePlugin.BmpImageFile, PIL.Image.Imageなど
            # PILイメージの場合
            self.disp_image = image
        # elif (type(image) is np.ndarray) == True:
        # elif type(image) is np.ndarray:
        elif isinstance(image, np.ndarray):
            # Numpy ndarrayの場合、PILに変換
            self.disp_image = Image.fromarray(image)
        else:
            return None

        # self.disp_image = pil_image

        # ウィジェットのサイズ
        wig_width = self.winfo_width()
        wig_height = self.winfo_height()

        # self.update_idletasks()

        # アフィン変換後の画像の左上座標
        left_top = np.dot(self.__mat_affine, (0., 0., 1.))
        # アフィン変換後の画像の右下座標
        right_down = np.dot(self.__mat_affine, (float(self.disp_image.width), float(
            self.disp_image.height), 1.))  # type: ignore

        # アフィン変換後の画像の左上のウィジェット座標
        x_0 = left_top[0]
        y_0 = left_top[1]
        # アフィン変換後の画像の右下のウィジェット座標
        x_1 = right_down[0]
        y_1 = right_down[1]

        # アフィン変換の移動量
        t_x = 0.0
        t_y = 0.0

        if x_0 < 0:
            t_x = x_0
            x_0 = 0
        if y_0 < 0:
            t_y = y_0
            y_0 = 0

        x_1 = min(x_1, wig_width)
        y_1 = min(y_1, wig_height)

        # 出力サイズ
        dst_width = x_1 - x_0
        dst_height = y_1 - y_0

        if (dst_width <= 0) or (dst_height <= 0):
            # 画像全体がキャンバスからはみ出している場合
            self.image = None
            return

        mat = self.__mat_affine.copy()
        mat[0, 2] = t_x
        mat[1, 2] = t_y
        mat_inv = np.linalg.inv(mat)

        # numpy arrayをアフィン変換用のタプルに変換
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
        )

        # PILの画像データをアフィン変換する
        dst = self.disp_image.transform(  # type: ignore
            (int(dst_width), int(dst_height)),  # 出力サイズ
            Image.Transform.AFFINE,   # アフィン変換 Image.AFFINE,   # アフィン変換
            affine_inv,    # アフィン変換行列（出力→入力への変換行列）
            self.__resample   # 補間方法、ニアレストネイバー
        )

        # 輝度値の描画(Canvasではなく、pillow imageに描画する)
        self._draw_bright(x_0, y_0, x_1, y_1, dst)

        self.image = ImageTk.PhotoImage(image=dst)

        # 画像の描画
        self.delete("all")  # キャンバスのクリア
        item = self.create_image(
            x_0, y_0,                 # 画像表示位置(左上のキャンバスの座標)
            anchor='nw',          # アンカー、左上が原点
            image=self.image      # 表示画像データ
        )

        # Grid線の描画
        self._draw_grid(x_0, y_0, x_1, y_1)

        # プロファイルの描画
        self._draw_profile(x_0, y_0, x_1, y_1)

        return item

    def redraw_image(self):
        ''' Redrawing an image '''
        self.draw_image(self.disp_image)

    def translate(self, offset_x: float, offset_y: float):
        ''' Translation '''
        mat = np.eye(3)  # 3x3の単位行列
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)

        self.__mat_affine = np.dot(mat, self.__mat_affine)

    def scale_transform(self, scale: float):
        ''' scaling '''

        # 変更後のスケール
        dst_scale = self.disp_scale * scale

        if scale > 1 and dst_scale > self.__max_scale:
            return
        if scale < 1 and dst_scale < self.__min_scale:
            return

        mat = np.eye(3)  # 単位行列
        mat[0, 0] *= scale
        mat[1, 1] *= scale

        self.__mat_affine = np.dot(mat, self.__mat_affine)

    def scale_at(self, scale: float, c_x: float, c_y: float):
        ''' Scaling around the coordinates (cx, cy) '''

        # 原点へ移動
        self.translate(-c_x, -c_y)
        # 拡大縮小
        self.scale_transform(scale)
        # 元に戻す
        self.translate(c_x, c_y)

    def zoom_fit(self, image_width: int, image_height: int):
        '''Display the image in the entire widget'''

        # ウィジェットのサイズ
        wig_width = self.winfo_width()
        wig_height = self.winfo_height()

        if (image_width * image_height <= 0) or (wig_width * wig_height <= 0):
            return

        # アフィン変換の初期化
        self.reset_transform()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0

        if (wig_width * image_height) > (image_width * wig_height):
            # ウィジェットが横長（画像を縦に合わせる）
            scale = wig_height / image_height
            # あまり部分の半分を中央に寄せる
            offsetx = (wig_width - image_width * scale) / 2
        else:
            # ウィジェットが縦長（画像を横に合わせる）
            scale = wig_width / image_width
            # あまり部分の半分を中央に寄せる
            offsety = (wig_height - image_height * scale) / 2

        # 拡大縮小
        self.scale_transform(scale)
        # あまり部分を中央に寄せる
        self.translate(offsetx, offsety)

    def reset_transform(self):
        '''
        Reset affine transformation to initialization (scale 1, no movement)
        '''
        self.__mat_affine = np.eye(3)  # 3x3の単位行列

    def src_to_dest_xy(self, x_y: Tuple[float, float]) -> Tuple[float, float]:
        '''Converts the XY coordinates on the image to the XY coordinates on the widget.

        Parameters
        ----------
        x_y
            Specifies the coordinates on the image, given as (x, y).

        Returns
        -------
        dest_xy
            Specifies the coordinates on the widget, given as (x, y).

        '''

        dst_xy = np.dot(self.__mat_affine, (x_y[0], x_y[1], 1.))
        return (dst_xy[0], dst_xy[1])

    def dest_to_src_xy(self, x_y: Tuple[float, float]) -> Tuple[float, float]:
        '''Converts the XY coordinates on the widget to the XY coordinates on the image.

        Parameters
        ----------
        x_y
            Specifies the coordinates on the widget, given as (x, y).

        Returns
        -------
        src_xy
            Specifies the coordinates on the image, given as (x, y).

        '''

        inv = np.linalg.inv(self.__mat_affine)
        dst_xy = np.dot(inv, (x_y[0], x_y[1], 1.))
        return (dst_xy[0], dst_xy[1])

    def _disp_image_rect(self, left, top, right, bottom):
        '''
        表示する画像座標の領域
        '''

        if self.disp_image is None:
            return 0, 0, 0, 0

        mat = self.__mat_affine.copy()
        mat_inv = np.linalg.inv(mat)

        # アフィン変換前の画像の左上座標
        image_left_top = np.dot(mat_inv, (left, top, 1.))
        # アフィン変換前の画像の右下座標
        image_right_down = np.dot(mat_inv, (right, bottom, 1.))

        x_0 = int(np.floor(image_left_top[0]))
        x_1 = int(np.ceil(image_right_down[0]))
        y_0 = int(np.floor(image_left_top[1]))
        y_1 = int(np.ceil(image_right_down[1]))

        if x_1 > self.disp_image.width:  # type: ignore
            x_1 = self.disp_image.width  # type: ignore

        if y_1 > self.disp_image.height:  # type: ignore
            y_1 = self.disp_image.height  # type: ignore

        return x_0, y_0, x_1, y_1

    def _draw_grid(self, left, top, right, bottom):
        '''
        グリッド線の描画
        '''
        if self.__grid_enabled is False:
            return
        if self.disp_scale < self.grid_disp_scale:
            return

        # 画像表示領域
        x_0, y_0, x_1, y_1 = self._disp_image_rect(left, top, right, bottom)

        for x in range(x_0, x_1):
            widget_point0 = np.dot(self.__mat_affine, (x, y_0, 1.0))
            widget_point1 = np.dot(self.__mat_affine, (x, y_1, 1.0))

            self.create_line(widget_point0[0], widget_point0[1],
                             widget_point1[0], widget_point1[1], fill=self.__grid_color)

        for y in range(y_0, y_1):
            widget_point0 = np.dot(self.__mat_affine, (x_0, y, 1.0))
            widget_point1 = np.dot(self.__mat_affine, (x_1, y, 1.0))

            self.create_line(widget_point0[0], widget_point0[1],
                             widget_point1[0], widget_point1[1], fill=self.__grid_color)

    def _draw_bright(self, left, top, right, bottom, pillow_image):
        '''
        画素座標、輝度値の描画
        '''
        if self.__bright_enabled is False:
            return

        pixel_size = self.__mat_affine[0, 0]

        if pixel_size < 55:
            # １画素のサイズが55画素以下の場合は表示しない
            return

        # 画像表示領域
        x_0, y_0, x_1, y_1 = self._disp_image_rect(left, top, right, bottom)

        data = self.disp_image.getdata()  # type: ignore

        width = self.disp_image.width  # type: ignore

        draw = ImageDraw.Draw(pillow_image)

        # if data.mode == "L":
        if data.bands == 1:
            # モノクロのとき
            for y in range(y_0, y_1):
                index = y * width
                for x in range(x_0, x_1):
                    val = data[x + index]
                    if val < 127:
                        col = 255
                    else:
                        col = 0
                    locate = np.dot(self.__mat_affine, (x, y, 1.0))
                    draw.text((locate[0] + 1 - left, locate[1] + 1 - top),
                              "({0}, {1})".format(x, y), fill=col, anchor="la")
                    draw.text((locate[0] + pixel_size * 0.5 - left, locate[1] +
                              pixel_size * 0.5 - top), "{0}".format(val), fill=col)

        else:
            # カラーのとき
            col_r = "#C80096"
            col_g = "#96C800"
            col_b = "#0096C8"
            for y in range(y_0, y_1):
                index = y * width
                for x in range(x_0, x_1):
                    val = data[x + index]
                    if val[0] + val[1] + val[2] < 381:
                        col = "#FFFFFF"
                    else:
                        col = "#000000"
                    locate = np.dot(self.__mat_affine, (x, y, 1.0))
                    draw.text((locate[0] + 1 - left, locate[1] + 1 - top),
                              "({0}, {1})".format(x, y), fill=col, anchor="la")
                    p_x = locate[0] + pixel_size * 0.5 - left
                    draw.text(
                        (p_x, locate[1] + pixel_size * 0.5 - 15 - top), "{0:>3}".format(val[0]), fill=col_r)
                    draw.text(
                        (p_x, locate[1] + pixel_size * 0.5 - top), "{0:>3}".format(val[1]), fill=col_g)
                    draw.text(
                        (p_x, locate[1] + pixel_size * 0.5 + 15 - top), "{0:>3}".format(val[2]), fill=col_b)

    def _draw_bright_create_text(self, left, top, right, bottom):
        '''
        画素座標、輝度値の描画
        '''
        if self.__bright_enabled is False:
            return

        pixel_size = self.__mat_affine[0, 0]

        if pixel_size < 20:
            # １画素のサイズが20画素以下の場合は表示しない
            return

        font_size = int(pixel_size / 8 + 0.5)  # フォントサイズ（セルの１/４）
        if font_size < 5:
            return  # フォントが小さくて表示できない

        # 画像表示領域
        x_0, y_0, x_1, y_1 = self._disp_image_rect(left, top, right, bottom)

        # font_type = ('Tahoma', font_size)
        font_type = ('', font_size)
        font_data = ('', font_size + 2)

        data = self.disp_image.getdata()  # type: ignore

        width = self.disp_image.width  # type: ignore

        # if data.mode == "L":
        if data.bands == 1:
            # モノクロのとき
            for y in range(y_0, y_1):
                index = y * width
                for x in range(x_0, x_1):
                    val = data[x + index]
                    if val < 127:
                        col = "#FFFFFF"
                    else:
                        col = "#000000"
                    locate = np.dot(self.__mat_affine, (x, y, 1.0))
                    self.create_text(
                        locate[0] + 1, locate[1] + 1, text=f"({x}, {y})", font=font_type, fill=col, anchor=tk.NW)
                    self.create_text(locate[0] + pixel_size, locate[1] + pixel_size,
                                     text=f"{val}", font=font_type, fill=col, anchor=tk.SE)
        else:
            # カラーのとき
            col_r = "#C80096"
            col_g = "#96C800"
            col_b = "#0096C8"
            for y in range(y_0, y_1):
                index = y * width
                for x in range(x_0, x_1):
                    val = data[x + index]
                    if val[0] + val[1] + val[2] < 381:
                        col = "#FFFFFF"
                    else:
                        col = "#000000"
                    locate = np.dot(self.__mat_affine, (x, y, 1.0))
                    self.create_text(
                        locate[0] + 1, locate[1] + 1, text=f"({x}, {y})", font=font_type, fill=col, anchor=tk.NW)
                    p_x = locate[0] + pixel_size
                    self.create_text(
                        p_x, locate[1] + pixel_size * 0.25, text=f"{val[0]}", font=font_data, fill=col_r, anchor=tk.NE)
                    self.create_text(
                        p_x, locate[1] + pixel_size * 0.5, text=f"{val[1]}", font=font_data, fill=col_g, anchor=tk.NE)
                    self.create_text(
                        p_x, locate[1] + pixel_size * 0.75, text=f"{val[2]}", font=font_data, fill=col_b, anchor=tk.NE)

    def _draw_profile(self, left, top, right, bottom, max_value=255):
        '''
        プロファイルの描画
        '''
        if self.__profile_enabled is False:
            return

        # ウィジェットのサイズ
        wig_width = self.winfo_width()
        wig_height = self.winfo_height()

        # 画像表示領域
        x_0, y_0, x_1, y_1 = self._disp_image_rect(left, top, right, bottom)

        data = self.disp_image.getdata()   # type: ignore  # 表示画像データ
        width = self.disp_image.width  # type: ignore
        height = self.disp_image.height  # type: ignore

        mat = self.__mat_affine.copy()
        mat_inv = np.linalg.inv(mat)

        # プロファイル表示位置の画像の座標
        image_point = np.dot(
            mat_inv, (self.__profile_x, self.__profile_y, 1.0))

        x_enable = False
        if image_point[1] >= 0 and image_point[1] < height:
            x_enable = True
        y_enable = False
        if image_point[0] >= 0 and image_point[0] < width:
            y_enable = True

        # クロスビームの描画
        if x_enable is True:
            self.create_line(0, self.__profile_y, wig_width,
                             self.__profile_y, fill=self.__cross_beam_color)
        if y_enable is True:
            self.create_line(self.__profile_x, 0, self.__profile_x,
                             wig_height, fill=self.__cross_beam_color)

        scale_color = "#AAAA00"  # 目盛線の色
        scale_offset = 10  # 原点までの表示位置のオフセット

        pixel_size = self.disp_scale

        if x_enable is True:
            # 横目盛りの描画(実線)
            for i in range(0, 5, 2):
                y = wig_height - scale_offset - i * self.__profile_height / 4.0
                self.create_line(left, y,
                                 right, y,
                                 fill=scale_color)

            # 横目盛りの描画(点線)
            for i in range(1, 5, 2):
                y = wig_height - scale_offset - i * self.__profile_height / 4.0
                self.create_line(left, y,
                                 right, y,
                                 fill=scale_color,
                                 dash=(3, 1))

            index = int(np.floor(image_point[1])) * width

            # if data.mode == "L":
            if data.bands == 1:
                # モノクロのとき
                points = []
                if pixel_size < 1:
                    for x in range(x_0, x_1):
                        widget_point = np.dot(self.__mat_affine, (x, 0, 1.0))
                        points.append(
                            (widget_point[0], wig_height - scale_offset - self.__profile_height * data[x + index] / max_value))
                else:
                    for x in range(x_0, x_1):
                        widget_point = np.dot(self.__mat_affine, (x, 0, 1.0))
                        y = wig_height - scale_offset - \
                            self.__profile_height * data[x + index] / max_value
                        points.append((widget_point[0], y))
                        points.append((widget_point[0] + pixel_size, y))

                if len(points) > 0:
                    flattened = [a for x in points for a in x]
                    self.create_line(
                        *flattened, fill=self.__profile_x_color, width=1 + pixel_size / 20)

            else:
                # カラーのとき
                points_r = []
                points_g = []
                points_b = []
                if pixel_size < 1:
                    for x in range(x_0, x_1):
                        widget_point = np.dot(self.__mat_affine, (x, 0, 1.0))
                        val = data[x + index]
                        points_r.append(
                            (widget_point[0], wig_height - scale_offset - self.__profile_height * val[0] / max_value))
                        points_g.append(
                            (widget_point[0], wig_height - scale_offset - self.__profile_height * val[1] / max_value))
                        points_b.append(
                            (widget_point[0], wig_height - scale_offset - self.__profile_height * val[2] / max_value))
                else:
                    for x in range(x_0, x_1):
                        widget_point = np.dot(self.__mat_affine, (x, 0, 1.0))
                        val = data[x + index]
                        y = wig_height - scale_offset - \
                            self.__profile_height * val[0] / max_value
                        points_r.append((widget_point[0], y))
                        points_r.append((widget_point[0] + pixel_size, y))
                        y = wig_height - scale_offset - \
                            self.__profile_height * val[1] / max_value
                        points_g.append((widget_point[0], y))
                        points_g.append((widget_point[0] + pixel_size, y))
                        y = wig_height - scale_offset - \
                            self.__profile_height * val[2] / max_value
                        points_b.append((widget_point[0], y))
                        points_b.append((widget_point[0] + pixel_size, y))

                if len(points_r) > 0:
                    flattened = [a for x in points_r for a in x]
                    self.create_line(*flattened, fill="#DC0000",
                                     width=1 + pixel_size / 20)
                    flattened = [a for x in points_g for a in x]
                    self.create_line(*flattened, fill="#006000",
                                     width=1 + pixel_size / 20)
                    flattened = [a for x in points_b for a in x]
                    self.create_line(*flattened, fill="#0000DC",
                                     width=1 + pixel_size / 20)

        if y_enable is True:
            # 縦目盛りの描画(実線)
            for i in range(0, 5, 2):
                x = wig_width - scale_offset - i * self.__profile_height / 4.0
                self.create_line(x, top,
                                 x, bottom,
                                 fill=scale_color)

            # 縦目盛りの描画(点線)
            for i in range(1, 5, 2):
                x = wig_width - scale_offset - i * self.__profile_height / 4.0
                self.create_line(x, top,
                                 x, bottom,
                                 fill=scale_color,
                                 dash=(3, 1))

            index = int(np.floor(image_point[0]))

            # if data.mode == "L":
            if data.bands == 1:
                # モノクロのとき
                points = []
                if pixel_size < 1:
                    for y in range(y_0, y_1):
                        widget_point = np.dot(self.__mat_affine, (0, y, 1.0))
                        points.append((wig_width - scale_offset - self.__profile_height *
                                      data[index + y * width] / max_value, widget_point[1]))
                else:
                    for y in range(y_0, y_1):
                        widget_point = np.dot(self.__mat_affine, (0, y, 1.0))
                        x = wig_width - scale_offset - self.__profile_height * \
                            data[index + y * width] / max_value
                        points.append((x, widget_point[1]))
                        points.append((x, widget_point[1] + pixel_size))

                if len(points) > 0:
                    flattened = [a for y in points for a in y]
                    self.create_line(
                        *flattened, fill=self.__profile_y_color, width=1 + pixel_size / 20)

            else:
                # カラーのとき
                points_r = []
                points_g = []
                points_b = []
                if pixel_size < 1:
                    for y in range(y_0, y_1):
                        widget_point = np.dot(self.__mat_affine, (0, y, 1.0))
                        val = data[index + y * width]
                        points_r.append(
                            (wig_width - scale_offset - self.__profile_height * val[0] / max_value, widget_point[1]))
                        points_g.append(
                            (wig_width - scale_offset - self.__profile_height * val[1] / max_value, widget_point[1]))
                        points_b.append(
                            (wig_width - scale_offset - self.__profile_height * val[2] / max_value, widget_point[1]))
                else:
                    for y in range(y_0, y_1):
                        widget_point = np.dot(self.__mat_affine, (0, y, 1.0))
                        val = data[index + y * width]
                        x = wig_width - scale_offset - \
                            self.__profile_height * val[0] / max_value
                        points_r.append((x, widget_point[1]))
                        points_r.append((x, widget_point[1] + pixel_size))
                        x = wig_width - scale_offset - \
                            self.__profile_height * val[1] / max_value
                        points_g.append((x, widget_point[1]))
                        points_g.append((x, widget_point[1] + pixel_size))
                        x = wig_width - scale_offset - \
                            self.__profile_height * val[2] / max_value
                        points_b.append((x, widget_point[1]))
                        points_b.append((x, widget_point[1] + pixel_size))

                if len(points_r) > 0:
                    flattened = [a for x in points_r for a in x]
                    self.create_line(*flattened, fill="#DC0000",
                                     width=1 + pixel_size / 20)
                    flattened = [a for x in points_g for a in x]
                    self.create_line(*flattened, fill="#006000",
                                     width=1 + pixel_size / 20)
                    flattened = [a for x in points_b for a in x]
                    self.create_line(*flattened, fill="#0000DC",
                                     width=1 + pixel_size / 20)

    def _check_color_name(self, color_name):
        '''Is the color naming convention correct? '''
        try:
            self.winfo_rgb(color_name)
            return True
        except tk.TclError:
            print("[Error] Wrong color name:", color_name)
            return False
