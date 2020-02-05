#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""system.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

システムモジュール。
"""
import phase as _phase
import utils.const as _const
import utils.general as _general


class System(object):
    u"""メインシステム。
    """
    __slots__ = (
        "__accumulate", "__base_skills", "__battle", "__cmds", "__game_over",
        "__id", "__is_pause_available", "__is_paused", "__is_playing",
        "__is_transparent", "__phase", "__pressure", "__puzzle", "__resource",
        "__thinker", "__turn")
    __IS_TEST = False
    __TURN_OVER = 0b11111111

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
            import resource as __resource
            import utils.layouter as __layouter
            self.__is_playing = True
            self.__is_pause_available = True
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
            self.__resource = __resource.Resource(level.deck)
            __layouter.Game.set_stars(
                (__huds.Star(self.__resource, i) for i in range(7)), self.__id)

        def __set_puzzle():
            u"""パズルシステム設定。
            """
            import puzzle as __puzzle
            self.__puzzle = __puzzle.System(self, parent, level)
            self.__puzzle.forward(4 if self.__id == 0 else 3, False)
            self.__puzzle.update()

        def __set_battle():
            u"""戦闘システム設定。
            """
            import battle as __battle
            self.__battle = __battle.System(self, level)
            __huds.Pressure(self.__battle.player, self)
            if self.has_skill(_const.FORCE_JOKER_SKILL):
                self.__battle.hand.draw(*__collectible.Collectible.get_by_name(
                    u"リバースサモン", u"リバースソーサリー"))
            self.__battle.turn()

        def __set_test():
            u"""テスト用設定。
            """
            if self.__IS_TEST:
                if self.__id == 0:
                    for i in range(_const.NUMBER_OF_STAR):
                        self.__resource.increase(i, 0)
                    self.__battle.hand.draw(
                        *__collectible.Collectible.get_by_name())
                else:
                    for i in range(_const.NUMBER_OF_STAR):
                        self.__resource.increase(i, 0)
                    self.__battle.hand.draw(
                        *__collectible.Collectible.get_by_name())
        __set_parameter()
        __set_puzzle()
        __set_battle()
        __set_test()
        self.set_boot()

    # ---- Phase ----
    def complete(self, rival):
        u"""ラインコンプリート処理。
        """
        self.__phase.sub_complete(rival, self.__thinker)
        self.__phase.complete()

    def release(self, rival):
        u"""アルカナ開放処理。
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

    # ------ Command ------
    def input_command(self, cmd):
        u"""コマンド入力。
        """
        self.__phase.input_command(cmd)

    def run_command(self, rival):
        u"""コマンドの処理全般。
        """
        while self.__cmds:
            self.__phase.run_command(self.__cmds[0], rival)
            self.__cmds = self.__cmds[1:]

    # ---- Process ----
    def damage_calc(self, rival, damage, effects):
        u"""ダメージ計算。
        """
        def __vampire():
            u"""スター吸収スキル処理。
            """
            import random as __random
            targets = tuple(j for j, is_exsit in enumerate(
                _const.STAR_ENERGY <= i for i in self.resource.stars
            ) if is_exsit)
            if (
                targets and rival.flash(_const.VAMPIRE_SKILL) and
                not self.flash(_const.TALISMAN_SKILL)
            ):
                target = __random.choice(targets)
                self.resource.decrease(target, _const.STAR_ENERGY)
                rival.resource.increase(target, _const.STAR_ENERGY)

        def __rob_card():
            u"""カード強奪スキル処理。
            """
            if (
                self.__battle.hand and rival.flash(_const.ROB_CARD_SKILL) and
                not self.flash(_const.SAFETY_SKILL)
            ):
                for i, card in enumerate(self.__battle.hand):
                    if card.arcanum.type != _const.JOKER_ARCANUM:
                        rival.battle.hand.draw(
                            *self.__battle.discard(i, is_force=True))
                        return None
        player = self.__battle.player
        group = self.__battle.group
        pressure = player.defense(group.receive(damage))
        group.destroy(resource=rival.resource, detect=self.flash)
        if pressure:
            player.flash("damage")
            self.__accumulate.add_pressure(pressure)
            for effect in effects:
                if effect:
                    new, _, _ = effect
                    if self.__battle.player.armor.is_prevention(new):
                        _, _, armor, _ = self.__battle.equip_huds
                        armor.flash()
                    elif not self.__battle.group.is_prevention(new):
                        self.__accumulate.add_effect(effect)
            __vampire()
            __rob_card()
            self.update()

    def forward(self):
        u"""ターンを進める。
        """
        self.__turn = self.__turn+1 & self.__TURN_OVER

    # ---- Skill ----
    def has_skill(self, skill):
        u"""スキル判定。
        """
        name = _general.get_skill_names(skill)
        return name in self.__skills.split("#")

    def flash(self, skill):
        u"""スキル所持対象を光らせる。
        """
        name = _general.get_skill_names(skill)
        if name in self.__base_skills.split("#"):
            self.__battle.player.flash("skill")
            return True
        return self.__battle.flash(skill)

    # ---- Update ----
    def update(self):
        u"""カード表示とスキル設定。
        """
        self.__puzzle.field.skills = self.__resource.skills = self.__skills
        self.__battle.hand.update()

    # ---- Getter ----
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
                parameter.donors = self.__battle.group.donors
                parameter.catalyst = (
                    self.__battle.catalyst.number if
                    self.__battle.catalyst else -1)
                parameter.resource = self.__resource.copy
                parameter.is_arcana_available = (
                    self.__battle.is_arcana_available)

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
                1 << i if not item.is_available else 0 for
                i, item in enumerate(self.__battle.player.equip))
            parameter.hand = self.__battle.hand.by_number
            parameter.jokers = len(self.__battle.hand.jokers)
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
            self.__base_skills, self.__battle.skills) if skills)
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
    def resource(self):
        u"""リソース取得。
        """
        return self.__resource

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
        is_short_trun = self.has_skill(_const.SHORT_TURN_SKILL)
        return self.__turn << 1 if is_short_trun else self.__turn

    # ------ Detection ------
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
    def is_pause_available(self):
        u"""一時停止可能状態取得。
        """
        return self.__is_pause_available

    @is_pause_available.setter
    def is_pause_available(self, value):
        u"""一時停止可能状態設定。
        """
        self.__is_pause_available = bool(value)

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
