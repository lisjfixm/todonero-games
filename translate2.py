#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Precise Chinese translation for todonero game shelf."""
import re, os, glob

SITE = '/home/user/Doubao/chats/38451458306244866/todonero/site'
os.chdir(SITE)

# ============ 1. Index page: hero text + game cards ============
html = open('index.html', encoding='utf-8').read()

# Hero title
html = html.replace('トドネロのゲーム置き場', 'トドネロ遊戲場')

# Hero subtitle / intro
html = html.replace('ブラウザで遊べる', '瀏覽器直接玩')
html = html.replace('ミニゲーム置き場', '小遊戲合集')
html = html.replace(
    'パズル、アクション、対戦、触って楽しむおもちゃまで、ブラウザですぐ遊べるミニゲームを公開しています。インストールや登録は不要で、スマートフォンでも PC でも遊べます。新しいゲームも順に追加しています。',
    '解謎、動作、對戰、各種互動玩具，瀏覽器直接開玩。免安裝免註冊，手機電腦都能玩。持續更新新遊戲。'
)

# Game title + desc translations (by href)
GAMES = {
    'games/10000-bowling/index.html': ('1萬瓶保齡球', '兩球打倒一萬根瓶的保齡球'),
    'games/Moji-Avoid/index.html': ('文字閃避大作戰', '輸入文字當自己，閃避子彈'),
    'games/acrobatic-train/index.html': ('特技列車', '電車前後分開換乘'),
    'games/banjo-cat/index.html': ('斑鳩琴貓', '彈斑鳩琴貓就會跳出來'),
    'games/blitz-reversi/index.html': ('閃電黑白棋', '不輪流同時放子的黑白棋'),
    'games/blitz-tac-toe/index.html': ('閃電圈圈叉叉', '不輪流同時放的圈圈叉叉'),
    'games/burger-tower/index.html': ('漢堡塔', '彈起配料疊高漢堡'),
    'games/carpet-art/index.html': ('地毯藝術', '沿地毯描出花紋'),
    'games/chitei-lever/index.html': ('地底拉桿', '拉桿彈金幣潛到地下'),
    'games/circle-bounce/index.html': ('圓圈反彈', '轉輪接球的打磚塊'),
    'games/claw-draw-ufo/index.html': ('畫爪娃娃機', '畫個爪子夾奖品'),
    'games/colorful-bomb-sort/index.html': ('彩色炸彈分類', '把炸彈分到同色區域'),
    'games/crazy-windmill/index.html': ('瘋狂風車', '逃離風車手的恐怖迷宮'),
    'games/donut-maker-3d/index.html': ('甜甜圈製作3D', '畫形狀炸甜甜圈再裝飾'),
    'games/double-booking/index.html': ('時間表崩壞', '把會動的行程塞進空檔'),
    'games/draw-roll-race/index.html': ('塗鴉滾輪賽跑', '畫手腳滾著跑'),
    'games/draw-sumo/index.html': ('塗鴉相撲', '畫手腳把對手推出界'),
    'games/find-1px/index.html': ('找1像素', '計時找出藏在畫面裡的1像素'),
    'games/font-merge/index.html': ('字體合成', '同字體相吸養大的方塊消除'),
    'games/font-sort/index.html': ('字體分類', '落下文字依字體分類'),
    'games/giant-wall/index.html': ('巨牆遊戲', ''),
    'games/giraffe-fight/index.html': ('長頸鹿打架', '比長頸鹿脖子互撞'),
    'games/gori-or-not-gori/index.html': ('有沒有猩猩', '判斷讀音有沒有「ごり」'),
    'games/gori-power/index.html': ('猩猩力量', '找含「ごり」「うほ」的詞'),
    'games/homerun-derby/index.html': ('全壘打大賽', '打變化球比全壘打數'),
    'games/human-bey/index.html': ('人類陀螺', '擺姿勢的人當陀螺對戰'),
    'games/infinite-jako/index.html': ('無限小魚乾', '在小魚乾山裡找生物'),
    'games/inflation-hockey/index.html': ('膨脹曲棍球', '冰球不斷變多的曲棍球'),
    'games/jack-o-lantern-maker/index.html': ('南瓜燈製作', '雕刻南瓜擺門口'),
    'games/kaden-master/index.html': ('家電達人', '敲壞家電再修好的計時賽'),
    'games/kakomi-survivor/index.html': ('包圍倖存者', '用身體圍地面把人弄下去'),
    'games/katakana-barabara/index.html': ('片假名散亂', '從散亂片假名猜單字'),
    'games/lens-warp/index.html': ('扭曲透鏡', '放鏡頭扭曲照片的玩具'),
    'games/long-potato/index.html': ('螺旋薯條機', '把馬鈴薯切螺旋比長度'),
    'games/madori-drop/index.html': ('戶型掉落', '疊房間方塊比房租'),
    'games/mansion-simulator/index.html': ('豪宅模擬器', '把照片變豪宅廣告風格'),
    'games/mawasu-yatsu-simulator/index.html': ('旋轉那個模擬器', '轉石臼時速衝1000km'),
    'games/moji-kushiyaki/index.html': ('文字串燒', '把喜歡的字串起來炭火烤'),
    'games/no-hole-in/index.html': ('不進洞', '變成杯子擋高爾夫球'),
    'games/nobinobi-giraffe/index.html': ('伸長長頸鹿', '伸長鹿頸比高度'),
    'games/one-pixel-a-day/index.html': ('大家一起畫一格', '大家輪流一格一格畫的共享畫板'),
    'games/othellis/index.html': ('黑白棋 OTHELLIS', '翻轉消除的黑白棋方塊遊戲'),
    'games/paint_breakout_image/index.html': ('塗地對戰', '打磚塊搶地盤對戰'),
    'games/pattern-hacker/index.html': ('圖案解鎖', '推理破解隱藏圖案鎖'),
    'games/phone-flipper/index.html': ('翻手機', '開合摺疊手機前進'),
    'games/pointcloud-puzzle/index.html': ('點雲拼圖', '轉點群找出畫面'),
    'games/prefecture-derby/index.html': ('都道府縣賽馬', '猜支出最高都道府縣的賽馬遊戲'),
    'games/rakugaki-fighter/index.html': ('塗鴉戰士', '畫的塗鴉變3D對戰'),
    'games/serpentile/index.html': ('六邊形路線', '轉方塊把棋子趕出盤外'),
    'games/serpentile-climb/index.html': ('六邊形攀爬', '接方塊讓箭頭往上爬'),
    'games/serpentile-connect/index.html': ('六邊形連接', '轉方塊對齊邊色的拼圖'),
    'games/serpentile-point/index.html': ('六邊形引導', '用方塊引導箭頭收集金幣'),
    'games/shodo-simulator-3d/index.html': ('書道模擬器3D', '毛筆寫字評分'),
    'games/skystar/index.html': ('星空', '只靠噴射操縱噴射車'),
    'games/soft-poop-fall/index.html': ('大便圖鑑', '疊大便收集稀有品種'),
    'games/speed-cards/index.html': ('速度卡牌', '跟電腦比賽接龍速度'),
    'games/spinning-JP/index.html': ('47都道府縣對戰', '把都道府縣棋子彈出場外'),
    'games/star-hopper/star-hopper.html': ('跳星星', '在星星重力圈間跳躍'),
    'games/swing-master/index.html': ('鞦韆大師', '盪鞦韆盪到最遠'),
    'games/synthwave-stg/synthwave-stg.html': ('合成波射擊', '夕陽網格上飛的3D射擊'),
    'games/time-schedule-simulator/index.html': ('時間表模擬器', '停掉輪迴行程排一天計畫'),
    'games/tissue-rush/index.html': ('衛生紙衝鋒', '抽完50張衛生紙計時賽'),
    'games/toilet-paper-rush/index.html': ('捲筒衛生紙衝鋒', '抽完整捲衛生紙計時賽'),
    'games/tower-climb/tower-climb.html': ('爬塔', '跳踏板爬塔頂'),
    'games/train-time-attack/index.html': ('列車計時挑戰', '電車環狀線跑一圈計時賽'),
    'games/turkish-ice-cream-3d/index.html': ('土耳其冰淇淋3D', '躲過客人的土耳其冰淇淋老闆'),
    'games/typhoon-escape/index.html': ('颱風逃脫', '移動日本列島躲颱風'),
    'games/usb-simulator-3d/index.html': ('USB模擬器3D', '不讓USB插進來'),
    'games/waffle-maker-3d/index.html': ('鬆餅製作3D', '畫模具烤自己喜歡的形狀鬆餅'),
    'games/walk-the-dog/index.html': ('遛狗', '狗把主人甩出去'),
    'games/zipper-finger/index.html': ('拉鍊手指', '描一下照片出現拉鍊的玩具'),
}

