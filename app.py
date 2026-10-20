import streamlit as st

# 1. ページの設定
st.set_page_config(
    page_title="Happy Birthday! Special Gift Tickets",
    page_icon="🎂",
    layout="centered"
)

# 2. ヘッダー表示
st.markdown("<h1 style='text-align: center; color: #e63946;'>🎂 Special Gift Tickets</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a4e69;'>お誕生日おめでとう！好きなタイミングでいつでも使ってね✨</p>", unsafe_allow_html=True)
st.write("")

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

# 5. チケット使用状況メーター
used_count = sum(1 for t in tickets if st.session_state[t["id"]])
total_count = len(tickets)
st.progress(used_count / total_count, text=f"🎁 チケット使用状況：{total_count}枚中 {used_count}枚 使用済み")
st.write("")

# 6. 使用確認用のポップアップ（ダイアログ）
@st.dialog("⚠️ 使用確認")
def confirm_use_dialog(ticket_id, ticket_title):
    st.write(f"本当に **「{ticket_title}」** を使用しますか？")
    st.write("※使用すると「使用済み」に切り替わります。")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("はい、使います！ 🎉", key=f"confirm_{ticket_id}", use_container_width=True, type="primary"):
            st.session_state[ticket_id] = True
            st.balloons()  # 画面全体に風船・紙吹雪が舞い上がります
            st.rerun()
    with col_b:
        if st.button("キャンセル", key=f"cancel_{ticket_id}", use_container_width=True):
            st.rerun()

# 7. チケットの一覧表示（Streamlitの標準パーツで美しく安全に構築）
for idx, t in enumerate(tickets):
    is_used = st.session_state[t["id"]]
    
    # カード風の枠線ボックスを作成
    with st.container(border=True):
        if is_used:
            st.markdown("🔴 **【 USED / 使用済み 】**")
        else:
            st.markdown(f"🏷️ **{t['tag']}**")
            
        st.subheader(t['title'])
        st.write(t['desc'])
        
        st.write("")
        if is_used:
            st.button("使用済み", key=f"btn_{t['id']}", disabled=True, use_container_width=True)
        else:
            if st.button("この券を使う 🎁", key=f"btn_{t['id']}", use_container_width=True):
                confirm_use_dialog(t["id"], t["title"])
                
    st.write("") # カードとカードの間のスペース

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
