#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""system.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

システムモジュール。
"""
import utils.const as _const
import phase as _phase


class System(object):
    u"""メインシステム。
    """
    __slots__ = (
        "__accumulate", "__base_skills", "__battle", "__cmds", "__game_over",
        "__id", "__is_pauseable", "__is_paused", "__is_playing",
        "__is_transparent", "__phase", "__pressure", "__puzzle", "__resorce",
        "__thinker", "__turn")
    __ROUND = 0b11111111

    def __init__(self, level, parent, id_):
        u"""システム初期化。
        召喚・魔法などのサブシステムもここで設定する。
        """
        import armament.collectible as __collectible
        import sprites.huds as __huds

        def __set_parameter():
            u"""パラメータ設定
            """
            import accumulate as __accumulate
            import armament.skill as __skill
            import resorce as __resorce
            import utils.layouter as __layouter
            self.__is_playing = True
            self.__is_pauseable = True
            self.__is_paused = False
            self.__id = int(id_)
            self.__turn = 0
            self.__game_over = 0
            self.__cmds = ""
            self.__base_skills = reduce(lambda x, y: x+"#"+y, (
                __skill.get(i).name for i in level.skill
            )) if level.skill else ""
            self.__thinker = None
            self.__accumulate = __accumulate.Accumulate()
            self.__resorce = __resorce.Resorce(level.deck)
            __layouter.Game.set_stars(
                (__huds.Star(self.__resorce, i) for i in range(7)), self.__id)

        def __set_puzzle():
            u"""パズルシステム設定。
            """
            import puzzle as __puzzle
            self.__puzzle = __puzzle.System(self, parent, level)
            self.__puzzle.forward(4 if self.__id == 0 else 3, False)
            self.__puzzle.update_window()

        def __set_battle():
            u"""戦闘システム設定。
            """
            import battle as __battle
            self.__battle = __battle.System(self, level)
            __huds.Pressure(self.__battle.player, self)
            name, _ = _const.FORCE_JOKER_SKILL.split("#")
            if self.has_skill(name):
                self.__battle.draw(*__collectible.Collectible.get_by_name(
                    u"リバースサモン", u"リバースソーサリー"))

        def __set_test():
            u"""テスト用設定。
            """
            if _const.IS_SYSTEM_TEST:
                if self.__id == 0:
                    for i in range(7):
                        self.__resorce.inc_and_dec(i, 16)
                    self.__battle.draw(*__collectible.Collectible.get_by_name(
                        u"オールデリート", u"オールデリート",
                        u"オールデリート", u"オールデリート"))
                else:
                    for i in range(7):
                        self.__resorce.inc_and_dec(i, 16)
                    self.__battle.draw(*__collectible.Collectible.get_by_name(
                        u"アンロック", u"アンロック",
                        u"アンロック", u"リバースソーサリー"))
        __set_parameter()
        __set_puzzle()
        __set_battle()
        __set_test()
        self.set_boot()

    def get_parameter(self, is_ai):
        u"""AI用パラメータ取得。
        """
        import input.ai.parameter as __parameter

        def __set_search():
            u"""コマンド探索用パラメータ設定。
            """
            if is_ai:
                parameter.piece = self.__puzzle.piece.parameter
                parameter.piece_pos = self.__puzzle.piece.topleft
                hold = self.__puzzle.hold.virtual
                parameter.hold = hold.parameter if hold else None
                parameter.is_hold_captured = self.__puzzle.hold.is_captured
                parameter.recepters = self.__battle.group.recepters
                parameter.catalyst = (
                    self.__battle.catalyst.number if
                    self.__battle.catalyst else -1)
                parameter.resorce = self.__resorce
                parameter.is_sorcery_useable = self.__battle.is_sorcery_useable

        def __set_peice():
            u"""ピース関連パラメータ設定。
            """
            field = self.__puzzle.field
            parameter.field = field.parameter
            parameter.field_one_eighth = field.one_eighth
            parameter.has_alone_chest = field.table.has_alone_chest
            parameter.hold_item_state = self.__puzzle.hold.item_state

        def __set_battle():
            u"""戦闘関連パラメータ設定。
            """
            parameter.equip_broken_state = sum(
                1 << i if not item.is_useable else 0 for
                i, item in enumerate(self.__battle.player.equip))
            parameter.hand = self.__battle.hand_by_number
            parameter.jokers = len(self.__battle.jokers)
            group = self.__battle.group
            parameter.is_full_group = group.is_full
            parameter.is_group_exsit = bool(group)
            parameter.has_health = bool(group.healths)
            parameter.has_normal = bool(group.get_livings(group.healths))
            parameter.has_damaged = bool(group.get_livings(group.damaged))
        parameter = __parameter.Parameter()
        parameter.skills = self.__skills
        __set_search()
        __set_peice()
        __set_battle()
        return parameter

    # ---- Command ----
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

    # ---- Process ----
    def damage_calc(self, rival, damage, effects):
        u"""ダメージ計算。
        """
        def __vampire():
            u"""スター吸収スキル処理。
            """
            import random as __random
            vampire, _ = _const.VAMPIRE_SKILL.split("#")
            talisman, _ = _const.TALISMAN_SKILL.split("#")
            if rival.has_skill(vampire) and not self.has_skill(talisman):
                targets = tuple(j for j, is_exsit in enumerate(
                    _const.STAR_ENERGY <= i for i in self.__resorce.stars
                ) if is_exsit)
                if targets:
                    target = __random.choice(targets)
                    self_stars = list(self.__resorce.stars)
                    self_stars[target] -= _const.STAR_ENERGY
                    self.__resorce.stars = self_stars
                    rival_stars = list(rival.__resorce.stars)
                    rival_stars[target] += _const.STAR_ENERGY
                    rival.__resorce.stars = rival_stars

        def __rob_card():
            u"""カード強奪スキル処理。
            """
            name, _ = _const.ROB_CARD_SKILL.split("#")
            if rival.has_skill(name):
                for i, card in enumerate(self.__battle.hand):
                    if card.arcanum.type != _const.JOKER_ARCANUM:
                        rival.__battle.draw(
                            *self.__battle.dump(i, is_force=True))
                        return None
        player = self.__battle.player
        group = self.__battle.group
        pressure = player.defense(group.receive(damage))
        group.destroy()
        if pressure:
            player.flash("damage")
            self.__accumulate.add_pressure(pressure)
            for effect in effects:
                if effect:
                    new, _, _ = effect
                    if self.__battle.player.armor.is_prevention(new):
                        _, _, armor, _ = self.__battle.equip
                        armor.flash()
                    elif not self.__battle.group.is_prevention(new):
                        self.__accumulate.add_effect(effect)
            __vampire()
            __rob_card()
            self.__battle.update()

    def forward(self):
        u"""ターンを進める。
        """
        self.__turn = self.__turn+1 & self.__ROUND

    # ---- Phase ----
    def completion(self, rival):
        u"""ラインコンプリート処理。
        """
        self.__phase.sub_completion(rival, self.__thinker)
        self.__phase.completion()

    def release(self, rival):
        u"""魔術開放処理。
        """
        self.__phase.release(rival)

    def throw(self, rival):
        u"""ブロック投下処理。
        """
        self.__phase.throw(rival, self.__thinker)

    def fall(self):
        u"""ブロック自動落下処理。
        """
        self.__phase.fall()

    # ---- Skill ----
    def has_skill(self, name):
        u"""指定されたスキル所持数を返す。
        """
        skills = self.__skills.split("#")
        return skills.count(name)

    def update_skills(self):
        u"""スキル更新処理。
        """
        self.__puzzle.field.skills = self.__resorce.skills = self.__skills

    # ---- Setter ----
    def set_thinker(self, rival):
        u"""AI設定。
        """
        import input.ai as __ai
        self.__thinker = __ai.Thinker((self, rival))

    def set_boot(self):
        u"""起動フェイズ設定。
        """
        self.__phase = _phase.BootPhase(self)

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

    def set_win(self):
        u"""勝利設定。
        """
        self.__game_over = 1

    def set_lose(self):
        u"""敗北設定。
        """
        self.__game_over = -1

    # ---- Property ----
    @property
    def __skills(self):
        u"""スキル文字列取得。
        return: 'skill1#skill2#skill3...'
        """
        skills = tuple(skills for skills in (
            self.__base_skills, self.__battle.card_skills,
            self.__battle.creature_skills) if skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""

    # ------ System ------
    @property
    def id(self):
        u"""ID取得。
        """
        return self.__id

    @property
    def thinker(self):
        u"""AI取得。
        """
        return self.__thinker

    @property
    def battle(self):
        u"""戦闘システム取得。
        """
        return self.__battle

    @property
    def puzzle(self):
        u"""パズルシステム取得。
        """
        return self.__puzzle

    @property
    def resorce(self):
        u"""リソース取得。
        """
        return self.__resorce

    @property
    def accumulate(self):
        u"""蓄積ダメージ取得。
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
    def turn(self):
        u"""ターン取得。
        """
        name, _ = _const.SHORT_TURN_SKILL.split("#")
        return self.__turn << 1 if self.has_skill(name) else self.__turn

    # ------ Detect ------
    @property
    def is_throwing(self):
        u"""通常フェイズ判定。
        """
        return isinstance(self.__phase, _phase.ThrowingPhase)

    @property
    def is_game_over(self):
        u"""ゲームオーバー状態取得。
        """
        return bool(self.__game_over)

    @property
    def is_win(self):
        u"""勝利判定。
        """
        return self.__game_over == 1

    @property
    def is_lose(self):
        u"""敗北判定。
        """
        return self.__game_over == -1

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
