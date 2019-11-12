#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""system.py

Copyright (c) 2019 Yukio Kuro
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
        "__catalyst", "__core", "__equip", "__group", "__hand",
        "__player", "__reserved", "__spell_point")
    __SPELL_COST = 2

    def __init__(self, core, level):
        u"""コンストラクタ。
        """
        import armament.units as __units
        import sprites.huds as __huds
        self.__spell_point = self.__SPELL_COST
        self.__core = core
        self.__hand = []
        number, _ = level.player
        puzzle = self.__core.puzzle
        self.__player = __units.Player(
            (0, 0), __units.get_player(number), puzzle.field.packet)
        _layouter.Game.set_player(self.__player, puzzle.window)
        self.__player.is_another = self.__core.id
        self.__player.is_right = not self.__core.id
        self.__player.set_equip(*level.equip)
        self.__equip = tuple(
            __huds.Equip((0, 0), item) for item in self.__player.equip)
        _layouter.Game.set_equip(self.__core, self.__equip)
        self.__group = __units.Group(self.__core, self.__player)
        self.__catalyst = None
        self.__reserved = None

    def update(self):
        u"""カード表示と使用可能スキル更新。
        """
        self.__core.update_skills()
        for card in self.__hand:
            card.set_available()

    def turn(self, is_game_over=False):
        u"""ターン毎の処理。
        """
        self.__spell_point = self.__SPELL_COST
        self.draw(*self.__core.resorce.draw())
        self.__player.count_down()
        self.__group.turn(is_game_over)
        self.update()

    # ---- Hand ----
    def __remove_skill_card(self, name):
        u"""指定したスキルカード削除。
        """
        for i, card in enumerate(self.__hand):
            if name in card.arcanum.skills.split("#"):
                self.destroy(i)
                return None

    def draw(self, *numbers):
        u"""手札にカードを追加。
        anucana: アルカナ番号のタプル。
        """
        import armament.collectible as __collectible
        import card as __card
        for number in numbers:
            if len(self.jokers) < _const.NUMBER_OF_HAND:
                arcanum = __collectible.get(number)
                cards = {
                    _const.SUMMON_ARCANUM: __card.Summon,
                    _const.SORCERY_ARCANUM: __card.Sorcery,
                    _const.SHIELD_ARCANUM: __card.Shield,
                    _const.SUPPORT_ARCANUM: __card.Support,
                    _const.JOKER_ARCANUM: __card.Joker}
                Card = cards[arcanum.type]
                self.__hand.append(Card(self.__core, arcanum))
                _layouter.Game.set_hand(self.__core)
                if _const.NUMBER_OF_HAND < len(self.__hand):
                    for card in self.__hand:
                        if not card.arcanum.type == _const.JOKER_ARCANUM:
                            self.__hand.remove(card)
                            card.burn()
                            _layouter.Game.set_hand(self.__core, True)
                            break
        self.update()

    def dump(self, number, is_force=False):
        u"""カードを捨てる。
        number: 捨てるカード番号。
        is_force: 真の場合に強制削除。
        """
        def __soul_eat():
            u"""サモンカード削除時にエレメンタルを取得する。
            """
            name, _ = _const.SOUL_EAT_SKILL.split("#")
            if (
                not is_force and self.__core.has_skill(name) and
                waste.arcanum.type == _const.SUMMON_ARCANUM
            ):
                self.__core.resorce.inc_and_dec(waste.arcanum.star, 1)
                self.__remove_skill_card(name)
        if number < len(self.__hand):
            name, _ = _const.PURIFY_SKILL.split("#")
            has_purify = self.__core.has_skill(name)
            is_joker = self.__hand[number].arcanum.type == _const.JOKER_ARCANUM
            if (
                (0 < self.__spell_point or is_force) and
                (not is_joker or has_purify)
            ):
                waste = self.__hand.pop(number)
                waste.burn()
                if is_joker and has_purify:
                    self.__remove_skill_card(name)
                __soul_eat()
                self.__player.add_effect(_effects.Shred(
                    self.__player.rect.center, waste.arcanum))
                if not is_force:
                    self.__spell_consume()
                    self.update()
                _layouter.Game.set_hand(self.__core, True)
                if waste.arcanum.type != _const.JOKER_ARCANUM:
                    return waste.arcanum.number,
        return ()

    def destroy(self, number=-1):
        u"""カード破壊。
        """
        deleted = 0
        if self.__hand:
            if number == -1:
                deleted = len(self.__hand)
                for card in self.__hand[:]:
                    self.__hand.remove(card)
                    card.burn()
            else:
                deleted = 1
                card = self.__hand[number]
                self.__hand.remove(card)
                card.burn()
                _layouter.Game.set_hand(self.__core, True)
            self.__core.update_skills()
        return deleted

    def shuffle(self):
        u"""カード回転処理。
        """
        if (
            1 < len(self.__hand) and
            all(not arcanum.is_moving for arcanum in self.__hand)
        ):
            import material.sound as __sound
            __sound.SE.play("shuffle")
            self.__hand = self.__hand[1:]+self.__hand[:1]
            _layouter.Game.set_hand(self.__core, True)

    # ---- Arcana ----
    def __spell_consume(self):
        u"""呪文ポイントを消費。
        ※自分へのブロック変化効果でポイントはリセットされる。
        """
        name, _ = _const.DOUBLE_SPELL_SKILL.split("#")
        self.__spell_point -= (
            self.__SPELL_COST >> 1 if self.__core.has_skill(name) else
            self.__SPELL_COST)

    def __intercept(self, other, sorcery):
        u"""シールド処理。
        other: 対戦相手のシステム。
        sorcery: 対戦相手の魔術。
        シールドに成功した場合、魔術効果を防いだかどうかの判定と、
        カウンターエフェクトを返す。
        """
        for card in self.__hand:
            if (
                card.arcanum.type == _const.SHIELD_ARCANUM and
                sorcery.star == card.arcanum.star
            ):
                self.__player.add_effect(_effects.Spell(
                    self.__player.rect.center, card.arcanum))
                card.burn()
                self.__hand.remove(card)
                _layouter.Game.set_hand(self.__core, True)
                card.arcanum.use((
                    (other, self.__core) if card.arcanum.is_agrsv else
                    (self.__core, other)), other.battle.group)
                return True
        return False

    def reserve(self, number):
        u"""アルカナ予約処理。
        """
        if number < len(self.__hand):
            arcanum = self.__hand[number].arcanum
            is_summonable = arcanum.type == _const.SUMMON_ARCANUM and (
                not self.__group.is_full or self.__group.adapt(arcanum))
            cost_number, _ = self.__core.resorce.get_available(arcanum)
            is_useable = bool(cost_number) and (
                is_summonable or arcanum.type in (
                    _const.SORCERY_ARCANUM, _const.JOKER_ARCANUM))
            if 0 < self.__spell_point and is_useable:
                self.__core.resorce.consumption(arcanum)
                self.__reserved = arcanum
                self.__hand[number].burn()
                self.__hand.remove(self.__hand[number])
                self.__spell_consume()
                self.update()
                _layouter.Game.set_hand(self.__core, True)
                return True
        return False

    def release(self, other):
        u"""予約したカードの使用処理。
        """
        def __release_summon(summon):
            u"""サモンカード処理。
            """
            name, _ = _const.ANTI_SUMMONING_SKILL.split("#")
            if (
                other.has_skill(name) and
                other.battle.__intercept(self.__core, summon)
            ):
                other.battle.__remove_skill_card(name)
                return summon, True
            else:
                fusioned = self.__group.adapt(summon)
                if fusioned:
                    self.__group.fusion(summon)
                    return fusioned, False
                else:
                    self.__group.summon(summon)
                    name, _ = _const.POISON_SUMMON_SKILL.split("#")
                    if self.__core.has_skill(name):
                        self.__group[-1].poisoning()
                    return summon, False

        def __release_sorcery(sorcery):
            u"""ソーサリーカード処理。
            """
            name, _ = _const.REVERSE_SORCERY_SKILL.split("#")
            has_reverse_sorcery = self.__core.has_skill(name)
            self.__remove_skill_card(name)
            if other.battle.__intercept(self.__core, sorcery):
                return sorcery, True, has_reverse_sorcery
            else:
                if self.__catalyst:
                    altered = sorcery.adapt(self.__catalyst)
                    if altered:
                        sorcery = altered
                is_agrsv = (
                    not sorcery.is_agrsv if has_reverse_sorcery else
                    sorcery.is_agrsv)
                sorcery.use(
                    (other, self.__core) if is_agrsv else
                    (self.__core, other), (
                        self.__core if has_reverse_sorcery else other
                    ).battle.group)
                self.__catalyst = (
                    sorcery if sorcery.type == _const.SORCERY_ARCANUM else
                    None)
                return sorcery, False, has_reverse_sorcery
        is_delete = False
        arcanum = self.__reserved
        if (
            arcanum and other.is_throwing and
            not other.puzzle.field.is_active
        ):
            is_summon = arcanum.type == _const.SUMMON_ARCANUM
            if is_summon:
                arcanum, is_delete = __release_summon(arcanum)
            else:
                arcanum, is_delete, has_reverse_sorcery = (
                    __release_sorcery(arcanum))
            center = self.__player.rect.center
            if is_delete:
                self.__player.add_effect(_effects.Shred(center, arcanum))
            else:
                self.__player.add_effect(_effects.Spell(
                    center, arcanum, not is_summon and has_reverse_sorcery))
            self.__reserved = None
            self.update()

    # ---- Property ----
    @property
    def catalyst(self):
        u"""触媒魔術取得。
        """
        return self.__catalyst

    @property
    def is_sorcery_useable(self):
        u"""魔術・カード削除使用可能な場合に真。
        """
        return not self.__reserved and 0 < self.__spell_point

    # ------ Hand ------
    @property
    def hand(self):
        u"""手札取得。
        """
        return tuple(self.__hand)

    @property
    def hand_by_number(self):
        u"""番号による手札取得。
        """
        return tuple(card.arcanum.number for card in self.__hand)

    @property
    def jokers(self):
        u"""ジョーカー取得。
        """
        return tuple(
            card for card in self.__hand if
            card.arcanum.type == _const.JOKER_ARCANUM)

    # ------ Skill ------
    @property
    def card_skills(self):
        u"""カードスキル取得。
        """
        skills = tuple(
            card.arcanum.skills for card in self.__hand if
            card.arcanum.skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""

    @property
    def creature_skills(self):
        u"""クリーチャースキル取得。
        """
        return self.__group.skills

    # ------ Unit ------
    @property
    def player(self):
        u"""プレイヤー取得。
        """
        return self.__player

    @property
    def equip(self):
        u"""装備情報取得。
        """
        return self.__equip

    @property
    def group(self):
        u"""クリーチャーグループを取得。
        """
        return self.__group
