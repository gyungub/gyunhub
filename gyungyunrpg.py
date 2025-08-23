import random
import time

# =============== 아스키 아트 ===============
ASCII_TITLE = r"""
██████╗ ██████╗  ██████╗      ██████╗ ██████╗  ██████╗
██╔══██╗██╔══██╗██╔════╝     ██╔════╝ ██╔══██╗██╔════╝
██████╔╝██████╔╝██║  ███╗    ██║  ███╗██████╔╝██║  ███╗
██╔═══╝ ██╔══██╗██║   ██║    ██║   ██║██╔══██╗██║   ██║
██║     ██║  ██║╚██████╔╝    ╚██████╔╝██║  ██║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
"""

ASCII_GYUN = r"""
         .-.
        (o o)   균
        | O \
         \   \
          `~~~'
"""

ASCII_TOWN = r"""
  ~ 마   을 ~
 [상점] [대장간] [여관] [퀘스트] [도박장] [사냥터] [던전]
"""

ASCII_DUNGEON = r"""
   ____    _   _   _   _   ____   _   _   _____   _   _
  |  _ \  | | | | | \ | | / __ \ | \ | | |_   _| | \ | |
  | | | | | | | | |  \| || |  | ||  \| |   | |   |  \| |
  | | | | | | | | | . ` || |  | || . ` |   | |   | . ` |
  | |_| | | |_| | | |\  || |__| || |\  |  _| |_  | |\  |
  |____/   \___/  |_| \_| \____/ |_| \_| |_____| |_| \_|
"""

ASCII_MON = {
    "슬라임": r"( •_•)  ~미끈미끈~",
    "고블린": r"/\_/\  (•̀ᴗ•́)و ̑̑  칼을 휘두른다!",
    "늑대": r"ᘛ⁐̤ᕐᐷ  아우우웅!",
    "오우거": r"(ง'̀-'́)ง  우르르!",
    "해골병사": r"☠  달그락…",
    "마법사": r"(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "리치": r"(◣_◢)  영혼을 수확하리라",
    "키메라": r"🦁+🐐+🐍  으르렁!",
    "악마": r"( ⚈̥̥̥̥̥́‸⚈̥̥̥̥̥́) 🔥",
    "드래곤": r"🐉🔥  포효한다!"
}

# =============== 전역 게임 데이터 ===============
MAX_LEVEL = 100

player = {
    "name": "용사",
    "job": None,
    "level": 1,
    "exp": 0,
    "hp": 100, "max_hp": 100,
    "mp": 50,  "max_mp": 50,
    "atk": 10, "def": 5, "spd": 5,
    "gold": 500,
    "stat_points": 0,
    "weapon": {"name": "낡은 검", "atk": 5, "tier": 0},
    "armor":  {"name": "천 옷",   "def": 2, "tier": 0},
    "accessory": None,
    "inventory": {"포션": 3, "에테르": 1},
    "bestiary": set(),         # 처치한 몬스터 이름 기록
    "bleed": 0                 # 출혈 피해 남은 턴
}

jobs = {
    "전사": {"hp": 40, "mp": 0,  "atk": 5, "def": 8, "spd": 0,
             "skills": {"방패막기": {"mp": 5, "type": "guard", "desc": "이번 턴 받는 피해 -50%"},
                        "분노의일격": {"mp": 10, "type": "strike", "power": 2.0, "desc": "강력한 일격(공*2)!"}}},
    "마법사": {"hp": 10, "mp": 40, "atk": 3, "def": 0, "spd": 0,
             "skills": {"파이어볼": {"mp": 12, "type": "magic", "power": 2.2, "desc": "불덩이 투척!"},
                        "힐":      {"mp": 10, "type": "heal",  "power": 0.5, "desc": "최대체력의 50% 회복"}}},
    "도적": {"hp": 20, "mp": 10, "atk": 4, "def": 2, "spd": 8,
             "skills": {"이중타":  {"mp": 8,  "type": "multi", "hits": 2, "power": 1.1, "desc": "두 번 베기"},
                        "출혈독":  {"mp": 10, "type": "bleed","stacks": 3, "desc": "3턴간 출혈(소량 고정 피해)"}}}
}

