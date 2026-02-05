import random
import csv
from datetime import datetime


# ===============================
# かんたん翻訳ヘルパ（最低限）
# ===============================
TEXT = {
    "ACT1": "培地設計",
    "ACT2": "衛生巡回",
    "ACT3": "菌糸ネットワーク探索",
    "ACT4": "業務終了",
    "P3": "まいたけ",
    "MONEY_LABEL": "¥",
}


def t(key):
    return TEXT.get(key, key)


def money_fmt(x):
    return f"{x:,}"


# ===============================
# Logger
# ===============================
class GameLogger:
    def __init__(self, filepath="run_log.csv"):
        self.filepath = filepath
        self.fieldnames = ["timestamp", "day", "action", "hp", "mp", "money"]

        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def log(self, day, player, facility, action="", event=""):
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "day": day,
            "action": action,
            "hp": player.HP,
            "mp": player.MP,
            "money": player.money,
        }
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)


# ===============================
# Facility
# ===============================
class Facility:
    def __init__(self):
        self.name = "しいたけファーム"
        self.pfas_level = 10

    def display_info(self):
        print(f"胞子汚染度: {self.pfas_level}")

    def check_for_event(self):
        if self.pfas_level > 50:
            return "SPORE_CRISIS"
        return None


# ===============================
# Player
# ===============================
class Player:
    def __init__(self):
        self.name = t("P3")
        self.HP = 100
        self.MP = 50
        self.money = 0

    def display_status(self):
        print(f"HP:{self.HP} MP:{self.MP} 収支:{self.money}")

    def do_menu_planning(self, facility):
        self.money += 1000
        self.MP -= 3

    def do_hygiene_check(self, facility):
        facility.pfas_level -= 5
        self.MP -= 3

    def do_special_trip(self, day):
        self.MP -= 5


# ===============================
# レポート生成
# ===============================
def generate_reports(_):
    print("レポート生成完了")


# ===============================
# メインゲーム
# ===============================
def start_game():
    logger = GameLogger()
    player = Player()
    facility = Facility()

    day = 1

    logger.log(day, player, facility, action="start_game")

    while player.HP > 0 and player.MP > 0 and day <= 10:
        print(f"\n--- DAY {day} ---")
        player.display_status()
        facility.display_info()

        print("\n--- 今日の行動を選択してください ---")
        print(f"1: {t('ACT1')}")
        print(f"2: {t('ACT2')}")
        print(f"3: {t('ACT3')}")
        print(f"4: {t('ACT4')}")

        choice = input("番号を入力: ")

        if choice == "1":
            player.do_menu_planning(facility)
            logger.log(day, player, facility, action="culture_planning")

        elif choice == "2":
            player.do_hygiene_check(facility)
            logger.log(day, player, facility, action="hygiene_patrol")

        elif choice == "3":
            player.do_special_trip(day)
            logger.log(day, player, facility, action="mycelium_trip")

        elif choice == "4":
            print("業務終了")
            logger.log(day, player, facility, action="end_day")
            day += 1
            continue

        else:
            print("無効な入力")

        day += 1

    generate_reports("run_log.csv")


# ===============================
# 起動スイッチ（超重要）
# ===============================
if __name__ == "__main__":
    start_game()
