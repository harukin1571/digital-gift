import streamlit as st
import streamlit.components.v1 as components

# 1. ページの設定
st.set_page_config(
    page_title="Happy Birthday! Special Gift Tickets",
    page_icon="🎂",
    layout="centered"
)

# 2. デザイン（CSS）の設定
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff0f3 0%, #ffe3e8 100%);
    }
    .gift-header {
        text-align: center;
        padding: 15px 10px 15px 10px;
    }
    .gift-header h1 {
        color: #e63946;
        font-family: 'Hiragino Mincho ProN', 'Yu Mincho', serif;
        font-weight: bold;
        font-size: 26px;
        margin-bottom: 8px;
    }
    .gift-header p {
        color: #4a4e69;
        font-size: 14px;
        margin: 0;
    }
    /* チケットカードのデザイン */
    .ticket-card {
        background: #ffffff;
        border-radius: 18px;
        border: 2px solid #ffccd5;
        padding: 22px;
        box-shadow: 0 10px 20px rgba(230, 57, 70, 0.08);
        position: relative;
        overflow: hidden;
    }
    .ticket-tag {
        background: #ff4d6d;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .ticket-title {
        font-size: 20px;
        font-weight: bold;
        color: #2b2d42;
        margin-bottom: 8px;
    }
    .ticket-desc {
        color: #595959;
        font-size: 13.5px;
        line-height: 1.6;
    }
    /* 使用済みスタンプのデザイン */
    .used-stamp {
        position: absolute;
        top: 20px;
        right: 15px;
        border: 3px solid #d63031;
        color: #d63031;
        font-size: 18px;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 8px;
        transform: rotate(-12deg);
        background: rgba(255, 255, 255, 0.9);
        letter-spacing: 2px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    /* カード間の区切り線 */
    .ticket-divider {
        border: none;
        border-top: 2px dashed #ffb3c1;
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ギフト券データ（ご指定の7枚）
tickets = [
    {
        "id": "ticket_1",
        "tag": "TICKET #01",
        "title": "💆‍♀️ ① 全身マッサージ券",
        "desc": "日頃の疲れをスッキリ解消！頭から足先まで心を込めてしっかりほぐします。"
    },
    {
        "id": "ticket_2",
        "tag": "TICKET #02",
        "title": "🚗 ② ドキドキ恐怖のドライブチケット",
        "desc": "逆走注意！？ちょっとスリリング（？）なドライブにお連れします！"
    },
    {
        "id": "ticket_3",
        "tag": "TICKET #03",
        "title": "🎰 ③ 欲しいの出るまでガチャガチャ回します券",
        "desc": "狙いのが出るまで何回でもチャレンジOK！"
    },
    {
        "id": "ticket_4",
        "tag": "TICKET #04",
        "title": "🐙 ④ たこ焼きチケット",
        "desc": "アツアツ焼き立ての美味しいたこ焼きパーティー！"
    },
    {
        "id": "ticket_5",
        "tag": "TICKET #05",
        "title": "📞 ⑤ ∞時間お電話チケット",
        "desc": "どれだけ長電話になってもOK！何時まででももちもち"
    },
    {
        "id": "ticket_6",
        "tag": "SPECIAL TICKET",
        "title": "✨ ⑥ なんでも券",
        "desc": "願い事をなんでも1つ叶えます！わがまま・お願いごと、なんでもOK"
    },
    {
        "id": "ticket_7",
        "tag": "SPECIAL TICKET",
        "title": "🐌 ⑦ でんでんむしむしチケット",
        "desc": "なにかやらかしてもでんでん大丈夫になる"
    }
]

# 4. セッション状態の初期化
for t in tickets:
    if t["id"] not in st.session_state:
        st.session_state[t["id"]] = False

if "play_effect" not in st.session_state:
    st.session_state["play_effect"] = False

# 5. ヘッダー表示 ＆ チケット進捗メーター
st.markdown("""
<div class="gift-header">
    <p style="font-size: 12px; color: #ff4d6d; letter-spacing: 3px; font-weight: bold;">HAPPY BIRTHDAY</p>
    <h1>🎂 さおり専属 Special Gift Tickets</h1>
    <p>お誕生日おめでとう！好きなタイミングでいつでも使ってね✨</p>
</div>
""", unsafe_allow_html=True)

# 使用枚数カウント
used_count = sum(1 for t in tickets if st.session_state[t["id"]])
total_count = len(tickets)
st.progress(used_count / total_count, text=f"🎁 チケット使用状況：{total_count}枚中 {used_count}枚 使用済み")

# 6. 紙吹雪演出の埋め込み
if st.session_state["play_effect"]:
    components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            var count = 200;
            var defaults = { origin: { y: 0.7 } };
            function fire(particleRatio, opts) {
                confetti(Object.assign({}, defaults, opts, {
                    particleCount: Math.floor(count * particleRatio)
                }));
            }
            fire(0.25, { spread: 26, startVelocity: 55 });
            fire(0.2, { spread: 60 });
            fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
            fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
            fire(0.1, { spread: 120, startVelocity: 45 });
        </script>
    """, height=0)
    st.session_state["play_effect"] = False

# 7. 使用確認用のダイアログ
@st.dialog("⚠️ 使用確認")
def confirm_use_dialog(ticket_id, ticket_title):
    st.write(f"本当に **「{ticket_title}」** を使用しますか？")
    st.write("※使用すると「使用済み」に切り替わります。")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("はい、使います！ 🎉", key=f"confirm_{ticket_id}", use_container_width=True, type="primary"):
            st.session_state[ticket_id] = True
            st.session_state["play_effect"] = True
            st.rerun()
    with col_b:
        if st.button("キャンセル", key=f"cancel_{ticket_id}", use_container_width=True):
            st.rerun()

# 8. チケットの一覧表示（HTMLタグが文字化けしないように修正）
for idx, t in enumerate(tickets):
    is_used = st.session_state[t["id"]]
    
    stamp = '<div class="used-stamp">USED / 使用済</div>' if is_used else ''
    
    card_html = f'''
    <div class="ticket-card">
        {stamp}
        <span class="ticket-tag">{t['tag']}</span>
        <div class="ticket-title">{t['title']}</div>
        <div class="ticket-desc">{t['desc']}</div>
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    st.write("")
    if is_used:
        st.button("【 使用済み 】", key=f"btn_{t['id']}", disabled=True, use_container_width=True)
    else:
        if st.button("この券を使う 🎁", key=f"btn_{t['id']}", use_container_width=True):
            confirm_use_dialog(t["id"], t["title"])
            
    if idx < len(tickets) - 1:
        st.markdown('<div class="ticket-divider"></div>', unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()

# 9. 管理者用リセットエリア
with st.expander("⚙️ 管理者用メニュー"):
    password = st.text_input("暗証番号を入力", type="password")
    if password == "1234":
        if st.button("すべてのチケットを「未使用」に戻す"):
            for t in tickets:
                st.session_state[t["id"]] = False
            st.success("すべてのチケットをリセットしました！")
            st.rerun()
