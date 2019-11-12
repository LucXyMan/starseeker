#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""main.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

メインゲームシステムモジュール。
"""
import utils.const as _const
import phase as _phase


class System(object):
    u"""メインゲームシステム。
    """
    __slots__ = (
        "__accumulate", "__battle", "__blocks", "__cmds", "__game_over",
        "__id", "__is_pauseable", "__is_paused", "__is_playing",
        "__is_transparent", "__phase", "__pressure", "__resorce", "__skills",
        "__thinker", "__turn")
    __ROUND = 0b11111111
    __IS_TEST = False

    def __init__(self, level, parent, id_):
        u"""システム初期化。
        召喚・魔法などのサブシステムもここで設定する。
        """
        import accumulate as __accumulate
        import armament.collectible as __collectible
        import armament.skill as __skill
        import battle as __battle
        import blocks as __blocks
        import resorce as __resorce
        import sprites.indicator as __indicator
        import utils.layouter as __layouter
        self.__id = id_
        self.__thinker = None
        self.__turn = 0
        self.__game_over = 0
        self.__is_playing = True
        self.__is_pauseable = True
        self.__is_paused = False
        self.__cmds = ""
        self.__skills = reduce(
            lambda x, y: x+"#"+y, (skill.name for skill in (
                __skill.get(i) for i in level.skill))) if level.skill else ""
        self.__blocks = __blocks.System(self, parent, level)
        self.__blocks.advance(4 if self.__id == 0 else 3, False)
        self.__accumulate = __accumulate.Accumulate()
        self.__battle = __battle.System(self, level)
        self.__resorce = __resorce.Resorce(self.__skills)
        if self.has_skill(_const.DARK_FORCE_SKILL_NAME):
            self.__resorce.add_star(5, 4)
            self.__battle.draw(
                *__collectible.Collectible.get_by_name(u"ブラックドラゴン"))
        if self.__IS_TEST:
            for i in range(7):
                self.__resorce.add_star(i, 1)
            if self.__id == 0:
                self.__battle.draw(*__collectible.Collectible.get_by_name(
                    u"ゴーストキャット", u"ゴーストキャット", u"フェアリーシード", u"ソーダスライム"))
            else:
                self.__battle.draw(*__collectible.Collectible.get_by_name(
                    u"フリーズジェル", ))
        __layouter.Game.set_stars(tuple(
            __indicator.Star(self, n) for n in range(7)), self.__id)
        __indicator.Pressure(self.__battle.player, self)
        self.__blocks.update_display()
        self.set_boot()

    def command_input(self, cmd):
        u"""コマンド入力。
        """
        self.__phase.command_input(cmd)

    def command_run(self, rival):
        u"""コマンドの処理全般。
        """
        while self.__cmds:
            self.__phase.command_run(self.__cmds[0], rival)
            self.__cmds = self.__cmds[1:]

    def completion(self, rival):
        u"""ラインコンプリート処理。
        """
        self.__phase.sub_completion(rival, self.__thinker)
        self.__phase.completion()

    def damage_calc(self, rival, damage, effects):
        u"""ダメージ計算。
        """
        def __vampire(rival):
            u"""スター吸収スキル処理。
            """
            import random as __random
            if rival.has_skill(_const.VAMPIRE_SKILL_NAME):
                targets = tuple(j for j, is_charged in enumerate(
                    _const.STAR_ENERGY <= i for i in self.__resorce.stars) if
                    is_charged)
                if targets:
                    target = __random.choice(targets)
                    self_stars = self.__resorce.stars
                    self_stars[target] -= _const.STAR_ENERGY
                    self.__resorce.stars = self_stars
                    rival_stars = rival.__resorce.stars
                    rival_stars[target] += _const.STAR_ENERGY
                    rival.__resorce.stars = rival_stars

        def __rob_card(rival):
            u"""カード強奪スキル処理。
            """
            if rival.has_skill(_const.ROB_CARD_SKILL_NAME):
                for i, arcanum in enumerate(self.__battle.hand):
                    if arcanum.contents.type != _const.JOKER_TYPE:
                        rival.__battle.draw(*self.__battle.shred(
                            i, is_force=True))
                        break
        player = self.__battle.player
        group = self.__battle.group
        pressure = player.defense(group.receive(damage))
        group.destroy()
        if pressure:
            player.flash("Damage")
            self.__accumulate.add_pressure(pressure)
            for effect in effects:
                if effect:
                    battle = self.__battle
                    new, _, _ = effect
                    if battle.player.armor.is_prevents(new):
                        _, _, armor_info, _ = battle.equip_info
                        armor_info.flash()
                    elif not battle.group.is_prevents(new):
                        self.__accumulate.add_effect(effect)
            __vampire(rival)
            __rob_card(rival)
            self.__battle.set_available()

    def release(self, rival):
        u"""魔術開放処理。
        """
        self.__phase.release(rival)

    def throw(self, rival):
        u"""ブロック投下処理。
        """
        self.__phase.throw(rival, self.__thinker)

    def fall(self):
        u"""ブロックの自動落下処理。
        """
        self.__phase.fall()

    def has_skill(self, name):
        u"""指定されたスキルを所持している場合に真。
        """
        return name in self.__skills.split("#")

    def has_equip(self, names):
        u"""指定された装備をしている場合に真。
        """
        return all(
            name for name in names.split("#") if
            name in (equip.name for equip in self.__player.equip))

    def get_parameter(self, is_myself=False):
        u"""AI用パラメータ取得。
        """
        import input.ai.parameter as __parameter
        parameter = __parameter.Parameter()
        if is_myself:
            parameter.skills = self.__skills
            parameter.piece = self.__blocks.piece.parameter
            parameter.piece_pos = self.__blocks.piece.topleft
            hold = self.__blocks.hold.virtual
            parameter.hold = hold.parameter if hold else None
            parameter.is_hold_captured = self.__blocks.hold.is_captured
            parameter.hand = self.__battle.hand_by_number
            parameter.has_locked_chest = self.__blocks.field.has_locked_chest
            parameter.recepters = self.__battle.group.recepters
            parameter.pile = (
                self.__battle.pile.number if self.__battle.pile else -1)
            parameter.resorce = self.__resorce
            parameter.is_sorcery_usable = self.__battle.is_sorcery_usable
        parameter.equip_broken_state = sum(
            (1 << i if not item.is_useable else 0) for
            i, item in enumerate(self.__battle.player.equip))
        parameter.hold_item_state = self.__blocks.hold.item_state
        parameter.field = self.__blocks.field.parameter
        parameter.field_one_eighth = self.__blocks.field.one_eighth
        group = self.__battle.group
        parameter.is_full_group = group.is_full
        parameter.is_group_exsit = bool(group)
        parameter.has_health = bool(group.healths)
        parameter.has_normal = bool(group.get_livings(group.healths))
        parameter.has_damaged = bool(group.get_livings(group.damaged))
        return parameter

    @property
    def battle(self):
        u"""戦闘システム取得。
        """
        return self.__battle

    @property
    def blocks(self):
        u"""ブロックシステム取得。
        """
        return self.__blocks

    @property
    def resorce(self):
        u"""リソース取得。
        """
        return self.__resorce

    @property
    def skills(self):
        u"""スキル取得。
        """
        return self.__skills

    @property
    def turn(self):
        u"""ターンを進めて値を取得。
        """
        self.__turn = (self.__turn+1) & self.__ROUND
        return self.__turn

    @property
    def accumulate(self):
        u"""蓄積ダメージ管理オブジェクト取得。
        """
        return self.__accumulate

    @property
    def cmds(self):
        u"""コマンド取得。
        """
        return self.__cmds

    @cmds.setter
    def cmds(self, value):
        u"""コマンド設定。
        """
        self.__cmds = str(value)

    @property
    def drop_pos(self):
        u"""ピースの落下地点を取得。
        """
        return self.__blocks.drop_pos

    @property
    def id(self):
        u"""IDを取得。
        """
        return self.__id

    @property
    def thinker(self):
        u"""使用AIの取得。
        """
        return self.__thinker

    def set_thinker(self, rival):
        u"""使用AIの設定。
        """
        import input.thinker as __thinker
        self.__thinker = __thinker.Thinker(self, rival)

    def set_boot(self):
        u"""起動フェイズ設定。
        """
        self.__phase = _phase.BootPhase(self)

    @property
    def is_throwing(self):
        u"""通常フェイズの場合True。
        """
        return isinstance(self.__phase, _phase.ThrowingPhase)

    def set_throwing(self):
        u"""通常フェイズ設定。
        """
        self.__phase = _phase.ThrowingPhase(self)

    def set_thrown(self):
        u"""投下後フェイズ設定。
        """
        self.__phase = _phase.ThrownPhase(self)

    def set_complete(self):
        u"""ライン補完フェイズ設定。
        """
        self.__phase = _phase.CompletePhase(self)

    @property
    def is_game_over(self):
        u"""ゲームオーバー状態取得。
        """
        return bool(self.__game_over)

    @property
    def is_win(self):
        u"""勝利時に真。
        """
        return self.__game_over == 1

    def set_win(self):
        u"""勝利状態設定。
        """
        self.__game_over = 1

    @property
    def is_lose(self):
        u"""敗北時に真。
        """
        return self.__game_over == -1

    def set_lose(self):
        u"""敗北状態設定。
        """
        self.__game_over = -1

    @property
    def is_pauseable(self):
        u"""一時停止可能状態取得。
        """
        return self.__is_pauseable

    @is_pauseable.setter
    def is_pauseable(self, value):
        u"""一時停止可能状態設定。
        """
        self.__is_pauseable = bool(value)

    @property
    def is_paused(self):
        u"""一時停止状態取得。
        """
        return self.__is_paused

    @is_paused.setter
    def is_paused(self, value):
        u"""一時停止状態設定。
        """
        self.__is_paused = bool(value)