# 던전 1~10 층 고정 몬스터(중복 없음)
DUNGEON_TABLE = {
    1: {"name": "슬라임", "hp": 60, "atk": 10, "def": 2, "spd": 3, "gold": 80,  "exp": 80},
    2: {"name": "고블린", "hp": 90, "atk": 18, "def": 5, "spd": 6, "gold": 120, "exp": 120},
    3: {"name": "늑대",   "hp": 120,"atk": 22, "def": 7, "spd": 10,"gold": 160, "exp": 160},
    4: {"name": "오우거", "hp": 160,"atk": 28, "def": 10,"spd": 4, "gold": 200, "exp": 200},
    5: {"name": "해골병사","hp": 200,"atk": 35, "def": 14,"spd": 8, "gold": 260, "exp": 260},
    6: {"name": "마법사", "hp": 230,"atk": 42, "def": 16,"spd": 9, "gold": 320, "exp": 320},
    7: {"name": "리치",   "hp": 270,"atk": 48, "def": 20,"spd": 11,"gold": 380, "exp": 380},
    8: {"name": "키메라", "hp": 320,"atk": 55, "def": 24,"spd": 12,"gold": 450, "exp": 450},
    9: {"name": "악마",   "hp": 380,"atk": 62, "def": 28,"spd": 13,"gold": 520, "exp": 520},
   10: {"name": "드래곤", "hp": 600,"atk": 80, "def": 35,"spd": 15,"gold": 1200,"exp": 1200, "boss": True}
}

# 사냥터(필드) 레벨 구간 -> 몬스터 풀(랜덤)
FIELDS = {
    (1, 10):  [
        {"name": "야생슬라임", "hp": 35, "atk": 8,  "def": 2, "spd": 3, "gold": 30, "exp": 30},
        {"name": "숲토끼",   "hp": 30, "atk": 9,  "def": 1, "spd": 5, "gold": 28, "exp": 28}
    ],
    (11, 20): [
        {"name": "사막도마뱀", "hp": 70, "atk": 15, "def": 4, "spd": 6, "gold": 50, "exp": 55},
        {"name": "모래고블린","hp": 80, "atk": 16, "def": 5, "spd": 6, "gold": 55, "exp": 60}
    ],
    (21, 30): [
        {"name": "설산늑대", "hp": 110, "atk": 22, "def": 7, "spd": 8, "gold": 90, "exp": 95},
        {"name": "빙정정령","hp": 130, "atk": 20, "def": 10,"spd": 7, "gold": 100,"exp": 110}
    ],
    (31, 50): [
        {"name": "오우거전사", "hp": 170, "atk": 30,"def": 12,"spd": 6, "gold": 150,"exp": 160},
        {"name": "망령",     "hp": 150, "atk": 28,"def": 10,"spd": 12,"gold": 160,"exp": 170}
    ],
    (51, 100): [
        {"name": "지옥개",   "hp": 260,"atk": 50,"def": 20,"spd": 14,"gold": 260,"exp": 300},
        {"name": "암흑기사", "hp": 320,"atk": 56,"def": 24,"spd": 12,"gold": 320,"exp": 360}
    ]
}

WEAPON_SHOP = [
    {"name": "철검",   "atk": 15, "tier": 1, "price": 600},
    {"name": "강철검", "atk": 25, "tier": 2, "price": 1500},
    {"name": "마법검", "atk": 40, "tier": 3, "price": 4000},
    {"name": "용의검", "atk": 65, "tier": 4, "price": 12000},
]

ARMOR_SHOP = [
    {"name": "가죽갑옷", "def": 10, "tier": 1, "price": 600},
    {"name": "강철갑옷", "def": 18, "tier": 2, "price": 1500},
    {"name": "마법갑옷", "def": 28, "tier": 3, "price": 4000},
    {"name": "용비늘갑주", "def": 45, "tier": 4, "price": 12000},
]

# =============== 유틸 ===============
def clamp(v, lo, hi): return max(lo, min(hi, v))