def replace_card(m):
    card = m.group(0)
    href_m = re.search(r'href="([^"]+)"', card)
    if not href_m: return card
    href = href_m.group(1)
    if href not in GAMES: return card
    new_title, new_desc = GAMES[href]
    # Replace h2
    card = re.sub(r'(<h2>).*?(</h2>)', r'\g<1>' + new_title + r'\g<2>', card)
    # Replace desc (may not exist)
    if '<p class="desc">' in card:
        card = re.sub(r'(<p class="desc">).*?(</p>)', r'\g<1>' + new_desc + r'\g<2>', card)
    elif new_desc:
        # Insert desc after dir
        card = re.sub(r'(<p class="dir">[^<]*</p>)', r'\g<1><p class="desc">' + new_desc + r'</p>', card)
    return card

html = re.sub(r'<li class="game-card">.*?</li>', replace_card, html, flags=re.S)

open('index.html', 'w', encoding='utf-8').write(html)
print("index.html done")

# ============ 2. Game files: targeted UI string replacement ============
# Only replace known safe UI strings — NOT hrefs, NOT JS variables, NOT game content data
UI = {
    # Buttons / labels
    'スタート': '開始', 'スタート！': '開始！',
    'もう一度': '再來一次', 'もういちど': '再來一次', 'もういっかい': '再來一次',
    'もう一度押すと消えます': '再按一次取消',
    'クリア！': '過關！', 'クリア!': '過關！',
    'ゲームオーバー': '遊戲結束',
    '勝ち！': '獲勝！', '勝利！': '勝利！', '敗北…': '失敗…', '敗北': '失敗',
    '次へ': '下一個', '次のステージへ': '下一關', '次のレースへ': '下一場比賽',
    'タップで次へ': '點擊繼續', 'タップで閉じる': '點擊關閉',
    'タップでリスタート': '點擊重新開始',
    'クリック / タップでリトライ': '點擊／觸控重試',
    'Space でスタート': '按空格開始', 'Space でもう一度': '按空格再來一次',
    'スコア': '分數', 'タイム : ': '時間：',
    'ベスト更新！': '刷新紀錄！', 'ベスト更新': '刷新紀錄',
    '新記録！': '新紀錄！',
    '設定': '設定', '結果': '結果',
    '遊び方': '玩法', 'ルールと操作': '規則與操作',
    '読み込み中…': '載入中…', '読込中': '載入中',
    '読み込む': '讀取', '書き出す': '匯出',
    'シェア': '分享', 'Xでシェア': '分享到X', 'Xに投稿': '發文到X',
    '共有': '分享', '共有する': '分享',
    'コピーしました': '已複製',
    '削除': '刪除', '元に戻す': '還原',
    '残り': '剩餘',
    '効果音：ON': '音效：開', '効果音：OFF': '音效：關',
    '音：ON': '聲音：開', '音：OFF': '聲音：關',
    '左右反転 ON': '左右翻轉 開', '左右反転 OFF': '左右翻轉 關',
    '閉じる': '關閉', '戻る': '返回',
    # Game over / status
    '力尽きた': '力盡了',
    '防衛失敗': '防守失敗', '防衛成功': '防守成功',
    'まもなくスタートです': '即將開始',
    'まもなく発車': '即將發車',
    '脱出成功': '脫逃成功',
    '脱落！': '淘汰！',
    '連勝': '連勝', '連勝中': '連勝中',
    '優勝': '優勝', '決勝': '決賽', '準決勝': '準決賽',
    '1回戦': '第一輪', '2回戦': '第二輪', '3回戦': '第三輪', '4回戦': '第四輪',
    # Errors
    'エラー: ': '錯誤：',
    '読み込み中…': '載入中…',
    # Common game text
    'スコア ': '分數 ',
    'ハイスコア': '最高分',
    'もう一度': '再來一次',
    'ゲームを終わる': '結束遊戲',
    # Buttons
    'スタート': '開始',
    'リトライ': '重試',
    'つぎへ': '下一個',
    'つぎの試合へ': '下一場比賽',
    'やり直し': '重新開始',
    # Common phrases in games
    '押して': '按',
    'タップして': '點擊',
    'スワイプ': '滑動',
    'ドラッグ': '拖曳',
    '回す': '轉動',
    '引く': '拉',
    '上へ': '往上', '下へ': '往下',
    '右へ': '往右', '左へ': '往左',
    # Score / timer prefixes
    'スコア: ': '分數：',
    'タイム: ': '時間：',
    '最高': '最高', '最大': '最大',
    '自己ベスト更新！': '刷新個人最佳！',
    '自己ベスト更新': '刷新個人最佳',
    '新発見！': '新發現！',
    '見つけた！': '找到了！',
    # Footer / misc
    'ホームページ': '首頁',
    'ゲームセンター': '遊戲中心',
}

# Sort by length descending
items = sorted(UI.items(), key=lambda x: -len(x[0]))

game_files = glob.glob('games/*/index.html') + glob.glob('games/*/*.html') + ['common/js/howto.js']
changed = 0
for f in game_files:
    try:
        orig = open(f, encoding='utf-8').read()
    except: continue
    new = orig
    for jp, zh in items:
        if jp in new:
            new = new.replace(jp, zh)
    if new != orig:
        open(f, 'w', encoding='utf-8').write(new)
        changed += 1

print(f"Game files translated: {changed}/{len(game_files)}")
