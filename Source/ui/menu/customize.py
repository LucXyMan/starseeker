#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""customizeize.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

カスタマイズ画面モジュール。
"""
import armament.collectible as _collectible
import armament.equips as _equips
import armament.units as _units
import armament.skill as _skill
import inventories as _inventories
import material.sound as _sound
import sprites as _sprites
import sprites.huds as __huds
import ui.content as _content
import ui.label as _label
import utils.const as _const
import utils.layouter as _layouter
import ui.window as _window


class PlayerImage(__huds.HUD):
    u"""現在プレイヤー表示。
    """
    def __init__(self, gropus=None):
        u"""コンストラクタ。
        """
        import armament.units as __units
        super(PlayerImage, self).__init__(gropus)
        self.__images = tuple(
            player.get_image(True, False) for
            player in __units.get_players()[:-1])
        self.__old = -1
        self.update()

    def update(self):
        u"""画像更新処理。
        """
        player = _inventories.Utils.get_player()
        if self.__old != player:
            self.image = self.__images[player]
            if hasattr(self, "rect"):
                self.rect.size = self.image.get_size()
            else:
                self.rect = self.image.get_rect()
            _layouter.Menu.set_player(self)
            self.__old = player


class StatusWindow(_sprites.Window):
    u"""ステータス表示ウィンドウ。
    """
    __MATRIX = 9, 4

    def __init__(self, pos, content, groups=None):
        u"""コンストラクタ。
        """
        import pygame as __pygame

        class _ParamString(_sprites.String):
            u"""ゲームパラメータ文字列。
            """
            def __init__(self, pos, groups):
                u"""コンストラクタ。
                """
                super(_ParamString, self).__init__(
                    pos, "", _const.SYSTEM_CHAR_SIZE,
                    shorten=False, groups=groups)

        class __SlotString(_ParamString):
            u"""スロット文字列。
            """
            def update(self):
                u"""スプライト更新。
                """
                self.string = "CAP:{0: >3}/{1: >2}".format(
                    _inventories.Skill.get_used_slot(), _const.SKILL_CAPACITY)

        class __DeckString(_ParamString):
            u"""デッキ文字列。
            """
            def update(self):
                u"""スプライト更新。
                """
                self.string = "DECK:{0: >2}/{1: >2}".format(
                    _inventories.Deck.get_total(), _const.DECK_CAPACITY)

        class _StatusString(_ParamString):
            u"""ステータス文字列。
            """
            def __init__(self, pos, content, groups):
                u"""コンストラクタ。
                """
                self._content = content
                super(_StatusString, self).__init__(pos, groups=groups)

            def _update_color(self, difference):
                u"""文字色の更新。
                difference: パラメータの比較結果。
                """
                self.color = (
                    _const.RED+"##" if 0 < difference else
                    _const.CYAN+"##" if 0 > difference else "##")

        class __AttackString(_StatusString):
            u"""攻撃数値文字列。
            """
            def update(self):
                u"""スプライト更新。
                """
                str_ = _units.get_player(_inventories.Utils.get_player()).str
                attack = str_+_equips.get(_inventories.Equip.get(0)).value
                window = self._content.active_window
                difference = has = 0
                cursor = -1
                if window and self._content.is_item_selected:
                    cursor = window.cursor+1
                    compare = _equips.get(cursor)
                    if compare.is_weapon:
                        has = _inventories.Items.has(cursor-1)
                        compare_attack = str_+compare.value
                        difference = attack-compare_attack
                is_useable = (
                    has and _inventories.Skill.is_item_equippable(
                        _equips.get(compare.number)))
                high_low = difference if is_useable else 0
                self.string = "ATK:{0: >3}".format(
                    compare_attack if high_low else attack)
                self._update_color(high_low)

        class __DefenceString(_StatusString):
            u"""防御数値文字列。
            """
            def update(self):
                u"""スプライト更新。
                """
                Items = _inventories.Items
                Equip = _inventories.Equip
                Skill = _inventories.Skill
                armors = tuple(Equip.get(armor) for armor in range(1, 4))
                get = _equips.get
                defence = sum(get(armor).value for armor in armors)
                content = self._content
                active_window = content.active_window
                difference = has = 0
                cursor = -1
                if active_window and content.is_item_selected:
                    cursor = active_window.cursor+1
                    has = Items.has(cursor-1)
                    compare = get(cursor)
                    if compare.is_armor:
                        equip_slot = compare.type
                        compare_defence = sum(
                            get(armor).value for armor in
                            armors[:equip_slot-1]+(compare.number,) +
                            armors[equip_slot:])
                        difference = defence-compare_defence
                is_useable = has and Skill.is_item_equippable(
                    _equips.get(compare.number))
                high_low = difference if is_useable else 0
                self.string = "DEF: {0: >2}".format(
                    compare_defence if high_low else defence)
                self._update_color(high_low)
        col, row = self.__MATRIX
        super(StatusWindow, self).__init__(
            pos, __pygame.Surface((_const.GRID*col, _const.GRID*row)), groups)
        self.__strings = []
        for i, String in enumerate((
            __AttackString, __DefenceString, __SlotString, __DeckString
        )):
            string = (
                String((0, 0), content, ()) if i in range(2) else
                String((0, 0), ()))
            string.rect.midleft = 0, (_const.GRID >> 1)+_const.GRID*i
            self.__strings.append(string)
        _layouter.Menu.set_status(self)

    def update(self):
        u"""ウィンドウの更新処理。
        """
        import utils.image as __image

        def __string_blit():
            u"""文字列書き込み。
            """
            for string in self.__strings:
                string.update()
                self.image.blit(string.image, string.rect.topleft)
        col, row = self.__MATRIX
        self.image.blit(__image.get_checkered(col, row, 1), (0, 0))
        __string_blit()


class EquipWindow(_window.Label):
    u"""装備ウィンドウ。
    """
    def __init__(self, pos, groups=None):
        u"""コンストラクタ。
        """
        x, y = pos
        w, h = _const.GRID*9, _const.GRID*4
        super(EquipWindow, self).__init__((x, y, w, h), (9, 4), groups)
        self._items = tuple(
            _label.Equip((0, i*_const.GRID), i, ()) for i in range(4))
        _layouter.Menu.set_equip(self)


class Customize(_content.Control):
    u"""装備設定画面。
    """
    __slots__ = "_cmds",
    __PLAYER_NUMBER = 8
    __MATRIX = _content.Control.WINDOW_ROW, 4
    __ITEM_MATRIX = _content.Control.WINDOW_ROW, 20
    __SKILL_MATRIX = _content.Control.WINDOW_ROW, 16
    __DECK_MATRIX = _content.Control.WINDOW_ROW, 10

    def __init__(self):
        u"""コンストラクタ。
        """
        import material.misc as __misc
        import utils.image as __image
        import utils.screen as __screen

        def __init_controls():
            u"""操作ウィンドウの初期設定。
            """
            import icon as __icon
            col, row = self.__MATRIX
            self._controls = []
            window = _window.Icon((
                0, 0, col*_const.GRID, row*_const.GRID), self.__ITEM_MATRIX)
            for equip in _equips.get_all()[1:]:
                window.append(__icon.Item((0, 0), equip, ()))
            self._controls.append(window)
            window = _window.Label(
                (0, 0, col*_const.GRID, row*_const.GRID), self.__SKILL_MATRIX)
            for equip in range(_inventories.Skill.get_limit()):
                window.append(_label.Skill((0, 0), equip, ()))
            self._controls.append(window)
            window = _window.Icon(
                (0, 0, col*_const.GRID, row*_const.GRID), self.__DECK_MATRIX)
            for equip in (
                collection for collection in _collectible.get_all() if
                collection.type in (
                    _const.SUMMON_ARCANUM, _const.SORCERY_ARCANUM,
                    _const.SUPPORT_ARCANUM, _const.SHIELD_ARCANUM)
            ):
                window.append(__icon.Card((0, 0), equip, ()))
            self._controls.append(window)
            _layouter.Menu.set_controls(self._controls)
        super(Customize, self).__init__()
        PlayerImage()
        __init_controls()
        self.cursor = 0
        EquipWindow((0, 0))
        StatusWindow((0, 0), self)
        __image.BackGround.set_image(__misc.get("crypt"))
        __image.BackGround.transcribe(__screen.Screen.get_base())
        self._update_info()

    def _update_info(self):
        u"""情報を更新。
        """
        window = self.active_window
        rise_and_fall_text = u"決定・リムーブキーで増減#ホールドキーでゼロに"
        try:
            if window:
                info = (_equips.get(
                    window.cursor+1).info if self._cursor == 0 else
                    _skill.get(
                        _inventories.Utils.get_learnable()[window.cursor]
                    ).get_info() if self._cursor == 1 else
                    _collectible.get(window.cursor).info+"#" +
                    rise_and_fall_text)
            else:
                info = (
                    u"アイテム設定#{info}" if self._cursor == 0 else
                    u"スキル設定#{info}" if self._cursor == 1 else
                    u"デッキ設定#{info}").format(info=self._PLAYER_SELECT_TEXT)
            _sprites.Info.send(info)
        except IndexError:
            _sprites.Info.send("")

    def eliminate(self):
        u"""パースの削除処理。
        """
        self.__status.kill()
        self.__equips.kill()
        super(Customize, self).eliminate()

    # ---- Command ----
    def __player_chang(self, value):
        u"""プレイヤー変更。
        """
        player = _inventories.Utils.get_player()
        _inventories.Utils.set_player((player+value) % _const.PLEYERS)
        if _inventories.Utils.get_player() != player:
            _sound.SE.play("cursor_1")
        if self.active_window and self.is_skill_selected:
            self._update_info()
        return _const.IGNORE_STATUS

    def decision(self):
        u"""決定キー処理。
        """
        def __item_decision():
            u"""アイテム決定。
            """
            equip = _equips.get(self.active_window.cursor+1)
            if _inventories.Items.has(equip.number-1):
                if _inventories.Equip.get(equip.type) != equip.number:
                    if _inventories.Skill.is_item_equippable(
                        _equips.get(equip.number)
                    ):
                        _sound.SE.play("decision")
                        _inventories.Equip.set(equip.type, equip.number)
                    else:
                        _sound.SE.play("error")
            elif not equip.is_locked and not equip.is_sealed:
                _inventories.SP.buy_item(equip)
                self._update_info()
            else:
                _sound.SE.play("error")

        def __skill_decision():
            u"""スキル決定。
            """
            window = self.active_window
            player = _units.get_player(_inventories.Utils.get_player())
            try:
                learn = _skill.get(player.learnable[window.cursor])
            except IndexError:
                return
            if (
                learn.number in player.learnable and
                _inventories.Skill.has(window.cursor)
            ):
                _sound.SE.play("cancel")
                _inventories.Skill.off(window.cursor)
            elif (
                learn.slot+_inventories.Skill.get_used_slot() <=
                _const.SKILL_CAPACITY and learn.is_equippable
            ):
                _sound.SE.play("decision")
                _inventories.Skill.on(window.cursor)
            else:
                _sound.SE.play("error")

        def __card_decision():
            u"""カード決定。
            """
            arcnaum = _collectible.get(self.active_window.cursor)
            if _inventories.Deck.get_total() < _const.DECK_CAPACITY:
                number = _inventories.Deck.get(arcnaum.number)
                _number = number+1
                limit = _inventories.Card.get(arcnaum.number)
                _inventories.Deck.set(
                    arcnaum.number, _number if _number < limit else limit)
                if number != _inventories.Deck.get(arcnaum.number):
                    _sound.SE.play("decision")
                else:
                    _sound.SE.play("error")
            else:
                _sound.SE.play("error")
        window = self.active_window
        if not window:
            self._controls[self._cursor].is_active = True
            self._update_info()
        else:
            if self.is_item_selected:
                __item_decision()
            elif self.is_skill_selected:
                __skill_decision()
            elif self.is_card_selected:
                __card_decision()
        return _const.IGNORE_STATUS

    def cancel(self):
        u"""取り消しキー処理。
        """
        window = self.active_window
        if window:
            window.is_active = False
            self._update_info()
            return _const.IGNORE_STATUS
        else:
            return _const.EXIT_STATUS

    def hold(self):
        u"""ホールドキー処理。
        """
        window = self.active_window
        if window and self.is_card_selected:
            card = _collectible.get(window.cursor)
            number = _inventories.Deck.get(card.number)-1
            _inventories.Deck.set(_collectible.get(window.cursor).number, 0)
            if number != _inventories.Deck.get(card.number)-1:
                _sound.SE.play("cancel")
        return _const.IGNORE_STATUS

    def remove(self):
        u"""リムーブキー処理。
        """
        window = self.active_window
        if window:
            if self.is_item_selected:
                    equip = _equips.get(window.cursor+1)
                    if _inventories.Items.has(equip.number-1):
                        if equip.number == _inventories.Equip.get(equip.type):
                            _sound.SE.play("cancel")
                            _inventories.Equip.set(equip.type, 0)
            if self.is_card_selected:
                equip = _collectible.get(window.cursor)
                number = _inventories.Deck.get(equip.number)-1
                _inventories.Deck.set(
                    equip.number, number if 0 < number else 0)
                if number != _inventories.Deck.get(equip.number)-1:
                    _sound.SE.play("cancel")
        return _const.IGNORE_STATUS

    def delete(self):
        u"""プレイヤーを変更。
        """
        return self.__player_chang(-1)

    def use(self):
        u"""プレイヤーを変更。
        """
        return self.__player_chang(1)

    # ---- Property ----
    @property
    def is_item_selected(self):
        u"""アイテムウィンドウを選択している場合に真。
        """
        return self._cursor == 0

    @property
    def is_skill_selected(self):
        u"""スキルウィンドウを選択している場合に真。
        """
        return self._cursor == 1

    @property
    def is_card_selected(self):
        u"""カードウィンドウを選択している場合に真。
        """
        return self._cursor == 2