def show_status():
    print(ASCII_GYUN)
    print(f"[{player['name']}] 직업:{player['job']}  Lv.{player['level']}  EXP:{player['exp']}/{player['level']*100 if player['level']<MAX_LEVEL else '—'}")
    print(f"HP {player['hp']}/{player['max_hp']}   MP {player['mp']}/{player['max_mp']}")
    print(f"공:{player['atk']}(+{player['weapon']['atk']})  방:{player['def']}(+{player['armor']['def']})  속:{player['spd']}")
    print(f"무기:{player['weapon']['name']}  갑옷:{player['armor']['name']}  골드:{player['gold']}  스탯포인트:{player['stat_points']}")
    print(f"인벤토리: {player['inventory']}")
    print("-"*60)

def gain_exp(amount):
    if player["level"] >= MAX_LEVEL: return
    player["exp"] += amount
    while player["level"] < MAX_LEVEL and player["exp"] >= player["level"]*100:
        player["exp"] -= player["level"]*100
        player["level"] += 1
        # 자동 성장치
        player["max_hp"] += 25
        player["max_mp"] += 8
        player["atk"] += 4
        player["def"] += 3
        player["spd"] += 1
        player["stat_points"] += 3
        player["hp"] = player["max_hp"]
        player["mp"] = player["max_mp"]
        print(f"🎉 레벨업! 현재 레벨 {player['level']} (스탯 포인트 +3)")
        if player["level"] == MAX_LEVEL:
            player["exp"] = 0
            print("💯 최대 레벨 달성! 이제 드래곤도 울고 갑니다.")

def allocate_stats():
    if player["stat_points"] <= 0:
        print("분배할 포인트가 없습니다.")
        return
    print("분배할 스탯을 선택하세요: (hp/mp/atk/def/spd), 종료는 stop")
    while player["stat_points"] > 0:
        print(f"남은 포인트: {player['stat_points']}")
        s = input("> ").strip().lower()
        if s == "stop": break
        if s not in ["hp", "mp", "atk", "def", "spd"]:
            print("hp/mp/atk/def/spd 중 선택")
            continue
        player["stat_points"] -= 1
        if s == "hp":  player["max_hp"] += 10
        if s == "mp":  player["max_mp"] += 5
        if s == "atk": player["atk"] += 2
        if s == "def": player["def"] += 2
        if s == "spd": player["spd"] += 1
        print(f"{s} 상승! 현재: HP{player['max_hp']} MP{player['max_mp']} 공{player['atk']} 방{player['def']} 속{player['spd']}")
    player["hp"] = clamp(player["hp"], 0, player["max_hp"])
    player["mp"] = clamp(player["mp"], 0, player["max_mp"])

# =============== 전투 시스템 ===============
def calc_player_attack():
    return player["atk"] + player["weapon"]["atk"]

def calc_player_defense():
    return player["def"] + player["armor"]["def"]

def use_skill(mon, guard_state):
    skills = jobs[player["job"]]["skills"]
    names = list(skills.keys())
    for i, k in enumerate(names, 1):
        d = skills[k]
        print(f"{i}) {k} - MP {d['mp']} : {d['desc']}")
    sel = input("스킬 선택(취소:0): ").strip()
    if not sel.isdigit() or int(sel) < 1 or int(sel) > len(names):
        print("스킬 취소")
        return 0, guard_state, None
    key = names[int(sel)-1]
    data = skills[key]
    if player["mp"] < data["mp"]:
        print("마나 부족!")
        return 0, guard_state, None
    player["mp"] -= data["mp"]

    dmg = 0
    effect = None
    if data["type"] == "strike":
        dmg = max(int(calc_player_attack()*data["power"]) - mon["def"], 0)
    elif data["type"] == "magic":
        dmg = max(int((player["atk"]*0.8 + player["weapon"]["atk"]*0.7)*data["power"]) - int(mon["def"]*0.6), 0)
    elif data["type"] == "heal":
        heal = int(player["max_hp"]*data["power"])
        player["hp"] = clamp(player["hp"]+heal, 0, player["max_hp"])
        print(f"✨ 힐! HP {heal} 회복 (현재 {player['hp']}/{player['max_hp']})")
    elif data["type"] == "multi":
        hits = data["hits"]
        total = 0
        for _ in range(hits):
            hit = max(int(calc_player_attack()*data["power"]) - mon["def"], 0)
            total += hit
        dmg = total
    elif data["type"] == "guard":
        guard_state = True
        print("🛡️ 방패막기 자세! 이번 턴 받는 피해 감소")
    elif data["type"] == "bleed":
        effect = ("bleed", data["stacks"])
        print("🩸 출혈 독을 묻혔다! (3턴)")

    if dmg > 0:
        print(f"스킬 피해 {dmg}!")
    return dmg, guard_state, effect

