#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""manager.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲーム進行管理モジュール。
"""
import armament.levels as _levels
import armament.units as _units
import input as _input
import inventories as _inventories
import material.misc as _misc
import material.sound as _sound
import sprites.effects as _effects
import system as _system
import utils.const as _const
import utils.image as _image
import utils.screen as _screen


# ---- Phase ----
class __Phase(object):
    u"""ゲームフェイズ。
    """
    def __init__(self, manager):
        u"""コンストラクタ。
        """
        self._manager = manager

    def run(self):
        u"""実行。
        """


class _Boot(__Phase):
    u"""起動フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.boot()
        self._manager.command_io()


class _Drive(__Phase):
    u"""通常進行フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.release()
        self._manager.throw()
        self._manager.command_io()
        self._manager.complete()
        self._manager.terminate()


class _Disappear(__Phase):
    u"""ブロック消滅フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.complete()
        self._manager.disappear()


class _Crushing(__Phase):
    u"""クリーチャー撃破フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.complete()
        self._manager.crushing()


class _Winning(__Phase):
    u"""ゲーム勝敗表示フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.complete()
        self._manager.winning()


class _Result(__Phase):
    u"""ボーナス表示フェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.complete()
        if not _effects.Effect.is_active():
            self._manager.result()


class _Finish(__Phase):
    u"""フィニッシュフェイズ。
    """
    def run(self):
        u"""実行。
        """
        self._manager.complete()
        self._manager.finish()


class _Done(__Phase):
    u"""終了フェイズ。
    """
    pass


# ---- Manager ----
class __Manager(object):
    u"""ゲームシステム進行管理。
    """
    __slots__ = (
        "_1p", "_2p", "_controler_1p", "_is_error", "_parent", "_phase",
        "_rank")

    def __init__(self):
        u"""コンストラクタ。
        """
        import puzzle as __puzzle
        self._phase = _Boot(self)
        self._parent = __puzzle.Parent()
        self._controler_1p = _input.Main(0)
        self._is_error = False

    # ---- Normal ----
    def boot(self):
        u"""ゲーム開始時処理。
        """
        if not _effects.Effect.is_active():
            self._1p.set_throwing()
            self._2p.set_throwing()
            self._phase = _Drive(self)

    def release(self):
        u"""アルカナ開放処理。
        """
        self._1p.release(self._2p)
        self._2p.release(self._1p)

    def throw(self):
        u"""ピース投下時処理。
        """
        self._1p.throw(self._2p)
        self._2p.throw(self._1p)

    def command_io(self):
        u"""コマンド入出力。
        """
        self._controler_1p.input()
        self._1p.input_command(self._controler_1p.output())
        self._1p.run_command(self._2p)
        self._1p.fall()
        self._2p.thinker.start()
        self._2p.input_command(self._2p.thinker.output())
        self._2p.run_command(self._1p)
        self._2p.fall()

    def complete(self):
        u"""フィールド補完処理。
        """
        if not self._1p.is_lose:
            self._1p.complete(self._2p)
        if not self._2p.is_lose:
            self._2p.complete(self._1p)

    # ---- Terminate ----
    def terminate(self):
        u"""メインゲーム終了処理。
        """
        if self._1p.is_game_over or self._2p.is_game_over:
            if self._2p.thinker:
                self._2p.thinker.terminate()
            self._phase = _Disappear(self)

    def disappear(self):
        u"""セルの消去処理。
        """
        if self._1p.is_lose:
            self._1p.puzzle.vanish()
        if self._2p.is_lose:
            self._2p.puzzle.vanish()
        self._phase = _Crushing(self)

    def crushing(self):
        u"""クリーチャー撃破処理。
        """
        if not (
            self._1p.puzzle.field.is_active or
            self._2p.puzzle.field.is_active
        ):
            if self._1p.is_lose:
                self._1p.battle.group.destroy(
                    resource=self._2p.resource, detect=self._1p.flash,
                    is_game_over=True)
            if self._2p.is_lose:
                self._2p.battle.group.destroy(
                    resource=self._1p.resource, detect=self._2p.flash,
                    is_game_over=True)
            self._phase = _Winning(self)

    def winning(self):
        u"""勝利・敗北エフェクト。
        """
        if not _effects.Effect.is_active():
            if not self._1p.is_win and not self._2p.is_win:
                _sound.SE.play("draw")
                _effects.Draw(_screen.Screen.get_base().get_rect().center)
            else:
                Result = _effects.Win if self._1p.is_win else _effects.Lose
                Result(self._1p.puzzle.window.rect.center)
                Result = _effects.Win if self._2p.is_win else _effects.Lose
                Result(self._2p.puzzle.window.rect.center)
            self._phase = _Result(self)

    # ---- Result ----
    def _get_sp(self, total):
        u"""追加するSPを取得
        """
        return (
            total*4 if self._rank == 3 else total*3 if self._rank == 2 else
            total*2 if self._rank == 1 else total)

    def _win(self):
        u"""勝利時のリザルト処理。
        """
        _sound.SE.play("bonus")
        added = self._get_sp(self._1p.resource.total)
        _inventories.add_sp(added)
        self._1p.battle.player.add_effect(_effects.Bonus(
            _screen.Screen.get_base().get_rect().center, added))
        self._1p.resource.vanish()

    def _lose(self):
        u"""敗北時処理。
        """
    def result(self):
        u"""リザルト処理。
        """
        if self._1p.is_win:
            self._win()
        if self._1p.is_lose:
            self._lose()
        self._phase = _Finish(self)

    # ---- Finish ----
    def finish(self):
        u"""終了処理。
        """
        if not _effects.Effect.is_active():
            self._phase = _Done(self)

    # ---- Manage ----
    def _reset(self):
        u"""リセット時処理。
        """
        if self._2p.thinker:
            self._2p.thinker.terminate()

    def manage(self):
        u"""ゲーム進行管理。
        """
        def __pause_run():
            u"""ゲーム停止時のコマンド。
            """
            import material.sound as __sound
            import utils.const as __const
            self._controler_1p.input()
            output = self._controler_1p.output()
            if output == __const.START_COMMAND:
                self._1p.is_paused = self._2p.is_paused = False
                __sound.BGM.unpause()
            elif output == __const.SELECT_COMMAND:
                self._reset()
                self._phase = _Done(self)
        if self.is_paused:
            __pause_run()
        else:
            self._phase.run()

    # ---- Property ----
    @property
    def is_win(self):
        u"""1P勝利状態取得。
        """
        return self._1p.is_win

    @property
    def is_paused(self):
        u"""ポーズ状態取得。
        """
        return self._1p.is_paused or self._2p.is_paused

    @property
    def is_done(self):
        u"""ゲーム終了状態取得。
        """
        return isinstance(self._phase, _Done)

    @property
    def is_error(self):
        u"""エラー発生状態取得。
        """
        return self._is_error


class Duel(__Manager):
    u"""デュエル進行管理。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        level: 2P側のレベル。
        """
        level = _levels.get_duel()
        number, self._rank = level.player
        _sound.BGM.play("lv{lv}".format(lv=self._rank+1))
        _effects.Rival(_units.get_player(number).name)
        super(Duel, self).__init__()
        _image.BackGround.set_image(_misc.get(_const.BG_DICT[number]))
        self._1p = _system.System(
            _levels.get_1p(self._rank), self._parent, id_=0)
        self._2p = _system.System(level, self._parent, id_=1)
        self._2p.set_thinker(self._1p)


class Endless(__Manager):
    u"""エンドレス進行管理。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        level: 2P側のレベル。
        """
        _effects.Progress(_inventories.Endless.get_progress()+1)
        super(Endless, self).__init__()
        level = _levels.get_endless()
        number, self._rank = level.player
        _sound.BGM.play("lv{lv}".format(lv=self._rank+1))
        _image.BackGround.set_image(_misc.get(_const.BG_DICT[number]))
        self._1p = _system.System(
            _levels.get_1p(self._rank), self._parent, id_=0)
        self._2p = _system.System(level, self._parent, id_=1)
        self._2p.set_thinker(self._1p)

    def _win(self):
        u"""勝利時処理。
        """
        super(Endless, self)._win()
        progress = _inventories.Endless.get_progress()
        _inventories.Endless.set_reached(progress)

    def _lose(self):
        u"""敗北時処理。
        """
        _inventories.Endless.set_progress(
            _inventories.Endless.get_progress()-(_const.ENDLESS_INTRVAL+1))

    def _reset(self):
        u"""リセット時処理。
        """
        super(Endless, self)._reset()
        self._lose()


class Versus(__Manager):
    u"""ヴァーサス進行管理。
    """
    __slots__ = "__controler_2p",

    def __init__(self):
        u"""コンストラクタ。
        level: 2P側のレベル。
        """
        level = _levels.get_2p()
        number, self._rank = level.player
        _sound.BGM.play("lv{lv}".format(lv=self._rank+1))
        _effects.Rival(_units.get_player(number).name)
        super(Versus, self).__init__()
        self.__controler_2p = _input.Main(1)
        self._is_error = self.__controler_2p.is_init_error
        if not self._is_error:
            self._controler_1p.is_keyboard_available = False
            self.__controler_2p.is_keyboard_available = False
            _image.BackGround.set_image(_misc.get(_const.BG_DICT[number]))
            self._1p = _system.System(
                _levels.get_1p(self._rank), self._parent, id_=0)
            self._2p = _system.System(level, self._parent, id_=1)
            self._1p.is_pause_available = False
            self._2p.is_pause_available = False

    def command_io(self):
        u"""コマンド入出力。
        """
        self._controler_1p.input()
        self._1p.input_command(self._controler_1p.output())
        self._1p.run_command(self._2p)
        self._1p.fall()
        self.__controler_2p.input()
        self._2p.input_command(self.__controler_2p.output())
        self._2p.run_command(self._1p)
        self._2p.fall()

    def result(self):
        u"""リザルト処理。
        """
        added = self._get_sp(
            self._1p.resource.total+self._2p.resource.total >> 1)
        _inventories.add_sp(added)
        _sound.SE.play("bonus")
        self._1p.battle.player.add_effect(_effects.Bonus(
            _screen.Screen.get_base().get_rect().center, added))
        self._1p.resource.vanish()
        self._2p.resource.vanish()
        self._phase = _Finish(self)
