#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""phase.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ゲームフェイズモジュール。
"""
import material.sound as _sound
import utils.const as _const


class __Phase(object):
    u"""ゲームフェイズ。
    ゲームシステム状態を表す。
    """
    __slots__ = "_system",

    def __init__(self, system):
        u"""コンストラクタ。
        """
        self._system = system

    def sub_completion(self, rival, thinker):
        u"""コンプリート事前処理。
        """
    def completion(self):
        u"""コンプリート処理。
        """
    def release(self, rival):
        u"""魔術開放処理。
        """
    def throw(self, rival, thinker):
        u"""ピース投下処理。
        """
    def command_input(self, cmd):
        u"""コマンド入出力。
        """
    def command_run(self, cmd, rival):
        u"""コマンド実行。
        """
    def fall(self):
        u"""ピースの自動落下処理。
        """


class __ControlPhase(__Phase):
    u"""コマンド入力可能フェイズ。
    """
    def command_input(self, cmd):
        u"""コマンド入力。
        """
        if cmd:
            self._system.cmds += cmd

    def _sys_cmd(self, cmd):
        u"""音量調整など。
        """
        if cmd == _const.VOLUMEUP_COMMAND:
            _sound.BGM.volume_up()
            return True
        elif cmd == _const.VOLUMEDOWN_COMMAND:
            _sound.BGM.volume_down()
            return True
        elif cmd == _const.MUTE_COMMAND:
            _sound.BGM.mute()
            return True
        return False


class BootPhase(__ControlPhase):
    u"""ブートフェイズ。
    """
    def command_run(self, cmd, rival):
        u"""通常時コマンド。
        """
        if cmd and not rival.is_game_over:
            self._sys_cmd(cmd)


class ThrowingPhase(__ControlPhase):
    u"""スローイングフェイズ。
    ブロックを操作している状態。
    """
    def sub_completion(self, rival, thinker):
        u"""ラインコンプリートの前の事前処理。
        消去したラインをチャージ、リソースの処理等。
        """
        import sprites.effects as __effects

        def __completion_finish():
            u"""補完終了時処理。
            """
            def __attack(rival):
                u"""プレイヤーとモンスターグループのチャージと攻撃。
                """
                if blocks.del_lines:
                    damage = 0
                    effects = []
                    battle.player.charge(blocks.del_lines)
                    battle.group.charge(blocks.del_lines)
                    blocks.del_line_clear()
                    stroke, lv = battle.player.attack()
                    if stroke:
                        damage += stroke
                        effect = battle.player.weapon.get_special(lv)
                        if effect:
                            weapon_info, _, _, _ = battle.equip_info
                            weapon_info.flash()
                        effects.append(effect)
                    for creature in battle.group:
                        stroke, lv = creature.attack()
                        if stroke:
                            damage += stroke
                            ability = creature.get_special(lv)
                            if ability:
                                creature.flash("Ability")
                            effects.append(ability)
                    rival.damage_calc(self._system, damage, effects)

            def __helm_effect():
                u"""兜によるブロック持続変化効果。
                ※自分の防具効果によって防がれる場合がある。
                """
                effect = battle.player.helm.get_sustain(turn)
                if effect:
                    new, old, prm = effect
                    _, head_info, armor_info, _ = battle.equip_info
                    if battle.player.armor.is_prevents(new):
                        armor_info.flash()
                    elif (
                        not battle.group.is_prevents(new) and
                        self._system.blocks.field.replace(prm, (new, old))
                    ):
                        head_info.flash()

            def __sustain_effect():
                u"""クリーチャー持続能力による変化効果。
                """
                for creature in battle.group:
                    effect = creature.get_sustain(turn)
                    if effect:
                        new, old, prm = effect
                        if battle.player.armor.is_prevents(new):
                            _, _, armor_info, _ = battle.equip_info
                            armor_info.flash()
                        elif (
                            not battle.group.is_prevents(new) and
                            self._system.blocks.field.replace(prm, (new, old))
                        ):
                            creature.flash("Ability")

            def __shard_apply():
                u"""シャード効果適用。
                """
                import random as __random
                resorce = self._system.resorce
                for type_ in range(len(resorce.shards)):
                    plus = resorce.shard_release(type_)
                    if type_ == 0:
                        for _ in range(plus << 1 if self._system.has_skill(
                            _const.LIFE_BOOST_SKILL_NAME) else plus
                        ):
                            unit = battle.group.get_injured(
                                battle.group.get_livings(battle.group))
                            if unit:
                                unit.life += int(unit.max_life*0.5)
                            else:
                                equip = list(battle.player.equip)
                                __random.shuffle(equip)
                                for item in equip:
                                    if item.repair():
                                        break
                    elif type_ == 1:
                        plus = (plus << 1 if self._system.has_skill(
                            _const.MIGHTY_SKILL_NAME) else plus)
                        battle.player.power_plus(plus)
                        battle.group.power_plus(plus)
                    elif type_ == 2:
                        plus = plus << 1 if self._system.has_skill(
                            _const.TOUGHNESS_SKILL_NAME) else plus
                        battle.player.protect_plus(plus)
                        battle.group.protect_plus(plus)
                    elif type_ == 3:
                        plus = (plus << 1 if self._system.has_skill(
                            _const.SPEEDSTER_SKILL_NAME) else plus)
                        battle.player.speed_plus(plus)
                        battle.group.speed_plus(plus)
            __attack(rival)
            __helm_effect()
            __sustain_effect()
            __shard_apply()
            blocks.field.turn()
            blocks.update_parameter()
            blocks.is_completed = False
            self._system.cmds = ""
            if thinker:
                thinker.clear()
            self._system.set_thrown()
        blocks = self._system.blocks
        battle = self._system.battle
        is_effectable = False
        if not blocks.field.is_active and self._system.blocks.piece.is_rested:
            if (
                self._system.blocks.piece.is_t_spin and
                not blocks.field.is_super_drop
            ):
                is_effectable = True
                blocks.field.set_super_drop()
            one_pieces = blocks.field.sub_completion(self._system.resorce)
            if one_pieces:
                if is_effectable:
                    _sound.SE.play("Keen")
                    battle.player.add_effect(__effects.Special(
                        battle.player.rect.center, u"メテオドロップ"))
                blocks.del_line_plus(one_pieces)
                blocks.is_completed = True
                self._system.set_complete()
            else:
                turn = self._system.turn
                __completion_finish()

    def fall(self):
        u"""ピース自動落下処理。
        """
        self._system.blocks.fall()

    def command_run(self, cmd, rival):
        u"""通常時コマンド。
        """
        def __pause_command():
            u"""ポーズコマンド。
            """
            if self._system.is_pauseable:
                self._system.is_paused = True
                _sound.BGM.pause()
                _sound.SE.play("Pause")

        def __move_cmd():
            u"""上下左右移動コマンド。
            """
            moved = downed = False
            if cmd == _const.LEFT_COMMAND:
                blocks.piece.slide(blocks.field, False)
                moved = True
            elif cmd == _const.RIGHT_COMMAND:
                blocks.piece.slide(blocks.field, True)
                moved = True
            elif cmd == _const.DOWN_COMMAND:
                blocks.piece.down(blocks.field)
                moved = downed = True
            if cmd == _const.UP_COMMAND:
                blocks.piece.drop(blocks.field)
                moved = downed = True
            if moved:
                blocks.update_display()
            if downed:
                blocks.fall_clear()

        def __rotate_cmd():
            u"""左右回転コマンド。
            """
            if cmd == _const.DECISION_COMMAND:
                blocks.piece.rotate(blocks.field, True)
                blocks.update_display()
            elif cmd == _const.REMOVE_COMMAND:
                blocks.piece.rotate(blocks.field, False)
                blocks.update_display()

        def __summon_cmd():
            u"""召喚コマンド。
            """
            if cmd == _const.USE1_COMMAND:
                battle.reserve(0)
            elif cmd == _const.USE2_COMMAND:
                battle.reserve(1)
            elif cmd == _const.USE3_COMMAND:
                battle.reserve(2)
            elif cmd == _const.USE4_COMMAND:
                battle.reserve(3)
            elif cmd == _const.USE5_COMMAND:
                battle.shred(0)
            elif cmd == _const.USE6_COMMAND:
                battle.shred(1)
            elif cmd == _const.USE7_COMMAND:
                battle.shred(2)
            elif cmd == _const.USE8_COMMAND:
                battle.shred(3)
            elif cmd == _const.CANCEL_COMMAND:
                battle.shuffle()
            elif cmd == _const.USE_COMMAND:
                for i in range(4):
                    if battle.reserve(i):
                        break
            elif cmd == _const.DELETE_COMMAND:
                for i in range(4):
                    if battle.shred(i):
                        break
        if (
            cmd and not self._system. blocks.field.is_active and
            not rival.is_game_over
        ):
            if cmd == _const.START_COMMAND:
                __pause_command()
            else:
                blocks = self._system.blocks
                battle = self._system.battle
                if cmd == _const.HOLD_COMMAND:
                    blocks.hold.capture()
                __move_cmd()
                __rotate_cmd()
                __summon_cmd()
                self._sys_cmd(cmd)

    def release(self, rival):
        u"""魔術開放処理。
        """
        if not self._system.blocks.field.is_active:
            self._system.battle.release(rival)


class ThrownPhase(__Phase):
    u"""ピース接地後の処理フェイズ。
    """
    def throw(self, rival, thinker):
        u"""ブロック投下時の処理。
        1: 敵の攻撃をdamageに追加する。
        2: ダメージ計算。
        """
        def __press():
            u"""プレス処理。
            """
            pressure = self._system.accumulate.release_pressure()
            if 0 < pressure:
                level = (
                    _const.ADAMANT_PRESS_LEVEL >> 1 if
                    _const.ADAMANT_PRESS_LEVEL < pressure else
                    _const.SOLID_PRESS_LEVEL >> 1 if
                    _const.SOLID_PRESS_LEVEL < pressure else 1)
                press, add_pressure = divmod(pressure, level)
                self._system.accumulate.add_pressure(
                    add_pressure*_const.PRESS_POINT)
                self._system.cmds = ""
                if thinker:
                    thinker.clear()
                for effect in self._system.accumulate.release_effects():
                    if effect:
                        new, old, prm = effect
                        blocks.field.replace(prm, (new, old))
                blocks.field.press(press, level)
                __press()

        def __game_over_test():
            u"""ピースがフィールドに接触した時の処理。
            """
            if blocks.field.is_collide(blocks.piece):
                _sound.SE.play("Error")
                self._system.set_lose()
                if rival.blocks.field.is_collide(rival.blocks.piece):
                    rival.set_lose()
                else:
                    rival.set_win()
        blocks = self._system.blocks
        blocks.advance()
        __press()
        blocks.update_display()
        __game_over_test()
        blocks.hold.is_captured = False
        self._system.battle.turn()
        self._system.set_throwing()


class CompletePhase(__Phase):
    u"""コンプリートフェイズ。
    """
    def completion(self):
        u"""コンプリート処理。
        """
        blocks = self._system.blocks
        if not blocks.field.is_active:
            blocks.field.completion()
            self._system.set_throwing()
