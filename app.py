import streamlit as st

# 1. ページの設定（タイトルや表示幅）
st.set_page_config(
    page_title="デジタル・プレミアムギフト券",
    page_icon="🎁",
    layout="centered"
)

# 2. デザイン（CSS）の設定
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe3e3 100%);
    }
    .gift-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .gift-header h1 {
        color: #d63031;
        font-family: 'Hiragino Mincho ProN', 'Yu Mincho', serif;
        font-weight: bold;
    }
    .ticket-card {
        background: white;
        border-radius: 16px;
        border: 2px dashed #ff7675;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.06);
    }
    .ticket-tag {
        background: #ff7675;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }
    .ticket-title {
        font-size: 18px;
        font-weight: bold;
        color: #2d3436;
        margin-bottom: 6px;
    }
    .ticket-desc {
        color: #636e72;
        font-size: 13px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ヘッダー表示
st.markdown("""
<div class="gift-header">
    <p style="font-size: 13px; color: #e17055; letter-spacing: 2px; margin-bottom: 4px;">SPECIAL GIFT TICKET</p>
    <h1>🎁 プレミアム肩叩き・お手伝い券</h1>
    <p style="color: #636e72; font-size: 13px; margin-top: 0;">いつもありがとうの気持ちを込めて</p>
</div>
""", unsafe_allow_html=True)

# 4. ギフト券データ（ここでタイトルや内容を自由に変更できます！）
tickets = [
    {
        "id": "ticket_1",
        "tag": "Ticket #1",
        "title": "💆‍♂️ 極上肩叩き 30分コース",
        "desc": "疲れた肩をしっかり揉みほぐします！力加減の指定も自由です。"
    },
    {
        "id": "ticket_2",
        "tag": "Ticket #2",
        "title": "🦶 癒やしの足裏マッサージ 20分",
        "desc": "一日の終わりに足のむくみ・疲れをスッキリ解消。"
    },
    {
        "id": "ticket_3",
        "tag": "Ticket #3",
        "title": "☕️ お好きなドリンク淹れます券",
        "desc": "コーヒーや紅茶など、お好みの飲み物をお部屋までお届け！"
    },
    {
        "id": "ticket_4",
        "tag": "Ticket #4",
        "title": "✨ なんでもお願い・自由券",
        "desc": "家事の手伝い・買い物・肩叩きの延長など、なんでも頼めるスペシャル券！"
    }
]

# 5. ギフト券の保存状態を準備
for t in tickets:
    if t["id"] not in st.session_state:
        st.session_state[t["id"]] = False

# 6. チケットを順番に画面に表示
for t in tickets:
    is_used = st.session_state[t["id"]]
    
    col1, col2 = st.columns([3, 1.2])
    
    with col1:
        st.markdown(f"""
        <div class="ticket-card">
            <span class="ticket-tag">{t['tag']}</span>
            <div class="ticket-title">{t['title']}</div>
            <div class="ticket-desc">{t['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.write("") # ボタンの位置調整用スペース
        if is_used:
            st.error("【使用済み】")
        else:
            if st.button("この券を使う", key=f"btn_{t['id']}", use_container_width=True):
                st.session_state[t["id"]] = True
                st.balloons() # 紙ふぶき（風船）のアニメーション演出！
                st.rerun()

st.divider()

# 7. 管理者エリア（パスワードでリセット可能）
with st.expander("⚙️ 管理者用メニュー（プレゼントした本人用）"):
    password = st.text_input("暗証番号を入力してください", type="password")
    if password == "1234": # 暗証番号（好きな数字に変更OK）
        if st.button("すべての券を「未使用」に戻す"):
            for t in tickets:
                st.session_state[t["id"]] = False
            st.success("すべてのチケットをリセットしました！")
            st.rerun()