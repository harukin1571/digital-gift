import streamlit as st

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
        padding: 15px 10px 25px 10px;
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
    /* チケットカードのデザイン（独立感を持たせる） */
    .ticket-card {
        background: #ffffff;
        border-radius: 18px;
        border: 2px solid #ffccd5;
        padding: 22px;
        box-shadow: 0 10px 20px rgba(230, 57, 70, 0.08);
        position: relative;
        transition: transform 0.2s ease;
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
    /* カード間の区切り線（ミシン目風） */
    .ticket-divider {
        border: none;
        border-top: 2px dashed #ffb3c1;
        margin: 30px 0;
        position: relative;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ヘッダー表示
st.markdown("""
<div class="gift-header">
    <p style="font-size: 12px; color: #ff4d6d; letter-spacing: 3px; font-weight: bold;">HAPPY BIRTHDAY</p>
    <h1>🎂 さおり専属 Special Gift Tickets</h1>
    <p>お誕生日おめでとう！好きなタイミングでいつでも使ってね✨</p>
</div>
""", unsafe_allow_html=True)

# 4. ギフト券データ（ご指定の6枚）
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
        "desc": "行先は着いてからのお楽しみ！？ちょっとスリリング（？）で特別なドライブにお連れします！"
    },
    {
        "id": "ticket_3",
        "tag": "TICKET #03",
        "title": "🎰 ③ 欲しいの出るまでガチャガチャ回します券",
        "desc": "狙いの景品が出るまで何回でもチャレンジOK！コンプリートを目指そう。"
    },
    {
        "id": "ticket_4",
        "tag": "TICKET #04",
        "title": "🐙 ④ たこ焼きチケット",
        "desc": "アツアツ焼き立ての美味しいたこ焼きをご馳走（または一緒に作ってパーティー）します！"
    },
    {
        "id": "ticket_5",
        "tag": "TICKET #05",
        "title": "📞 ⑤ ∞時間お電話チケット",
        "desc": "どれだけ長電話になってもOK！寝落ちするまでずっと一緒におしゃべりしよう。"
    },
    {
        "id": "ticket_6",
        "tag": "SPECIAL TICKET",
        "title": "✨ ⑥ なんでも券",
        "desc": "願い事をなんでも1つ叶えます！わがまま・お願いごと、なんでも大歓迎。"
    }
]

# 5. セッション状態の初期化
for t in tickets:
    if t["id"] not in st.session_state:
        st.session_state[t["id"]] = False

# 6. 使用確認用のダイアログ（ポップアップ機能）
@st.dialog("⚠️ 使用確認")
def confirm_use_dialog(ticket_id, ticket_title):
    st.write(f"本当に **「{ticket_title}」** を使用しますか？")
    st.write("※使用すると「使用済み」に切り替わります。")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("はい、使います！", key=f"confirm_{ticket_id}", use_container_width=True, type="primary"):
            st.session_state[ticket_id] = True
            st.balloons()
            st.rerun()
    with col_b:
        if st.button("キャンセル", key=f"cancel_{ticket_id}", use_container_width=True):
            st.rerun()

# 7. チケットの一覧表示
for idx, t in enumerate(tickets):
    is_used = st.session_state[t["id"]]
    
    st.markdown(f"""
    <div class="ticket-card">
        <span class="ticket-tag">{t['tag']}</span>
        <div class="ticket-title">{t['title']}</div>
        <div class="ticket-desc">{t['desc']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if is_used:
        st.error("【 USED / 使用済み 】")
    else:
        if st.button("この券を使う 🎁", key=f"btn_{t['id']}", use_container_width=True):
            confirm_use_dialog(t["id"], t["title"])
            
    if idx < len(tickets) - 1:
        st.markdown('<div class="ticket-divider"></div>', unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()

# 8. 管理者用リセットエリア
with st.expander("⚙️ 管理者用メニュー"):
    password = st.text_input("暗証番号を入力", type="password")
    if password == "1234":
        if st.button("すべてのチケットを「未使用」に戻す"):
            for t in tickets:
                st.session_state[t["id"]] = False
            st.success("すべてのチケットをリセットしました！")
            st.rerun()
