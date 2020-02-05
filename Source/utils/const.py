#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""const.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

定数モジュール。
複数モジュールで共有する変数。
"""
# ---- System ----
CAPTION = u"Star Seeker"
COPYRIGHT = u"Copyright (c) 2019 Yukio Kuro"
VERSION = u"1.1.2"
IS_MULTIPROCESSING = True
BASE_SCREEN_SIZE = 320, 240
MAIN_SCREEN_SIZE = 640, 480
FRAME_RATE = 60
FRAME_DELAY = FRAME_RATE/15
GRID_SHIFT = 4
GRID = 1 << GRID_SHIFT
NEXT_WINDOW_SIZE = GRID << 1, GRID << 1
BG_DICT = {
    0: "boneyard", 1: "ruins", 2: "night_city", 3: "ruins",
    4: "night_city", 5: "night_city", 6: "boneyard", 7: "catacombe",
    8: "catacombe"}
# ---- String ----
SYSTEM_CHAR_SIZE = 10
EFFECT_CHAR_SIZE = 12
MODE_CHAR_SIZE = 32
SPEED_TEXTS = "VeryFast", "Fast", "Normal", "Slow", "VerySlow"
FIELD_SIZE_TEXTS = "Small", "Normal", "Large", "VeryLarge"
# ---- Mode ----
EXIT_STATUS = -1
IGNORE_STATUS = 0
MODE_SELECT_STATUS = 1
DUEL_SELECT_STATUS = 2
DUEL_STATUS = 3
ENDLESS_STATUS = 4
VERSUS_SELECT_STATUS = 5
VERSUS_STATUS = 6
CUSTOM_STATUS = 7
INTERVAL_STATUS = 8
RESULT_STATUS = 9
# ---- Game ----
PRESS_POINT = 100
PRESS_LIMIT = PRESS_POINT << 4
SOLID_PRESS_LEVEL = 4
ADAMANT_PRESS_LEVEL = 8
STAR_ENERGY_SHIFT = 2
STAR_ENERGY = 1 << STAR_ENERGY_SHIFT
ENDLESS_LIMIT = 40
ENDLESS_INTRVAL = 5
SKILL_CAPACITY = 8
DECK_CAPACITY = 16
PLEYERS = 8
BASIC_COLORS = 8
NUMBER_OF_STAR = 7
NUMBER_OF_HAND = 4
# ---- Name ----
ALTAIR_NAME = u"アルタイル"
CORVUS_NAME = u"コーヴァス"
NOVA_NAME = u"ノヴァ"
SIRIUS_NAME = u"シリウス"
CASTOR_NAME = u"カストル"
PLUTO_NAME = u"プルート"
REGULUS_NAME = u"レグルス"
LUCIFER_NAME = u"ルキフェル"
NEBULA_NAME = u"ネビュラ"
WARRIOR_ROLE = u"ウォーリア"
WIZARD_ROLE = u"ウィザード"
SEEKER_ROLE = u"シーカー"
ROYAL_ROLE = u"ロイヤル"
MONSTER_ROLE = u"モンスター"
SUMMON_ARCANUM = u"サモン"
FUSIONED_ARCANUM = u"フュージョン"
SORCERY_ARCANUM = u"ソーサリー"
ALTERED_ARCANUM = u"オルタナ"
SUPPORT_ARCANUM = u"サポート"
SHIELD_ARCANUM = u"シールド"
JOKER_ARCANUM = u"ジョーカー"
SWORD_CATEGORY = u"剣"
WAND_CATEGORY = u"杖"
HEAVY_CATEGORY = u"重武器"
MISSILE_CATEGORY = u"飛び道具"
WEAPON_CATEGORYS = (
    SWORD_CATEGORY, WAND_CATEGORY,
    HEAVY_CATEGORY, MISSILE_CATEGORY)
HAT_CATEGORY = u"帽子"
HELMET_CATEGORY = u"兜"
CROWN_CATEGORY = u"王冠"
HEAD_CATEGORYS = HAT_CATEGORY, HELMET_CATEGORY, CROWN_CATEGORY
CLOTHES_CATEGORY = u"服"
ARMOR_CATEGORY = u"鎧"
ROBE_CATEGORY = u"ローブ"
BODY_CATEGORYS = CLOTHES_CATEGORY, ARMOR_CATEGORY, ROBE_CATEGORY
RING_CATEGORY = u"指輪"
ACCESSORY_CATEGORYS = RING_CATEGORY,
BEAST_TRIBE = u"獣"
SKY_TRIBE = u"飛行"
ALCHMIC_TRIBE = u"錬金生物"
REGULAR_TRIBES = BEAST_TRIBE, SKY_TRIBE, ALCHMIC_TRIBE
UNDEAD_TRIBE = u"不死"
DRAGON_TRIBE = u"竜"
STAR_CHARS = u"木", u"火", u"土", u"金", u"水", u"月", u"太陽"
# ---- Skill ----
FIRE_EATER_SKILL = u"ファイアイーター#マグマを破壊"
ICE_PICKER_SKILL = u"アイスピッカー#アイスを破壊"
ACID_ERASER_SKILL = u"アシッドイレーザー#アシッドを破壊"
STONE_BREAKER_SKILL = u"ストーンブレーカー#ストーンを破壊"
POWER_STROKE_SKILL = u"パワーストローク#硬いブロックを一撃で破壊"
EXORCIST_SKILL = u"エクソシスト#悪霊を破壊"
PHANTOM_THIEF_SKILL = u"ファントムシーフ#宝箱をカギ無しで開ける"
WATER_PRESS_SKILL = u"ウォータープレス#プレスをウォーターに"
CHOCOLATE_PRESS_SKILL = u"チョコレートプレス#プレスをチョコレートに"
COMPLETE_ASSIST_SKILL = u"コンプアシスト#消去に必要なブロック-1"
ROB_CARD_SKILL = u"ロブカード#攻撃時に相手のカード強奪"
PURIFY_SKILL = u"ピュリファイ#ジョーカーを削除"
DOUBLE_SPELL_SKILL = u"ダブルスペル#連続でアルカナ使用"
SOUL_EAT_SKILL = u"ソウルイート#サモン削除時にスター増加"
REVERSE_SORCERY_SKILL = u"リバースソーサリー#ソーサリー効果反転"
ANTI_SUMMONING_SKILL = u"アンチサモーニング#シールドでサモン封印"
POISON_SUMMON_SKILL = u"ポイズンサモン#召喚時に毒を付与"
FORCE_JOKER_SKILL = u"フォースジョーカー#*手札にジョーカー追加*"
SHEPHERD_SKILL = u"シェパード#"+BEAST_TRIBE+u"サモンコスト減少"
FALCONER_SKILL = u"ファルコナー#"+SKY_TRIBE+u"サモンコスト減少"
ALCHMIST_SKILL = u"アルケミスト#"+ALCHMIC_TRIBE+u"サモンコスト減少"
NECROMANCER_SKILL = u"ネクロマンサー#"+UNDEAD_TRIBE+u"サモンコスト減少"
DRAGON_MASTER_SKILL = u"ドラゴンマスター#"+DRAGON_TRIBE+u"サモンコスト減少"
HALF_JUPITER_SKILL = u"ハーフジュピター#木アルカナコスト減少"
HALF_MARS_SKILL = u"ハーフマーズ#火アルカナコスト減少"
HALF_SATURN_SKILL = u"ハーフサターン#土アルカナコスト減少"
HALF_VENUS_SKILL = u"ハーフヴェヌス#金アルカナコスト減少"
HALF_MERCURY_SKILL = u"ハーフメルクリー#水アルカナコスト減少"
MOON_CHILD_SKILL = u"ムーンチャイルド#月アルカナコスト減少"
SON_OF_SUN_SKILL = u"サンオブサン#太陽アルカナコスト減少"
VAMPIRE_SKILL = u"ヴァンピール#攻撃時に相手のスター吸収"
CONVERT_RESOURCE_SKILL = u"コンバートリソース#あふれたスターを変換"
SAFETY_SKILL = u"セーフティ#毒性ブロック効果防止"
TALISMAN_SKILL = u"タリスマン#ジョーカー減衰効果防止"
LIFE_BOOST_SKILL = u"ライフブースト#生命の欠片効果倍増"
MIGHTY_SKILL = u"マイティ#力の欠片効果倍増"
TOUGHNESS_SKILL = u"タフネス#守りの欠片効果倍増"
SPEEDSTER_SKILL = u"スピードスター#速さの欠片効果倍増"
SHORT_TURN_SKILL = u"ショートターン#持続効果間隔短縮"
SWORD_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=SWORD_CATEGORY)
WAND_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=WAND_CATEGORY)
HEAVY_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=HEAVY_CATEGORY)
MISSILE_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=MISSILE_CATEGORY)
HAT_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=HAT_CATEGORY)
HELMET_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=HELMET_CATEGORY)
ARMOR_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=ARMOR_CATEGORY)
ROBE_EQUIP_SKILL = u"{equip}装備#{equip}装備可能".format(equip=ROBE_CATEGORY)
# ---- Equip ----
VERY_LOW_CORRECTION = 0.2
LOW_CORRECTION = 0.5
MID_CORRECTION = 1.0
HIGH_CORRECTION = 1.2
VERY_HIGH_CORRECTION = 1.5
# ---- Star ----
JUPITER_EFFECT = "blue_line"
MARS_EFFECT = "red_fire"
SATURN_EFFECT = "purple_light"
VENUS_EFFECT = "yellow_line"
MERCURY_EFFECT = "blue_bubble"
MOON_EFFECT = "black_fire"
SUN_EFFECT = "yellow_light"
# ---- Ability ----
ENCHANT_ABILITY = "enchant"
PERSISTENCE_ABILITY = "persistence"
PREVENTION_ABILITY = "prevention"
ADDITION_ABILITY = "addition"
# ---- Block Name ----
BASIC_NAMES = "Normal#Solid#Adamant"
STAR_NAMES = "Jupiter#Mars#Saturn#Venus#Mercury#Moon#Sun"
SHARD_NAMES = "Life#Power#Protect#Speed"
KEY_NAMES = "BronzeKey#SilverKey#GoldKey"
CHEST_NAMES = "IronChest#BronzeChest#SilverChest#GoldChest"
CARD_NAMES = "Summon#Sorcery#Shield#Support"
LEVEL_UP_NAMES = "HardnessDown#LuckUp"
BAD_LEVEL_UP_NAMES = "HardnessUp#LuckDown"
ITEM_NAMES = str(
    STAR_NAMES+"#"+SHARD_NAMES+"#" +
    KEY_NAMES+"#"+CHEST_NAMES+"#"+CARD_NAMES)
SLIME_NAMES = "Slime#Tired"
IRREGULAR_NAMES = "Ruined#Magma#Ice#Matango#Acid#Poison#Stone"
DEMON_NAMES = "Gargoyle#BlockEater#BlockDemon#ArchDemon"
GHOST_NAMES = "RIP#FireGhost#IceGhost#PoisonGhost"
MIMIC_NAMES = "BronzeMimic#SilverMimic#GoldMimic#PandoraMimic"
# ---- Change ----
MAGMA_CHANGE = "Magma##Normal"
ICE_CHANGE = "Ice##Normal#Solid"
STONE_CHANGE = "Stone##"+BASIC_NAMES
MATANGO_CHANGE = "Matango##"+BASIC_NAMES
ACID_CHANGE = "Acid##Normal#Solid"
POISON_CHANGE = "Poison##Normal#Jupiter#Mars#Venus#Mercury#Moon#Sun"
JUPITER_CHANGE = "Jupiter##"+BASIC_NAMES
MARS_CHANGE = "Mars##"+BASIC_NAMES
SATURN_CHANGE = "Saturn##"+BASIC_NAMES
VENUS_CHANGE = "Venus##"+BASIC_NAMES
MERCURY_CHANGE = "Mercury##"+BASIC_NAMES
MOON_CHANGE = "Moon##"+BASIC_NAMES
SUN_CHANGE = "Sun##"+BASIC_NAMES
LIFE_CHANGE = "Life##"+BASIC_NAMES
POWER_CHANGE = "Power##"+BASIC_NAMES
PROTECT_CHANGE = "Protect##"+BASIC_NAMES
SPEED_CHANGE = "Speed##"+BASIC_NAMES
SLIME_CHANGE = "Slime##"+BASIC_NAMES
BLOCK_EATER_CHANGE = "BlockEater##Normal"
# ---- Flag ----
FORCE_CRACK = 0b1
UNLOCK_CRACK = 0b10
TREASURE_CRACK = 0b100
FIRE_EATER_CRACK = 0b1000
ICE_PICKER_CRACK = 0b10000
ACID_ERASER_CRACK = 0b100000
STONE_BREAKER_CRACK = 0b1000000
POWER_CRACK = 0b10000000
EXORCIST_CRACK = 0b100000000
# ---- Cell ----
SINGLE_SCORE = 100
HALF_SCORE = SINGLE_SCORE >> 1
QUARTER_SCORE = SINGLE_SCORE >> 2
DOUBLE_SCORE = SINGLE_SCORE << 1
LOW_MALIGNANCY = 1
MID_MALIGNANCY = LOW_MALIGNANCY << 1
HIGH_MALIGNANCY = LOW_MALIGNANCY << 2
WHITE_TARGET_NUMBER = 0
RED_TARGET_NUMBER = 1
ORANGE_TARGET_NUMBER = 2
YELLOW_TARGET_NUMBER = 3
GREEN_TARGET_NUMBER = 4
CYAN_TARGET_NUMBER = 5
BLUE_TARGET_NUMBER = 6
MAGENTA_TARGET_NUMBER = 7
# ---- Piece ----
SINGLE_PRUNING = 0
HALF_PRUNING = 1
QUARTER_PRUNING = 2
CENTER = 0, 0
UP = 0, -1
RIGHT = 1, 0
DOWN = 0, 1
LEFT = -1, 0
UP_RIGHT = 1, -1
UP_LEFT = -1, -1
DOWN_RIGHT = 1, 1
DOWN_LEFT = -1, 1
A0 = 0
A90 = 1
A180 = 2
A270 = 3
UNROTATABLE = 0
ROTATABLE = 1
FLEXIBLE = 2
SHIFTED = 3
# ---- Command ----
EXIT_COMMAND = "."
UP_COMMAND = "W"
LEFT_COMMAND = "A"
RIGHT_COMMAND = "D"
DOWN_COMMAND = "S"
DECISION_COMMAND = "!"
CANCEL_COMMAND = "?"
HOLD_COMMAND = "&"
REMOVE_COMMAND = "|"
DELETE_COMMAND = "-"
USE_COMMAND = "+"
SELECT_COMMAND = "$"
START_COMMAND = "%"
USE1_COMMAND = "1"
USE2_COMMAND = "2"
USE3_COMMAND = "3"
USE4_COMMAND = "4"
USE5_COMMAND = "5"
USE6_COMMAND = "6"
USE7_COMMAND = "7"
USE8_COMMAND = "8"
VOLUMEUP_COMMAND = ">"
VOLUMEDOWN_COMMAND = "<"
MUTE_COMMAND = "_"
# ---- Color ----
WHITE = "0xFFFFFF"
GRAY = "0x808080"
BLACK = "0x101010"
RED = "0xFF0000"
ORANGE = "0xFF8000"
YELLOW = "0xFFFF00"
YELLOW_GREEN = "0x80FF00"
GREEN = "0x00FF00"
VIRIDIAN = "0x00FF80"
GREEN_BLUE = "0x0080FF"
CYAN = "0x00FFFF"
BLUE = "0x0000FF"
PURPLE = "0x8000FF"
MAGENTA = "0xFF00FF"
DARK_RED = "0x800000"
DARK_ORANGE = "0x804000"
DARK_YELLOW = "0x808000"
DARK_YELLOW_GREEN = "0x408000"
DARK_GREEN = "0x008000"
DARK_GREEN_BLUE = "0x008040"
DARK_VIRIDIAN = "0x008040"
DARK_CYAN = "0x008080"
DARK_BLUE = "0x000080"
DARK_MAGENTA = "0x800080"
RAINBOW = (
    DARK_RED, DARK_ORANGE, DARK_YELLOW, DARK_GREEN,
    DARK_CYAN, DARK_BLUE, DARK_MAGENTA, DARK_MAGENTA)
BURNING = RED, ORANGE, YELLOW, GREEN, YELLOW, ORANGE, RED, PURPLE
# ---- Debug ----
IS_OUTPUT = False
PIECE_TEST = ""
