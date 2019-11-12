#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""battle.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

戦闘システムモジュール。
"""
import sprites.effects as _effects
import utils.const as _const
import utils.layouter as _layouter


class System(object):
    u"""戦闘システム。
    ユニット・魔術・召喚を管理。
    """
    __slots__ = (
        "__equip_info", "__group", "__hand", "__main", "__pile", "__player",
        "__reserved", "__spell_point")
    __HAND_LIMIT = 4
    __SPELL_LIMIT = 4
    __SPELL_COST = 4

    def __init__(self, main, level):
        u"""コンストラクタ。
        """
        import armament.units as __units
        import sprites.indicator as __indicator
        self.__main = main
        self.__hand = []
        number, _ = level.player
        blocks = self.__main.blocks
        self.__player = __units.Player(
            (0, 0), __units.get_player(number), blocks.field.packet)
        _layouter.Game.set_player(self.__player, blocks.window)
        self.__player.is_another = self.__main.id
        self.__player.is_right = not self.__main.id
        self.__player.set_equip(*level.equip)
        self.__equip_info = tuple(
            __indicator.Equip((0, 0), e) for e in self.__player.equip)
        _layouter.Game.set_equip(
            self.__equip_info, blocks.window, self.__main.id)
        self.__group = __units.Group(self.__main, self)
        self.__pile = None
        self.__reserved = None
        self.__spell_point = self.__SPELL_LIMIT

    def set_available(self):
        u"""カードに使用可・不可属性を設定。
        """
        for arcanum in self.__hand:
            arcanum.set_available()

    def draw(self, *anucana):
        u"""手札にカードを追加。
        anucana: アルカナ番号のタプル。
        """
        import armament.collectible as __collectible
        import arcanum as __arcanum

        def __is_all_joeker():
            u"""手札が全てジョーカーの場合に真。
            """
            return (
                self.__HAND_LIMIT <= len(self.__hand) and
                all(
                    arcanum.contents.type == _const.JOKER_TYPE for arcanum in
                    self.__hand))
        window = self.__main.blocks.window
        id_ = self.__main.id
        for arcanum in anucana:
            if not __is_all_joeker():
                _arcanum = __collectible.get(arcanum)
                self.__hand.append({
                    _const.SUMMON_TYPE: __arcanum.Summon,
                    _const.SORCERY_TYPE: __arcanum.Sorcery,
                    _const.SHIELD_TYPE: __arcanum.Shield,
                    _const.JOKER_TYPE: __arcanum.Joeker}[_arcanum.type](
                        self.__main, _arcanum))
                _layouter.Game.set_card(self.__hand, window, id_)
                if self.__HAND_LIMIT < len(self.__hand):
                    for arcanum in self.__hand:
                        if not arcanum.contents.type == _const.JOKER_TYPE:
                            self.__hand.remove(arcanum)
                            arcanum.burn()
                            _layouter.Game.set_card(
                                self.__hand, window, id_, True)
                            break
        self.set_available()

    def shuffle(self):
        u"""カード回転処理。
        """
        if (
            1 < len(self.__hand) and
            not any(arcanum.is_moving for arcanum in self.__hand)
        ):
            import material.sound as __sound
            __sound.SE.play("Shuffle")
            self.__hand.append(self.__hand.pop(0))
            _layouter.Game.set_card(
                self.__hand, self.__main.blocks.window, self.__main.id,
                True)

    def __spell_consumption(self):
        u"""呪文ポイントを消費。
        ※自分へのブロック変化効果でポイントはリセットされる。
        """
        self.__spell_point -= (
            self.__SPELL_COST >> 1 if self.__main.has_skill(
                _const.DOUBLE_SPELL_SKILL_NAME) else self.__SPELL_COST)

    def reserve(self, number):
        u"""カード予約処理。
        """
        if number < len(self.__hand):
            contents = self.__hand[number].contents
            is_summonable = contents.type == _const.SUMMON_TYPE and (
                not self.__group.is_full or self.__group.adapt(contents))
            cost_number, _ = self.__main.resorce.get_available(contents)
            is_useable = bool(cost_number) and (
                is_summonable or contents.type in (
                    _const.SORCERY_TYPE, _const.JOKER_TYPE))
            if 0 < self.__spell_point and is_useable:
                self.__main.resorce.consumption(contents)
                self.__reserved = contents
                self.__hand[number].burn()
                self.__hand.remove(self.__hand[number])
                self.__spell_consumption()
                self.set_available()
                _layouter.Game.set_card(
                    self.__hand, self.__main.blocks.window, self.__main.id,
                    True)
                return True
        return False

    def shred(self, number, is_force=False):
        u"""カード削除。
        number: 削除するカード番号。-1で全て削除。
        is_force: 真の場合、強制的に削除。
        """
        def __soul_eat(arcanum):
            u"""カード削除時にエレメンタルを取得する。
            """
            if (
                not arcanum.contents.type == _const.JOKER_TYPE and
                self.__main.has_skill(_const.SOUL_EAT_SKILL_NAME)
            ):
                self.__main.resorce.add_star(arcanum.contents.star, 1)
        result = ()
        if 0 < self.__spell_point or is_force:
            if number == -1:
                result += tuple(arcanum for arcanum in self.__hand)
                for arcanum in self.__hand:
                    arcanum.burn()
                self.__hand = []
                self.__spell_consumption()
                self.set_available()
                _layouter.Game.set_card(
                    self.__hand, self.__main.blocks.window, self.__main.id,
                    True)
            elif number < len(self.__hand) and (
                self.__hand[number].contents.type != _const.JOKER_TYPE or
                    self.__main.has_skill(_const.PURIFY_SKILL_NAME)):
                waste = self.__hand.pop(number)
                result += waste,
                waste.burn()
                __soul_eat(waste)
                self.__player.add_effect(_effects.Delete(
                    self.__player.rect.center, waste.contents))
                self.__spell_consumption()
                self.set_available()
                _layouter.Game.set_card(
                    self.__hand, self.__main.blocks.window, self.__main.id,
                    True)
        return tuple(
            arcanum.contents.number for arcanum in result if
            arcanum.contents.type != _const.JOKER_TYPE)

    def discard(self, all_=False):
        u"""魔術によるカード削除。
        """
        import random as __random
        if self.__hand:
            if all_:
                for arcanum in self.__hand[:]:
                    self.__hand.remove(arcanum)
                    arcanum.burn()
            else:
                waste = self.__hand.pop(
                    __random.randint(0, len(self.__hand) - 1))
                waste.burn()
                self.__player.add_effect(_effects.Delete(
                    self.__player.rect.center, waste.contents))
        _layouter.Game.set_card(
            self.__hand, self.__main.blocks.window, self.__main.id, True)

    def intercept(self, other, sorcery):
        u"""対戦相手魔術のシールド処理。
        other: 対戦相手のシステム。
        sorcery: 対戦相手の魔術。
        シールドに成功した場合、魔術効果を防いだかどうかの判定と、
        カウンターエフェクトを返す。
        """
        for arcanum in self.__hand:
            _arcanum = arcanum.contents
            if (
                _arcanum.type == _const.SHIELD_TYPE and
                sorcery.star == _arcanum.star
            ):
                has_reverse_magic = self.__main.has_skill(
                    _const.REVERSE_SORCERY_SKILL_NAME)
                self.__main.battle.player.add_effect(_effects.Spell(
                    self.__main.battle.player.rect.center, _arcanum,
                    has_reverse_magic))
                arcanum.burn()
                self.__hand.remove(arcanum)
                _layouter.Game.set_card(
                    self.__hand, self.__main.blocks.window, self.__main.id,
                    True)
                for effect in _arcanum.get_effects((
                    self.__main if has_reverse_magic else
                    other).battle.group
                ):
                    is_agrsv = (
                        not _arcanum.is_agrsv if has_reverse_magic else
                        _arcanum.is_agrsv)
                    effect.use(*(
                        (other, self.__main) if is_agrsv else
                        (self.__main, other)))
                return True
        return False

    def release(self, other):
        u"""予約したカードの使用・魔法反応処理。
        """
        is_delete = False
        reserved = self.__reserved
        if (
            reserved and other.is_throwing and
            not other.blocks.field.is_active
        ):
            has_reverse_magic = self.__main.has_skill(
                _const.REVERSE_SORCERY_SKILL_NAME)
            is_summon = reserved.type == _const.SUMMON_TYPE
            if is_summon:
                if (
                    other.has_skill(_const.ANTI_SUMMONING_SKILL_NAME) and
                    other.battle.intercept(self.__main, reserved)
                ):
                    is_delete = True
                else:
                    packet = self.__main.blocks.field.packet
                    fusioned = self.__group.adapt(reserved)
                    if fusioned:
                        self.__group.fusion(reserved, packet)
                        reserved = fusioned
                    else:
                        self.__group.summon(reserved, packet)
            else:
                if other.battle.intercept(self.__main, reserved):
                    is_delete = True
                else:
                    if self.__pile:
                        piled = reserved.adapt(self.__pile)
                        if piled:
                            reserved = piled
                    for effect in reserved.get_effects((
                        self.__main if has_reverse_magic else
                        other).battle.group
                    ):
                        is_agrsv = (
                            not reserved.is_agrsv if has_reverse_magic else
                            reserved.is_agrsv)
                        effect.use(*(
                            (other, self.__main) if is_agrsv else
                            (self.__main, other)))
                    self.__pile = (
                        reserved if reserved.type == _const.SORCERY_TYPE else
                        None)
            center = self.__player.rect.center
            if is_delete:
                self.__player.add_effect(
                    _effects.Delete(center, reserved))
            else:
                self.__player.add_effect(_effects.Spell(
                    center, reserved, not is_summon and has_reverse_magic))
            self.__reserved = None
            self.set_available()

    def turn(self, game_over=False):
        u"""ターン毎の処理。
        """
        self.__spell_point = self.__SPELL_LIMIT
        self.draw(*self.__main.resorce.get_cards())
        self.__player.count_down()
        self.__group.turn(game_over)
        self.set_available()

    @property
    def is_sorcery_usable(self):
        u"""魔術・カード削除使用可能な場合に真。
        """
        return not self.__reserved and 0 < self.__spell_point

    @property
    def hand(self):
        u"""手札取得。
        """
        return tuple(self.__hand)

    @property
    def hand_by_number(self):
        u"""番号による手札取得。
        """
        return tuple(arcanum.contents.number for arcanum in self.__hand)

    @property
    def pile(self):
        u"""現在パイル魔術取得。
        """
        return self.__pile

    @property
    def player(self):
        u"""プレイヤー取得。
        """
        return self.__player

    @property
    def equip_info(self):
        u"""装備情報スプライト取得。
        """
        return self.__equip_info

    @property
    def group(self):
        u"""クリーチャーグループを取得。
        """
        return self.__group
