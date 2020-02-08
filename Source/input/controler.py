#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""controler.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

コントローラモジュール。
"""
import io as _io
import pygame as _pygame
import pygame.joystick as _joystick
import pygame.key as _key
import sprites as _sprites
import utils.const as _const


def init():
    u"""初期化処理。
    """
    import os as __os
    import inventories as __inventories
    config_dir = __inventories.get_config_dir()
    _Controler.config_file = __os.path.join(config_dir, "keyconf.txt")
    if not __os.path.exists(_Controler.config_file):
        if not __os.path.exists(config_dir):
            __os.makedirs(config_dir, mode=0o775)
        with _io.open(_Controler.config_file, "w") as out:
            out.write(
                u"# Key Assignment.\n"
                u"\n"
                u"# Keyboard.\n"
                u"# Refer. https://www.pygame.org/docs/ref/key.html\n"
                u"UP_KEY = K_w, K_UP\n"
                u"RIGHT_KEY = K_d, K_RIGHT\n"
                u"LEFT_KEY = K_a, K_LEFT\n"
                u"DOWN_KEY = K_s, K_DOWN\n"
                u"DECISION_KEY = K_l\n"
                u"CANCEL_KEY = K_k\n"
                u"HOLD_KEY = K_i\n"
                u"REMOVE_KEY = K_j\n"
                u"DELETE_KEY = K_q\n"
                u"USE_KEY = K_e\n"
                u"SELECT_KEY = K_BACKSPACE\n"
                u"START_KEY = K_SPACE\n"
                u"USE1_KEY = K_1\n"
                u"USE2_KEY = K_2\n"
                u"USE3_KEY = K_3\n"
                u"USE4_KEY = K_4\n"
                u"USE5_KEY = K_5\n"
                u"USE6_KEY = K_6\n"
                u"USE7_KEY = K_7\n"
                u"USE8_KEY = K_8\n"
                u"VOLUMEUP_KEY = K_SEMICOLON, K_KP_PLUS\n"
                u"VOLUMEDOWN_KEY = K_MINUS, K_KP_MINUS\n"
                u"MUTE_KEY = K_SLASH, K_KP_DIVIDE\n"
                u"\n"
                u"# Game Pad.\n"
                u"# In the range 0 to 7\n"
                u"# 1P Setting.\n"
                u"DECISION_BUTTON_1P = 0\n"
                u"CANCEL_BUTTON_1P = 1\n"
                u"HOLD_BUTTON_1P = 2\n"
                u"REMOVE_BUTTON_1P = 3\n"
                u"DELETE_BUTTON_1P = 4\n"
                u"USE_BUTTON_1P = 5\n"
                u"SELECT_BUTTON_1P = 6\n"
                u"START_BUTTON_1P = 7\n"
                u"# 2P Setting.\n"
                u"DECISION_BUTTON_2P = 0\n"
                u"CANCEL_BUTTON_2P = 1\n"
                u"HOLD_BUTTON_2P = 2\n"
                u"REMOVE_BUTTON_2P = 3\n"
                u"DELETE_BUTTON_2P = 4\n"
                u"USE_BUTTON_2P = 5\n"
                u"SELECT_BUTTON_2P = 6\n"
                u"START_BUTTON_2P = 7\n"
                u"\n")


def is_second_playable():
    u"""2P使用可能な場合に真。
    """
    return 2 <= _joystick.get_count()


class _Controler(object):
    u"""入出力制御。
    """
    __slots__ = (
        "_added", "__buttons", "__keyboard", "__id", "__interval",
        "__is_init_error", "__is_input_error", "__is_keyboard_available",
        "_joystick", "__presseds", "__pressure", "__queue", "__speed")
    _DECISION = "DECISION"
    _CANCEL = "CANCEL"
    _HOLD = "HOLD"
    _REMOVE = "REMOVE"
    _DELETE = "DELETE"
    _USE = "USE"
    _SELECT = "SELECT"
    _START = "START"
    _UP = "UP"
    _RIGHT = "RIGHT"
    _LEFT = "LEFT"
    _DOWN = "DOWN"
    _USE1 = "USE1"
    _USE2 = "USE2"
    _USE3 = "USE3"
    _USE4 = "USE4"
    _USE5 = "USE5"
    _USE6 = "USE6"
    _USE7 = "USE7"
    _USE8 = "USE8"
    _VOLUMEUP = "VOLUMEUP"
    _VOLUMEDOWN = "VOLUMEDOWN"
    _MUTE = "MUTE"
    __CORRECT_WORD = (
        _DECISION, _CANCEL, _HOLD, _REMOVE,
        _DELETE, _USE, _SELECT, _START,
        _UP, _RIGHT, _LEFT, _DOWN,
        _USE1, _USE2, _USE3, _USE4,
        _USE5, _USE6, _USE7, _USE8,
        _VOLUMEUP, _VOLUMEDOWN, _MUTE)

    def __init__(self, id_):
        u"""コンストラクタ。
        """
        import inventories as __inventories

        def __set_keys():
            u"""キー設定。
            """
            def __parse():
                u"""lineを解析して変数に設定。
                """
                text = line.replace("\n", "").replace(" ", "")
                if text and not text[0] == "#":
                    key, values = text.split("=")
                    set_key, value_type = key.split("_", 1)
                    if value_type.upper() == "KEY":
                        result = []
                        for value in values.split(","):
                            try:
                                result.append(getattr(_pygame, value))
                            except AttributeError:
                                pass
                            if set_key in self.__CORRECT_WORD:
                                self.__keyboard[set_key.upper()] =\
                                    tuple(result)
                    else:
                        value_type, player = value_type.split("_")
                        if value_type.upper() == "BUTTON":
                            if set_key in self.__CORRECT_WORD:
                                try:
                                    if self.__id == 0 and player == "1P":
                                        self.__buttons[set_key.upper()] =\
                                            int(values)
                                    elif self.__id == 1 and player == "2P":
                                        self.__buttons[set_key.upper()] =\
                                            int(values)
                                except ValueError:
                                    pass
            try:
                with _io.open(_Controler.config_file, "r") as out:
                    for line in out:
                        __parse()
            except (IOError, UnicodeDecodeError):
                pass
            for key, value in (
                (self._DECISION, (_pygame.K_l,)),
                (self._CANCEL, (_pygame.K_k,)),
                (self._HOLD, (_pygame.K_i,)),
                (self._REMOVE, (_pygame.K_j,)),
                (self._DELETE, (_pygame.K_q,)),
                (self._USE, (_pygame.K_e,)),
                (self._SELECT, (_pygame.K_BACKSPACE,)),
                (self._START, (_pygame.K_SPACE,)),
                (self._UP, (_pygame.K_w, _pygame.K_UP)),
                (self._RIGHT, (_pygame.K_d, _pygame.K_RIGHT)),
                (self._LEFT, (_pygame.K_a, _pygame.K_LEFT)),
                (self._DOWN, (_pygame.K_s, _pygame.K_DOWN)),
                (self._USE1, (_pygame.K_1,)),
                (self._USE2, (_pygame.K_2,)),
                (self._USE3, (_pygame.K_3,)),
                (self._USE4, (_pygame.K_4,)),
                (self._USE5, (_pygame.K_5,)),
                (self._USE6, (_pygame.K_6,)),
                (self._USE7, (_pygame.K_7,)),
                (self._USE8, (_pygame.K_8,)),
                (self._VOLUMEUP, (_pygame.K_SEMICOLON, _pygame.K_KP_PLUS)),
                (self._VOLUMEDOWN, (_pygame.K_MINUS, _pygame.K_KP_MINUS)),
                (self._MUTE, (_pygame.K_SLASH, _pygame.K_KP_DIVIDE)),
            ):
                if key not in self.__keyboard or not self.__keyboard[key]:
                    self.__keyboard[key] = value
            for key, value in (
                (self._DECISION, 0), (self._CANCEL, 1),
                (self._HOLD, 2), (self._REMOVE, 3),
                (self._DELETE, 4), (self._USE, 5),
                (self._SELECT, 6), (self._START, 7)
            ):
                if key not in self.__buttons:
                    self.__buttons[key] = value
        self.__id = id_
        self.__queue = ""
        self._added = ""
        self.__presseds = ""
        self.__keyboard = {}
        self.__buttons = {}
        self.__speed = __inventories.General.get_speed()+1
        self.__interval = _const.FRAME_RATE >> 1
        self.__pressure = 0
        self.__is_keyboard_available = True
        if _joystick.get_count():
            self._joystick = _joystick.Joystick(self.__id)
            try:
                self._joystick.init()
                self.__is_init_error = False
            except _pygame.error:
                _sprites.Notice.notify(
                    "CONTROLER INITIALIZE ERROR", is_warning=True)
                self.__is_init_error = True
        __set_keys()
        self.__is_input_error = False

    def _add_command(self, decision, added):
        u"""キューにコマンド追加。
        """
        if decision:
            if added not in self.__presseds:
                self.__queue += added
                self.__presseds += added
        else:
            self.__presseds = self.__presseds.replace(added, "")

    def _is_pressed(self, pressed, keys):
        u"""キーが押されている場合に真。
        """
        return (
            self.__is_keyboard_available and
            any(pressed[key] for key in self.__keyboard[keys]))

    def input(self):
        u"""キューを生成。
        """
        def __x_axis_input(x):
            u"""x軸入力。
            """
            pressed = _key.get_pressed()
            is_right = self._is_pressed(pressed, self._RIGHT) or x == 1
            is_left = self._is_pressed(pressed, self._LEFT) or x == -1
            if not (is_right and is_left):
                if is_right:
                    self._added = self._added+_const.RIGHT_COMMAND
                elif is_left:
                    self._added = self._added+_const.LEFT_COMMAND

        def __key_input():
            u"""キー・ジョイスティック入力。
            """
            pressed = _key.get_pressed()
            for key, command in (
                (self._DECISION, _const.DECISION_COMMAND),
                (self._CANCEL, _const.CANCEL_COMMAND),
                (self._HOLD, _const.HOLD_COMMAND),
                (self._REMOVE, _const.REMOVE_COMMAND),
                (self._DELETE, _const.DELETE_COMMAND),
                (self._USE, _const.USE_COMMAND),
                (self._SELECT, _const.SELECT_COMMAND),
                (self._START, _const.START_COMMAND),
                (self._USE1, _const.USE1_COMMAND),
                (self._USE2, _const.USE2_COMMAND),
                (self._USE3, _const.USE3_COMMAND),
                (self._USE4, _const.USE4_COMMAND),
                (self._USE5, _const.USE5_COMMAND),
                (self._USE6, _const.USE6_COMMAND),
                (self._USE7, _const.USE7_COMMAND),
                (self._USE8, _const.USE8_COMMAND)
            ):
                try:
                    has_key = _joystick.get_count() and key in self.__buttons
                    is_button_pressed = (
                        self._joystick.get_button(self.__buttons[key]) if
                        has_key else False)
                    self._add_command(
                        self._is_pressed(pressed, key) or
                        is_button_pressed, command)
                except _pygame.error:
                    if not self.__is_input_error:
                        self.__is_input_error = True
                        _sprites.Notice.notify(
                            "CONTROLER INPUT ERROR", is_warning=True)

        def __volume_input():
            u"""ボリューム入力。
            """
            if self.__id == 0:
                pressed = _key.get_pressed()
                volume_up = any(
                    pressed[key] for key in self.__keyboard[self._VOLUMEUP])
                volume_down = any(
                    pressed[key] for key in self.__keyboard[self._VOLUMEDOWN])
                if not (volume_up and volume_down):
                    if volume_up:
                        self._added += _const.VOLUMEUP_COMMAND
                    elif volume_down:
                        self._added += _const.VOLUMEDOWN_COMMAND
                self._add_command(
                    any(pressed[key] for key in self.__keyboard[self._MUTE]),
                    _const.MUTE_COMMAND)

        def __shift():
            u"""キーを押した時の変速処理。
            """
            if self.__pressure % self.__interval == 0:
                self.__pressure = 0
                self.__queue = self.__queue+self._added
            if self._added:
                self.__pressure += 1
                if self.__speed << 1 < self.__interval:
                    self.__interval -= 1
            else:
                self.__pressure = 0
                self.__interval = _const.FRAME_RATE >> 1
        self._added = ""
        is_joystick = bool(_joystick.get_count())
        __x_axis_input(
            round(self._joystick.get_axis(0)) if is_joystick else 0)
        self._y_axis_input(
            round(self._joystick.get_axis(1)) if is_joystick else 0)
        __key_input()
        __volume_input()
        __shift()

    def output(self, all_com=True):
        u"""コマンドをひとつだけ返す。
        """
        if self.__queue:
            if all_com:
                result = self.__queue
                self.__queue = ""
                return result
            else:
                command = self.__queue[0]
                self.__queue = self.__queue[1:]
                return command
        else:
            return ""

    @property
    def is_keyboard_available(self):
        u"""キーボード使用可能状態取得。
        """
        return self.__is_keyboard_available

    @is_keyboard_available.setter
    def is_keyboard_available(self, value):
        u"""キーボード使用可能状態設定。
        """
        self.__is_keyboard_available = value

    @property
    def is_init_error(self):
        u"""コントローラの初期化に失敗した場合に真。
        """
        return self.__is_init_error


class Main(_Controler):
    u"""メインゲームコントローラ。
    """
    __slots__ = ()

    def _y_axis_input(self, y):
        u"""y軸入力。
        """
        pressed = _key.get_pressed()
        if not (
            self._is_pressed(pressed, self._UP) and
            self._is_pressed(pressed, self._DOWN)
        ):
            if self._is_pressed(pressed, self._DOWN) or y == 1:
                self._added = self._added+_const.DOWN_COMMAND
        self._add_command(
            self._is_pressed(pressed, self._UP) or y == -1, _const.UP_COMMAND)


class Menu(_Controler):
    u"""メニュー画面コントローラ。
    """
    __slots__ = ()

    def _y_axis_input(self, y):
        u"""y軸入力。
        """
        pressed = _key.get_pressed()
        is_up = self._is_pressed(pressed, self._UP) or y == -1
        is_down = self._is_pressed(pressed, self._DOWN) or y == 1
        if not (is_up and is_down):
            if is_up:
                self._added = self._added+_const.UP_COMMAND
            elif is_down:
                self._added = self._added+_const.DOWN_COMMAND
