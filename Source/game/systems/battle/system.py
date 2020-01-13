#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""system.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

戦闘システムモジュール。
"""
import sprites.effects as _effects
import utils.const as _const
import utils.general as _general
import utils.layouter as _layouter


class System(object):
    u"""戦闘システム。
    ユニット・アルカナを管理。
    """
    __slots__ = (
        "__catalyst", "__core", "__equip_huds", "__group", "__hand",
        "__player", "__reserved", "__spell_point")
    __SPELL_COST = 2

    def __init__(self, core, level):
        u"""コンストラクタ。
        """
        import armament.units as __units
        import hand as __hand
        import sprites.huds as __huds
        self.__spell_point = self.__SPELL_COST
        self.__core = core
        self.__hand = __hand.Hand(self.__core)
        number, _ = level.player
        puzzle = self.__core.puzzle
        self.__player = __units.Player(
            (0, 0), __units.get_player(number), puzzle.field.packet)
        _layouter.Game.set_player(self.__player, puzzle.window)
        self.__player.is_another = self.__core.id
        self.__player.is_right = not self.__core.id
        self.__player.set_equip(level.equip)
        self.__equip_huds = tuple(
            __huds.Equip((0, 0), item) for item in self.__player.equip)
        _layouter.Game.set_equip(self.__core, self.__equip_huds)
        self.__group = __units.Group(self.__core, self.__player)
        self.__catalyst = None
        self.__reserved = None

    def turn(self):
        u"""ターン毎の処理。
        """
        self.__spell_point = self.__SPELL_COST
        self.__hand.draw(*self.__core.resource.draw())
        self.__player.turn()
        self.__group.turn()
        self.__group.destroy()
        self.__core.update()

    # ---- Arcana ----
    def __consume_spell(self):
        u"""呪文ポイントを消費。
        """
        has_ds = self.__core.has_skill(_const.DOUBLE_SPELL_SKILL)
        sub = self.__SPELL_COST >> 1 if has_ds else self.__SPELL_COST
        self.__spell_point -= sub

    def __intercept(self, rival, sorcery):
        u"""シールド処理。
        rival: 対戦相手のシステム。
        sorcery: 対戦相手のソーサリー。
        """
        for card in self.__hand:
            if (
                card.arcanum.type == _const.SHIELD_ARCANUM and
                sorcery.star == card.arcanum.star
            ):
                self.__player.add_effect(_effects.Spell(
                    self.__player.rect.center, card.arcanum))
                self.__hand.remove(card)
                card.arcanum.activate((self.__core, rival), False)
                return True
        return False

    def discard(self, number, is_force=False):
        u"""カードを捨てる。
        number: 捨てるカードの番号。
        is_force: 真の場合に強制削除。
        """
        def __remove():
            u"""カード削除。
            """
            import sprites.effects as __effects
            self.__hand.remove(waste)
            self.__player.add_effect(__effects.Shred(
                self.__player.rect.center, waste.arcanum))
            _layouter.Game.set_hand(self.__core, True)

        def __soul_eat():
            u"""サモンカード削除時にエレメンタルを取得する。
            """
            if (
                arcanum_type == _const.SUMMON_ARCANUM and
                self.__core.flash(_const.SOUL_EAT_SKILL)
            ):
                self.__core.resource.increase(
                    waste.arcanum.star, _const.STAR_ENERGY)
        if number < len(self.__hand) and (0 < self.__spell_point or is_force):
            waste = self.__hand[number]
            arcanum_type = waste.arcanum.type
            if arcanum_type != _const.JOKER_ARCANUM:
                __remove()
                if not is_force:
                    self.__consume_spell()
                    __soul_eat()
                self.__core.update()
                return waste.arcanum.number,
            elif not is_force and self.__core.flash(_const.PURIFY_SKILL):
                __remove()
                self.__consume_spell()
        self.__core.update()
        return ()

    def reserve(self, number):
        u"""アルカナ予約処理。
        """
        if number < len(self.__hand):
            arcanum = self.__hand[number].arcanum
            is_summonable = arcanum.type == _const.SUMMON_ARCANUM and (
                not self.__group.is_full or self.__group.adapt(arcanum))
            order = self.__core.resource.get_available_state(arcanum) & 0x00F
            is_available = 0 < order and (
                is_summonable or arcanum.type in
                (_const.SORCERY_ARCANUM, _const.JOKER_ARCANUM))
            if 0 < self.__spell_point and is_available:
                self.__core.resource.consume(arcanum)
                self.__reserved = arcanum
                self.__hand.remove(self.__hand[number])
                self.__consume_spell()
                self.__hand.update()
                return True
        return False

    def release(self, rival):
        u"""予約したカードの使用処理。
        """
        def __release_summon(summon):
            u"""サモンカード処理。
            """
            if rival.has_skill(
                _const.ANTI_SUMMONING_SKILL
            ) and rival.battle.__intercept(self.__core, summon):
                rival.flash(_const.ANTI_SUMMONING_SKILL)
                return summon, True
            else:
                fusioned = self.__group.adapt(summon)
                if fusioned:
                    self.__group.fusion(summon)
                    return fusioned, False
                else:
                    self.__group.summon(summon)
                    if self.__core.flash(_const.POISON_SUMMON_SKILL):
                        self.__group[-1].poison()
                    return summon, False

        def __release_sorcery(sorcery):
            u"""ソーサリーカード処理。
            """
            is_reverse = self.__core.flash(_const.REVERSE_SORCERY_SKILL)
            if rival.battle.__intercept(self.__core, sorcery):
                return sorcery, True, is_reverse
            else:
                if self.__catalyst:
                    altered = sorcery.adapt(self.__catalyst)
                    if altered:
                        sorcery = altered
                sorcery.activate((self.__core, rival), is_reverse)
                self.__catalyst = (
                    sorcery if sorcery.type == _const.SORCERY_ARCANUM else
                    None)
                return sorcery, False, is_reverse
        is_delete = False
        arcanum = self.__reserved
        if arcanum and rival.is_throwing and not rival.puzzle.field.is_active:
            is_summon = arcanum.type == _const.SUMMON_ARCANUM
            if is_summon:
                arcanum, is_delete = __release_summon(arcanum)
            else:
                arcanum, is_delete, is_reverse = (__release_sorcery(arcanum))
            center = self.__player.rect.center
            if is_delete:
                self.__player.add_effect(_effects.Shred(center, arcanum))
            else:
                self.__player.add_effect(_effects.Spell(
                    center, arcanum, not is_summon and is_reverse))
            self.__reserved = None
            self.__core.update()

    # ---- Skill ----
    def flash(self, skill):
        u"""スキル所持対象を光らせる。
        """
        name = _general.get_skill_names(skill)
        for hud, item in zip(self.__equip_huds, self.__player.equip):
            if name in item.skills.split("#"):
                hud.flash()
                return True
        if self.__group.flash(skill) or self.__hand.burn(skill):
            return True
        return False

    # ---- Property ----
    @property
    def hand(self):
        u"""手札取得。
        """
        return self.__hand

    @property
    def catalyst(self):
        u"""触媒ソーサリー取得。
        """
        return self.__catalyst

    @property
    def is_arcana_available(self):
        u"""アルカナ・カード削除使用可能な場合に真。
        """
        return not self.__reserved and 0 < self.__spell_point

    # ------ Unit ------
    @property
    def player(self):
        u"""プレイヤー取得。
        """
        return self.__player

    @property
    def equip_huds(self):
        u"""装備HUD取得。
        """
        return self.__equip_huds

    @property
    def group(self):
        u"""クリーチャーグループを取得。
        """
        return self.__group

    # ------ Skill ------
    @property
    def skills(self):
        u"""スキル取得。
        """
        skills = tuple(skills for skills in (
            self.__player.skills, self.__group.skills,
            self.__hand.skills) if skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""
