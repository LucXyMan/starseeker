#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""phase.py

Copyright (c) 2019 Yukio Kuro
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

    def sub_complete(self, rival, thinker):
        u"""コンプリート事前処理。
        """
    def complete(self):
        u"""コンプリート処理。
        """
    def release(self, rival):
        u"""アルカナ開放処理。
        """
    def throw(self, rival, thinker):
        u"""ピース投下処理。
        """
    def input_command(self, cmd):
        u"""コマンド入出力。
        """
    def run_command(self, cmd, rival):
        u"""コマンド実行。
        """
    def fall(self):
        u"""ピースの自動落下処理。
        """


class __ControlPhase(__Phase):
    u"""コマンド入力可能フェイズ。
    """
    __slots__ = ()

    def input_command(self, cmd):
        u"""コマンド入力。
        """
        if cmd:
            self._system.cmds += cmd

    def _run_system_command(self, cmd):
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
    __slots__ = ()

    def run_command(self, cmd, rival):
        u"""通常時コマンド。
        """
        if cmd and not rival.is_game_over:
            self._run_system_command(cmd)


class ThrowingPhase(__ControlPhase):
    u"""スローイングフェイズ。
    ブロックを操作している状態。
    """
    __slots__ = ()

    def sub_complete(self, rival, thinker):
        u"""ラインコンプリートの前の事前処理。
        消去したラインをチャージ、リソースの処理等。
        """
        import sprites.effects as __effects

        def __completion_finish():
            u"""補完終了時処理。
            """
            def __apply_shard():
                u"""シャード効果適用。
                """
                def __recovery():
                    u"""ライフ回復。
                    """
                    for _ in range(plus):
                        unit = battle.group.get_injured(
                            battle.group.get_livings(battle.group))
                        if unit:
                            unit.life_with_effect += int(unit.max_life*0.5)
                        else:
                            equip = list(battle.player.equip)
                            __random.shuffle(equip)
                            for item in equip:
                                if item.repair():
                                    return None

                def __enhence():
                    u"""パワーアップ追加。
                    """
                    battle.player.enhance(type_-1, plus)
                    battle.group.enhance(type_-1, plus)
                import random as __random
                resource = self._system.resource
                for type_ in range(len(resource.shards)):
                    skills = (
                        _const.LIFE_BOOST_SKILL, _const.MIGHTY_SKILL,
                        _const.TOUGHNESS_SKILL, _const.SPEEDSTER_SKILL)
                    plus = resource.release(type_)
                    if 0 < plus:
                        has_skill = self._system.flash(skills[type_])
                        plus = plus << 1 if has_skill else plus
                        if type_ == 0:
                            __recovery()
                        else:
                            __enhence()

            def __attack(rival):
                u"""プレイヤーとモンスターグループのチャージと攻撃。
                """
                if puzzle.one_pieces:
                    damage = 0
                    effects = []
                    battle.player.charge(puzzle.one_pieces)
                    battle.group.charge(puzzle.one_pieces)
                    puzzle.clear_line()
                    stroke, lv = battle.player.attack()
                    if stroke:
                        damage += stroke
                        effect = battle.player.weapon.get_enchant(lv)
                        if effect:
                            weapon, _, _, _ = battle.equip_huds
                            weapon.flash()
                            effects.append(effect)
                    for card in battle.hand:
                        effect = card.arcanum.get_enchant(lv)
                        if effect:
                            card.flash()
                            effects.append(effect)
                    for creature in battle.group:
                        stroke, lv = creature.attack()
                        if stroke:
                            damage += stroke
                            effect = creature.get_enchant(lv)
                            if effect:
                                creature.flash("skill")
                                effects.append(effect)
                    rival.damage_calc(self._system, damage, effects)

            def __effect_joker():
                u"""ジョーカー減衰効果。
                """
                jokers = battle.hand.jokers
                if jokers and not self._system.flash(_const.TALISMAN_SKILL):
                    for card in jokers:
                        if self._system.resource.disappear():
                            card.flash()
                        else:
                            break

            def __effect_head():
                u"""頭防具によるブロック持続効果。
                自分の体防具効果によって防がれる場合がある。
                """
                effect = battle.player.helm.get_persistence(turn)
                if effect:
                    new, old, prm = effect
                    _, head, armor, _ = battle.equip_huds
                    if battle.player.armor.is_prevention(new):
                        armor.flash()
                    elif (
                        not battle.group.is_prevention(new) and
                        self._system.puzzle.field.replace(prm, (new, old))
                    ):
                        head.flash()

            def __effect_card():
                u"""カードによる持続効果。
                自分の防具効果によって防がれる場合がある。
                """
                for card in battle.hand:
                    effect = card.arcanum.get_persistence(turn)
                    if effect:
                        new, old, prm = effect
                        _, _, armor, _ = battle.equip_huds
                        if battle.player.armor.is_prevention(new):
                            armor.flash()
                        elif (
                            not battle.group.is_prevention(new) and
                            self._system.puzzle.field.replace(prm, (new, old))
                        ):
                            card.flash()

            def __effect_creature():
                u"""クリーチャーによる持続効果。
                自分の防具効果によって防がれる場合がある。
                """
                for creature in battle.group:
                    effect = creature.get_persistence(turn)
                    if effect:
                        new, old, prm = effect
                        if battle.player.armor.is_prevention(new):
                            _, _, armor, _ = battle.equip_huds
                            armor.flash()
                        elif (
                            not battle.group.is_prevention(new) and
                            self._system.puzzle.field.replace(prm, (new, old))
                        ):
                            creature.flash("skill")
            __apply_shard()
            __attack(rival)
            __effect_joker()
            self._system.forward()
            turn = self._system.turn
            __effect_head()
            __effect_card()
            __effect_creature()
            puzzle.field.turn()
            puzzle.update_parameter()
            puzzle.is_completed = False
            self._system.cmds = ""
            self._system.set_thrown()
            if thinker:
                thinker.clear()
        puzzle = self._system.puzzle
        battle = self._system.battle
        is_effectable = False
        if not puzzle.field.is_active and self._system.puzzle.piece.is_rested:
            if (
                self._system.puzzle.piece.is_t_spin and
                not puzzle.field.is_super_drop
            ):
                is_effectable = True
                puzzle.field.set_super_drop()
            one_pieces = puzzle.field.sub_complete(
                self._system.resource, detect=self._system.flash)
            if one_pieces:
                if is_effectable:
                    _sound.SE.play("keen")
                    battle.player.add_effect(__effects.Special(
                        battle.player.rect.center, u"メテオドロップ"))
                puzzle.extend_line(one_pieces)
                puzzle.is_completed = True
                self._system.set_complete()
            else:
                __completion_finish()

    def fall(self):
        u"""ピース自動落下処理。
        """
        self._system.puzzle.fall()

    def run_command(self, cmd, rival):
        u"""通常時コマンド。
        """
        def __run_pause_command():
            u"""ポーズコマンド。
            """
            if self._system.is_pause_available:
                _sound.SE.play("pause")
                self._system.is_paused = True
                _sound.BGM.pause()

        def __run_move_command():
            u"""上下左右移動コマンド。
            """
            is_moved = is_downed = False
            if cmd == _const.LEFT_COMMAND:
                puzzle.piece.slide(puzzle.field, False)
                is_moved = True
            elif cmd == _const.RIGHT_COMMAND:
                puzzle.piece.slide(puzzle.field, True)
                is_moved = True
            elif cmd == _const.DOWN_COMMAND:
                puzzle.piece.down(puzzle.field)
                is_moved = is_downed = True
            if cmd == _const.UP_COMMAND:
                puzzle.piece.drop(puzzle.field)
                is_moved = is_downed = True
            if is_moved:
                puzzle.update_window()
            if is_downed:
                puzzle.clear_fall()

        def __run_rotate_command():
            u"""左右回転コマンド。
            """
            if cmd == _const.DECISION_COMMAND:
                puzzle.piece.rotate(puzzle.field, True)
                puzzle.update_window()
            elif cmd == _const.REMOVE_COMMAND:
                puzzle.piece.rotate(puzzle.field, False)
                puzzle.update_window()

        def __run_summon_command():
            u"""召喚コマンド。
            """
            for i, use_cmd in enumerate((
                _const.USE1_COMMAND, _const.USE2_COMMAND,
                _const.USE3_COMMAND, _const.USE4_COMMAND
            )):
                if cmd == use_cmd:
                    battle.reserve(i)
                    return None
            for i, use_cmd in enumerate((
                _const.USE5_COMMAND, _const.USE6_COMMAND,
                _const.USE7_COMMAND, _const.USE8_COMMAND
            )):
                if cmd == use_cmd:
                    battle.discard(i)
                    return None
            if cmd == _const.USE_COMMAND:
                for i in range(len(battle.hand)):
                    if battle.reserve(i):
                        break
            elif cmd == _const.DELETE_COMMAND:
                for i in range(len(battle.hand)):
                    if battle.discard(i):
                        break
            elif cmd == _const.CANCEL_COMMAND:
                battle.hand.shuffle()
        if (
            cmd and not self._system. puzzle.field.is_active and
            not rival.is_game_over
        ):
            if cmd == _const.START_COMMAND:
                __run_pause_command()
            else:
                puzzle = self._system.puzzle
                battle = self._system.battle
                if cmd == _const.HOLD_COMMAND:
                    puzzle.hold.capture()
                __run_move_command()
                __run_rotate_command()
                __run_summon_command()
                self._run_system_command(cmd)

    def release(self, rival):
        u"""アルカナ開放処理。
        """
        if not self._system.puzzle.field.is_active:
            self._system.battle.release(rival)