def try_flee(boss=False):
    if boss:
        print("보스 전투에서는 도망칠 수 없습니다!")
        return False
    chance = 0.45 + (player["spd"] - 5) * 0.02
    if random.random() < chance:
        print("도망 성공!")
        return True
    print("도망 실패!")
    return False

def battle(mon, boss=False):
    print(ASCII_MON.get(mon["name"], ""))
    print(f"⚔️ {mon['name']} 이(가) 나타났다!  (HP {mon['hp']})")
    php = player["hp"]
    m = {"name": mon["name"], "hp": mon["hp"], "atk": mon["atk"], "def": mon["def"], "spd": mon["spd"]}
    guard_state = False
    bleed_turns_on_mon = 0

    while m["hp"] > 0 and player["hp"] > 0:
        print(f"\n당신 HP {player['hp']}/{player['max_hp']}  MP {player['mp']}/{player['max_mp']}  |  {m['name']} HP {m['hp']}")
        print("1)공격  2)스킬  3)아이템  4)도망")
        act = input("> ").strip()

        # 선/후공: 속도 비교
        player_first = player["spd"] >= m["spd"]
        turns = [("player", act), ("monster", None)] if player_first else [("monster", None), ("player", act)]

        # 턴 처리
        for who, a in turns:
            if who == "player":
                if a == "1":
                    dmg = max(calc_player_attack() - m["def"], 0)
                    m["hp"] -= dmg
                    print(f"👊 공격! {m['name']}에게 {dmg} 피해.")
                elif a == "2":
                    dmg, guard_state, effect = use_skill(m, guard_state)
                    m["hp"] -= dmg
                    if effect and effect[0] == "bleed":
                        bleed_turns_on_mon = effect[1]
                elif a == "3":
                    use_item_in_battle()
                elif a == "4":
                    if try_flee(boss=boss):
                        return "flee"
                else:
                    print("잘못 입력!")
            else:
                if m["hp"] <= 0:
                    continue
                # 몬스터 공격
                base = m["atk"]
                dmg = max(base - calc_player_defense(), 0)
                if guard_state: dmg = dmg // 2
                player["hp"] -= dmg
                print(f"💢 {m['name']}의 공격! {dmg} 피해.")
        guard_state = False

        # 출혈 도트 (몬스터에게)
        if bleed_turns_on_mon > 0 and m["hp"] > 0:
            dot = max(5, m["hp"]//20)
            m["hp"] -= dot
            bleed_turns_on_mon -= 1
            print(f"🩸 출혈로 {dot} 지속 피해!")

    if player["hp"] <= 0:
        print("💀 쓰러졌다… 마을로 돌아간다.")
        player["hp"] = player["max_hp"]
        return "lose"

    # 승리
    print(f"✅ {m['name']} 격파!")
    player["bestiary"].add(m["name"])
    drop_and_reward(mon)
    return "win"

def use_item_in_battle():
    inv = player["inventory"]
    print(f"인벤토리: {inv}")
    print("사용할 아이템을 입력(포션/에테르, 취소: 엔터)")
    k = input("> ").strip()
    if k == "포션" and inv.get("포션", 0) > 0:
        inv["포션"] -= 1
        heal = 80
        player["hp"] = clamp(player["hp"]+heal, 0, player["max_hp"])
        print(f"포션 사용! HP +{heal}")
    elif k == "에테르" and inv.get("에테르", 0) > 0:
        inv["에테르"] -= 1
        mana = 40
        player["mp"] = clamp(player["mp"]+mana, 0, player["max_mp"])
        print(f"에테르 사용! MP +{mana}")
    elif k == "":
        print("아이템 사용 취소")
    else:
        print("해당 아이템이 없거나 잘못 입력")

def drop_and_reward(mon):
    gold = mon["gold"]
    exp  = mon["exp"]
    player["gold"] += gold
    gain_exp(exp)
    print(f"💰 골드 +{gold}, 📚 경험치 +{exp}")
    # 드랍
    if random.random() < 0.25:
        player["inventory"]["포션"] = player["inventory"].get("포션", 0) + 1
        print("🎁 드랍: 포션 +1")
    if random.random() < 0.15:
        player["inventory"]["에테르"] = player["inventory"].get("에테르", 0) + 1
        print("🎁 드랍: 에테르 +1")

# =============== 마을 컨텐츠 ===============
def shop():
    print("\n🏪 상점")
    while True:
        print("1) 포션(50골드)  2) 에테르(120골드)  3) 무기 구매  4) 갑옷 구매  5) 나가기")
        c = input("> ")
        if c == "1":
            if buy_cost(50): add_item("포션", 1); print("포션 구매!")
        elif c == "2":
            if buy_cost(120): add_item("에테르", 1); print("에테르 구매!")
        elif c == "3":
            buy_weapon()
        elif c == "4":
            buy_armor()
        elif c == "5":
            break
        else:
            print("잘못 입력")

def buy_cost(cost):
    if player["gold"] < cost:
        print("골드 부족!")
        return False
    player["gold"] -= cost
    return True

def add_item(name, n):
    player["inventory"][name] = player["inventory"].get(name, 0) + n

def buy_weapon():
    print("⚔️ 무기 목록:")
    for i, w in enumerate(WEAPON_SHOP, 1):
        print(f"{i}) {w['name']}  공+{w['atk']}  {w['price']}G")
    sel = input("번호(취소:엔터): ").strip()
    if not sel: return
    i = int(sel)-1
    w = WEAPON_SHOP[i]
    if player["gold"] >= w["price"]:
        player["gold"] -= w["price"]
        player["weapon"] = {"name": w["name"], "atk": w["atk"], "tier": w["tier"]}
        print(f"{w['name']} 구매 완료!")
    else:
        print("골드 부족!")

def buy_armor():
    print("🛡️ 갑옷 목록:")
    for i, a in enumerate(ARMOR_SHOP, 1):
        print(f"{i}) {a['name']}  방+{a['def']}  {a['price']}G")
    sel = input("번호(취소:엔터): ").strip()
    if not sel: return
    i = int(sel)-1
    a = ARMOR_SHOP[i]
    if player["gold"] >= a["price"]:
        player["gold"] -= a["price"]
        player["armor"] = {"name": a["name"], "def": a["def"], "tier": a["tier"]}
        print(f"{a['name']} 구매 완료!")
    else:
        print("골드 부족!")

def smithy():
    print("\n⚒️ 대장간 (강화 1회 300G: 무기 공+3 / 방어구 방+3)")
    while True:
        print("1) 무기 강화  2) 방어구 강화  3) 나가기")
        c = input("> ")
        if c == "1":
            if buy_cost(300):
                player["weapon"]["atk"] += 3
                print("무기 강화! 현재 무기공:", player["weapon"]["atk"])
        elif c == "2":
            if buy_cost(300):
                player["armor"]["def"] += 3
                print("방어구 강화! 현재 방어:", player["armor"]["def"])
        elif c == "3":
            break
        else:
            print("잘못 입력")

def inn():
    print("\n💤 여관에 묵었습니다. HP/MP 완전 회복!")
    player["hp"] = player["max_hp"]
    player["mp"] = player["max_mp"]

def quest_board():
    print("\n📜 퀘스트 게시판")
    print(" - [반복] 슬라임 1마리 처치 → 80G")
    print(" - [특수] 던전 5층 클리어 → 1000G")
    s = input("완료한 퀘스트가 있나요? (slime/d5/없음): ").strip().lower()
    if s == "slime" and "슬라임" in player["bestiary"]:
        player["gold"] += 80
        print("보상 80G 수령!")
    elif s == "d5" and "해골병사" in player["bestiary"]:
        player["gold"] += 1000
        print("보상 1000G 수령!")
    else:
        print("완료 조건을 충족하지 않았거나 잘못 입력")

def casino():
    print("\n🎲 도박장 - 주사위(배당 2배, 승률 45%)")
    bet = input("베팅할 골드(0=취소): ").strip()
    if not bet or not bet.isdigit(): return
    bet = int(bet)
    if bet <= 0 or bet > player["gold"]:
        print("베팅 불가")
        return
    player["gold"] -= bet
    if random.random() < 0.45:
        win = bet*2
        player["gold"] += win
        print(f"승리! +{win}G")
    else:
        print("패배…")

# =============== 사냥터 & 던전 ===============
def choose_field():
    lv = player["level"]
    pools = []
    for (lo, hi), mons in FIELDS.items():
        if lo <= lv <= hi: pools = mons
    if not pools:
        # 레벨이 높을수록 상위 필드 사용
        pools = FIELDS[max(FIELDS, key=lambda k: k[1])]
    print("\n🌲 사냥터: 랜덤 조우 시작!")
    mon = dict(random.choice(pools))  # copy
    print(f"[필드] {mon['name']} 조우!")
    battle(mon)

def enter_dungeon():
    print(ASCII_DUNGEON)
    try:
        d = int(input("입장할 던전 난이도(1~10): "))
    except:
        print("잘못 입력")
        return
    if d < 1 or d > 10:
        print("범위 밖")
        return

    # 난이도 2 이상은 기본 무기로 클리어 불가 → 입장 제한(강화/구매 요구)
    if d >= 2 and player["weapon"]["atk"] <= 10:
        print("⚠️ 무기가 너무 허접합니다… 대장간에서 강화하거나 상점에서 새 무기를 사세요.")
        return

    mon = dict(DUNGEON_TABLE[d])  # copy
    boss = mon.get("boss", False)
    res = battle(mon, boss=boss)
    if boss and res == "win":
        print("🎉 최종 보스 격파! 전설이 되었다…")

# =============== 시작/튜토리얼 ===============
def prologue():
    print(ASCII_TITLE)
    print("이 세계는 자원과 검술, 그리고 마법으로 유지됩니다.")
    print("당신은 떠오르는 모험가 ‘균’. 최종 목표는 난이도 10의 던전에서 드래곤을 토벌하는 것!")
    start = input("게임을 시작하시겠습니까? (yes/no): ").strip().lower()
    if start != "yes":
        print("안녕히 가세요!")
        return False
    name = input("당신의 이름은? (엔터=용사): ").strip()
    if name: player["name"] = name

    # 직업 선택
    print("\n직업을 선택하세요: 전사 / 마법사 / 도적")
    job = input("> ").strip()
    if job not in jobs: job = "전사"
    player["job"] = job
    jb = jobs[job]
    player["max_hp"] += jb["hp"]; player["hp"] = player["max_hp"]
    player["max_mp"] += jb["mp"]; player["mp"] = player["max_mp"]
    player["atk"] += jb["atk"];   player["def"] += jb["def"];  player["spd"] += jb["spd"]
    print(f"{job} 선택! 시작 스탯이 조정되었습니다.")

    print("\n[튜토리얼] 연습용 슬라임이 나타났다!")
    mon = {"name": "슬라임", "hp": 35, "atk": 6, "def": 1, "spd": 2, "gold": 20, "exp": 30}
    battle(mon)
    return True

# =============== 메인 루프 ===============
def main_menu():
    while True:
        show_status()
        print(ASCII_TOWN)
        print("1)상태/스탯분배  2)상점  3)대장간  4)여관  5)퀘스트  6)도박장  7)사냥터  8)던전  9)도감  0)종료")
        c = input("> ").strip()
        if c == "1":
            show_status()
            sub = input("스탯 분배 하시겠습니까? (yes/no): ").strip().lower()
            if sub == "yes": allocate_stats()
        elif c == "2":
            shop()
        elif c == "3":
            smithy()
        elif c == "4":
            inn()
        elif c == "5":
            quest_board()
        elif c == "6":
            casino()
        elif c == "7":
            choose_field()
        elif c == "8":
            enter_dungeon()
        elif c == "9":
            print("📖 도감:", ", ".join(sorted(player["bestiary"])) or "비어 있음")
        elif c == "0":
            print("게임 종료!")
            break
        else:
            print("잘못 입력")

if __name__ == "__main__":
    if prologue():
        main_menu()
