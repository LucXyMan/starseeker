#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""creature.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

クリーチャーモジュール。
"""
import unit as __unit
import utils.const as _const
import utils.memoize as _memoize
import utils.image as _image
import sprites.effects as _effects


class Creature(__unit.Unit):
    u"""クリーチャー。
    プレイヤーの分身になる。
    """
    __POISON_RATE = 0.025
    __REGENERATION_RATE = 0.0125

    class _Explosion(_effects.effect.Effect):
        u"""クリーチャー撃破エフェクト。
        """
        __STAR_NUMBER = 8
        __STAR_SPEED = 3
        __params = ()

        def __init__(self, pos, groups=None):
            u"""コンストラクタ。
            """
            def __init_params():
                u"""爆発に必要なパラメータを設定。
                """
                import math as __math
                if not Creature._Explosion.__params:
                    angle = 6.28/self.__STAR_NUMBER
                    Creature._Explosion.__params = tuple((
                        round(__math.cos(i*angle)*self.__STAR_SPEED),
                        round(__math.sin(i*angle)*self.__STAR_SPEED)) for
                        i in range(self.__STAR_NUMBER))
            self._images = self._generate(self.__STAR_NUMBER)
            __init_params()
            super(Creature._Explosion, self).__init__(pos, groups)

        def _generate(self, period):
            u"""エフェクト画像の生成。
            """
            class _RainbowStar(_effects.image.Image):
                u"""虹色の星型。
                クリーチャー撃破時のエフェクトに使用。
                """
                __MOVE_PERIOD = 5

                def __init__(self, pos, number, direction, groups=None):
                    u"""コンストラクタ。
                    """
                    self.__counter = 0
                    super(_RainbowStar, self).__init__(
                        pos, "comet_"+str(number & 0x07), direction, groups)

                def _generate(self, sources, direction):
                    u"""エフェクト画像の生成。
                    """
                    for image in self._get_images(sources):
                        for _ in range(_const.FRAME_DELAY):
                            yield image, (
                                direction if self.__counter <
                                self.__MOVE_PERIOD else (0, 0))
                        self.__counter += 1
            for i in range(period):
                yield _image.get_dummy(), (0, 0)
                _RainbowStar(
                    self.rect.center, i, Creature._Explosion.__params[i])

    def __init__(self, pos, data, packet):
        u"""コンスタラクタ。
        """
        import sprites.indicator as __indicator
        self.__is_destroyed = False
        self.__is_poison = False
        self.__frozen_time = 0
        super(Creature, self).__init__(pos, data, packet)
        self.__life = self.__max_life = self._data.life
        if data.tribe == _const.BEAST_TRIBE:
            self.power_plus(1)
        elif data.tribe == _const.ALCHMIC_TRIBE:
            self.protect_plus(1)
        elif data.tribe == _const.SKY_TRIBE:
            self.speed_plus(1)
        __indicator.Life(self)
        __indicator.Frozen(self)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<type: {type}, name: {name}, power_ups: {power_up}, "
            u"direction: {direction}, state: {state}>").format(
            type=self.__class__.__name__, name=self._data.name,
            power_up=self.power_up_level,
            direction="Right" if self._is_right else "Left", state=self.state)

    def destroy(self):
        u"""撃破時エフェクト。
        """
        import material.sound as __sound
        __sound.SE.play("ShockWave")
        self._Explosion(self.rect.center)
        self.flash("Summon")
        self.__is_destroyed = True

    def charge(self, onepieces):
        u"""チャージ処理。
        消去したライン得点をチャージする。
        凍結状態の場合凍結ゲージが減少する。
        """
        if self.is_frozen:
            self.frozen_time -= self._get_power_up_charge(
                self._get_score(onepieces))
        else:
            super(Creature, self).charge(onepieces)

    def attack(self):
        u"""攻撃の処理。
        """
        if not self.is_frozen:
            lv = self._power/self._packet
            power = self.release()
            if 0 < power:
                self.flash()
                return self._get_attack(
                    self._data.str, self.attack_level, power), lv
        return 0, 0

    def receive(self, stroke):
        u"""攻撃の受け取り処理。
        """
        self.life -= stroke
        if self.__life < 0:
            return abs(self.__life)
        return 0

    def poisoning(self):
        u"""毒状態を設定。
        """
        self.__is_poison = False if self.is_frozen else True

    def freezing(self):
        u"""凍結効果。
        """
        self.__frozen_time = int(0 if self.__is_poison else self._packet << 2)

    def death(self, force=False):
        u"""即死効果。不死属性の場合無効。
        """
        if not self.is_undead or force:
            self.__life = 0
            return True
        return False

    def poison_effect(self):
        u"""毒効果処理。
        不死属性の場合回復する。
        """
        if self.is_undead:
            recovery = self.__life+int(self.__max_life*self.__POISON_RATE)
            self.__life = (
                recovery if recovery < self.__max_life else self.__max_life)
        else:
            self.__life -= int(self.__max_life*self.__POISON_RATE)

    def regenerate(self):
        u"""回復効果処理。
        """
        if self.is_regeneratable:
            recovery = self.__life+int(
                self.__max_life*self.__REGENERATION_RATE)
            self.__life = (
                recovery if recovery < self.__max_life else self.__max_life)

    def get_special(self, level):
        u"""攻撃時の特殊効果を取得。
        """
        skill = self._data.skill
        if (
            level and not self.is_frozen and skill and
            skill.type == _const.ATTACK_SKILL_TYPE
        ):
            new, old = self._data.skill.target.split("##")
            rank = self._data.rank
            return new, old.split("#"), (
                (1, 1) if self._data.skill.is_single else
                (level*rank, level*rank+1))
        else:
            return ()

    def get_sustain(self, turn):
        u"""持続特殊効果を取得。
        """
        skill = self._data.skill
        if (
            not self.is_frozen and skill and
            skill.type == _const.SUSTAIN_SKILL_TYPE and
            turn & self._data.skill.sustain == 0
        ):
            new, old = self._data.skill.target.split("##")
            return new, old.split("#"), (1, 1)
        else:
            return ()

    def add_effect(self, effect):
        u"""エフェクトの追加。
        文字表示エフェクトが存在する場合にkillする。
        """
        if self._effect and not self._effect.is_dead:
            self._effect.kill()
            self._effect = None
        self._effect = effect

    def adapt(self, target):
        u"""融合可能な場合、融合後クリーチャーを返す。そうでない場合Noneを返す。
        """
        return self._data.adapt(target)

    def _update_finish(self):
        u"""終了時更新。
        """
        if self.__is_destroyed:
            self.kill()

    @property
    def base_image(self):
        u"""基本画像を取得。
        """
        return self._data.get_image(False)

    @property
    @_memoize.memoize()
    def current_image(self):
        u"""現在画像取得。
        """
        image = self.data.get_image(self.is_right)
        if self.is_poison:
            image = _image.get_colored_ave(image, _const.GREEN)
        elif self.is_frozen:
            image = _image.get_colored_ave(image, _const.CYAN)
        return image

    @property
    def is_half(self):
        u"""ライフが半分かどうかの判定。
        """
        return self.__life <= self.__max_life >> 1

    @property
    def is_quarter(self):
        u"""ライフが1/4かどうかの判定。
        """
        return self.__life <= self.__max_life >> 2

    @property
    def is_dead(self):
        u"""ユニットの死亡判定。
        """
        return self.__life <= 0

    @property
    def is_alive(self):
        u"""ユニットの生存判定。
        """
        return not self.is_dead

    @property
    def max_life(self):
        u"""最大ライフを取得。
        """
        return self.__max_life

    @property
    def life(self):
        u"""現在ライフを取得。
        """
        return self.__life

    @life.setter
    def life(self, value):
        u"""現在ライフを設定。
        """
        def __damage_display(damage):
            u"""ダメージ表示。
            """
            self.flash("Damage")
            if damage:
                self.add_effect(
                    _effects.Damage(self.rect.midbottom, str(damage)))

        def __recovery_display(recover):
            u"""回復表示。
            """
            self.flash("Recovery")
            if recover:
                self.add_effect(
                    _effects.Recovery(self.rect.midbottom, str(recover)))
        if self.__life < value and not self.is_undead:
            old = self.__life
            self.__life = value if value < self.__max_life else self.__max_life
            __recovery_display(self.__life-old)
            self.__is_poison = False
            self.__frozen_time = 0
        elif value < self.__life:
            __damage_display(self.__life-value)
            self.__life = value

    @property
    def hialing_priority(self):
        u"""回復優先度を取得。
        """
        return float(self.__max_life)/float(self.__life)*(
            2 if self.is_poison or self.is_frozen else 1)

    @property
    def str(self):
        u"""クリーチャーの力。
        """
        return self._data.str

    @property
    def vit(self):
        u"""クリーチャーの生命力。
        """
        return self._data.vit

    @property
    def is_poison(self):
        u"""毒状態を取得。
        """
        return self.__is_poison

    @property
    def frozen_time(self):
        u"""凍結時間を取得。
        """
        return self.__frozen_time

    @frozen_time.setter
    def frozen_time(self, value):
        u"""凍結時間を設定。
        """
        self.__frozen_time = 0 if value < 0 else int(value)

    @property
    def is_frozen(self):
        u"""凍結状態かどうかの判定。
        """
        return 0 < self.__frozen_time

    @property
    def is_healths(self):
        u"""クリーチャーが健康体かどうか判定。
        """
        return not self.__is_poison and not self.is_frozen

    @property
    def is_regeneratable(self):
        u"""自己再生効果の使用可能判定。
        """
        return (
            self._data.tribe == _const.DRAGON_TRIBE and
            not self.is_poison and not self.is_frozen)

    @property
    def is_undead(self):
        u"""不死属性判定。
        """
        return self._data.tribe == _const.UNDEAD_TRIBE

    @property
    def name(self):
        u"""名前取得。
        """
        return self._data.name

    @property
    def recepters(self):
        u"""受容可能クリーチャー名取得。
        """
        return self._data.recepters

    @property
    def prevents(self):
        u"""状態変化防止文字列取得。
        """
        skill = self._data.skill
        if (
            skill and not self.is_frozen and
            skill.type == _const.DEFENCE_SKILL_TYPE
        ):
            target = skill.target
            return target.split("#") if target else ()
        return ()

    @property
    def state(self):
        u"""現在の状態文字列取得。
        """
        return (
            u"Poison" if self.is_poison else
            u"Frozen" if self.is_frozen else
            u"Normal")