class ThrownPhase(__Phase):
    u"""ピース接地後の処理フェイズ。
    """
    __slots__ = ()

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
                pressure, remainder = divmod(pressure, level)
                self._system.accumulate.add_pressure(
                    remainder*_const.PRESS_POINT)
                self._system.cmds = ""
                if thinker:
                    thinker.clear()
                for effect in self._system.accumulate.release_effects():
                    if effect:
                        new, old, prm = effect
                        puzzle.field.replace(prm, (new, old))
                puzzle.field.press(pressure, level, detect=self._system.flash)
                __press()

        def __game_over_test():
            u"""ピースがフィールドに接触した時の処理。
            """
            if puzzle.field.is_collide(puzzle.piece):
                _sound.SE.play("error")
                self._system.set_lose()
                if rival.puzzle.field.is_collide(rival.puzzle.piece):
                    rival.set_lose()
                else:
                    rival.set_win()
        puzzle = self._system.puzzle
        puzzle.forward()
        __press()
        puzzle.update_window()
        __game_over_test()
        puzzle.hold.is_captured = False
        self._system.battle.turn()
        self._system.set_throwing()


class CompletePhase(__Phase):
    u"""コンプリートフェイズ。
    """
    __slots__ = ()

    def complete(self):
        u"""コンプリート処理。
        """
        puzzle = self._system.puzzle
        if not puzzle.field.is_active:
            puzzle.field.complete()
            self._system.set_throwing()
