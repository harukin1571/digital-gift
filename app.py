
import hmac
from datetime import datetime, timezone

import streamlit as st
from supabase import create_client


# =========================================================
# 1. ページ設定
# =========================================================
st.set_page_config(
    page_title="Happy Birthday! Special Gift Tickets",
    page_icon="🎂",
    layout="centered",
)


# =========================================================
# 2. チケットデータ（全7枚）
# =========================================================
TICKETS = [
    {
        "id": "ticket_1",
        "tag": "TICKET #01",
        "title": "💆‍♀️ ① 全身マッサージ券",
        "desc": "日頃の疲れをスッキリ解消！頭から足先まで心を込めてしっかりほぐします。",
    },
    {
        "id": "ticket_2",
        "tag": "TICKET #02",
        "title": "🚗 ② ドライブチケット",
        "desc": "逆走注意！？ちょっとスリリング（？）なドライブにお連れします！",
    },
    {
        "id": "ticket_3",
        "tag": "TICKET #03",
        "title": "🎰 ③ ガチャガチャ券",
        "desc": "狙いのが出るまで何回でもガチャガチャ回します！",
    },
    {
        "id": "ticket_4",
        "tag": "TICKET #04",
        "title": "🐙 ④ たこ焼きチケット",
        "desc": "アツアツ焼き立ての美味しいたこ焼きパーティー！",
    },
    {
        "id": "ticket_5",
        "tag": "TICKET #05",
        "title": "📞 ⑤ ∞時間お電話券",
        "desc": "どれだけ長電話になってもOK！何時まででももちもち",
    },
    {
        "id": "ticket_6",
        "tag": "SPECIAL TICKET",
        "title": "✨ ⑥ なんでも券",
        "desc": "願い事をなんでも1つ叶えます！わがまま・お願いごと、なんでもOK",
    },
    {
        "id": "ticket_7",
        "tag": "SPECIAL TICKET",
        "title": "🐌 ⑦ でんでんむしむしチケット",
        "desc": "なにかやらかしてもでんでん大丈夫になる",
    },
]

TICKET_IDS = [ticket["id"] for ticket in TICKETS]


# =========================================================
# 3. CSSデザイン（元のピンクデザインを維持）
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg, #fff0f3 0%, #ffe3e8 100%
        );
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

    .ticket-divider {
        border: none;
        border-top: 2px dashed #ffb3c1;
        margin: 30px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. Supabase接続
#    URLと秘密鍵はStreamlit CloudのSecretsから取得
# =========================================================
@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"].strip()
    secret_key = st.secrets["SUPABASE_SECRET_KEY"].strip()

    return create_client(url, secret_key)


try:
    supabase = get_supabase_client()
except Exception:
    st.error(
        "Supabaseに接続できませんでした。"
        "Streamlit CloudのSettings → Secretsで"
        "SUPABASE_URLとSUPABASE_SECRET_KEYを確認してください。"
    )
    st.stop()


# =========================================================
# 5. データベース操作
# =========================================================
def current_utc_time():
    """Supabaseに保存するUTC日時を作成する。"""
    return datetime.now(timezone.utc).isoformat()


def load_ticket_status():
    """データベースから7枚すべての最新状態を読み込む。"""
    response = (
        supabase.table("gift_tickets")
        .select("id, is_used")
        .in_("id", TICKET_IDS)
        .execute()
    )

    status = {
        row["id"]: row["is_used"]
        for row in response.data
    }

    missing_ids = set(TICKET_IDS) - set(status)

    if missing_ids:
        raise RuntimeError(
            "データベースに存在しないチケットがあります: "
            + ", ".join(sorted(missing_ids))
            + "。初期化SQLを実行してください。"
        )

    return status


def use_ticket(ticket_id):
    """
    未使用のチケットだけを使用済みにする。
    すでに別の端末で使用済みなら更新しない。
    """
    response = (
        supabase.table("gift_tickets")
        .update({
            "is_used": True,
            "updated_at": current_utc_time(),
        })
        .eq("id", ticket_id)
        .eq("is_used", False)
        .select("id")
        .execute()
    )

    return bool(response.data)


def reset_all_tickets():
    """7枚すべてを未使用に戻す。"""
    supabase.table("gift_tickets").update(
        {
            "is_used": False,
            "updated_at": current_utc_time(),
        }
    ).in_("id", TICKET_IDS).execute()


# =========================================================
# 6. ヘッダー
# =========================================================
st.markdown(
    """
    <div class="gift-header">
        <p style="
            font-size:12px;
            color:#ff4d6d;
            letter-spacing:3px;
            font-weight:bold;
        ">HAPPY BIRTHDAY</p>

<h1>Special Gift Tickets</h1>

<p>
    お誕生日おめでとう！好きなタイミングでいつでも使ってね✨
</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 7. セッション状態（画面内の一時情報のみ）
#    チケットの使用状態自体はSupabaseに保存する
# =========================================================
if "pending_ticket" not in st.session_state:
    st.session_state["pending_ticket"] = None

if "celebrate" not in st.session_state:
    st.session_state["celebrate"] = False

if "notice" not in st.session_state:
    st.session_state["notice"] = None

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False


# =========================================================
# 8. 使用確認ダイアログ
# =========================================================
@st.dialog("⚠️ 使用確認")
def confirm_use_dialog(ticket_id, ticket_title):
    st.write(f"本当に **「{ticket_title}」** を使用しますか？")
    st.write("※使用すると「使用済み」に切り替わります。")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(
            "はい、使います！",
            key=f"confirm_{ticket_id}",
            use_container_width=True,
            type="primary",
        ):
            try:
                success = use_ticket(ticket_id)

                st.session_state["pending_ticket"] = None

                if success:
                    st.session_state["celebrate"] = True
                    st.session_state["notice"] = (
                        f"「{ticket_title}」を使用しました！"
                    )
                else:
                    st.session_state["notice"] = (
                        "このチケットはすでに使用済みです。"
                        "最新の状態に更新しました。"
                    )

                st.rerun()

            except Exception:
                st.error(
                    "保存に失敗しました。使用状態は変更できていません。"
                    "通信環境やSupabaseの設定を確認してください。"
                )

    with col_b:
        if st.button(
            "キャンセル",
            key=f"cancel_{ticket_id}",
            use_container_width=True,
        ):
            st.session_state["pending_ticket"] = None
            st.rerun()


# =========================================================
# 9. 最新状態を読み込む
# =========================================================

try:
    ticket_status = load_ticket_status()
except Exception as e:
    st.error(
        "チケットの状態を読み込めませんでした。"
        "接続情報・テーブル・権限を確認してください。"
    )
    st.exception(e)
    st.stop()



# =========================================================
# 10. お知らせ・風船演出
# =========================================================
notice = st.session_state.get("notice")

if notice:
    st.info(notice)
    st.session_state["notice"] = None

if st.session_state.get("celebrate", False):
    st.balloons()
    st.session_state["celebrate"] = False


# =========================================================
# 11. 手動更新ボタン
# =========================================================
if st.button("🔄 最新の使用状況に更新", use_container_width=True):
    st.rerun()


# =========================================================
# 12. 7枚のチケット一覧
# =========================================================
for index, ticket in enumerate(TICKETS):
    ticket_id = ticket["id"]
    is_used = ticket_status[ticket_id]

    # チケットカード
    st.markdown(
        f"""
        <div class="ticket-card">
            <span class="ticket-tag">{ticket['tag']}</span>
            <div class="ticket-title">{ticket['title']}</div>
            <div class="ticket-desc">{ticket['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if is_used:
        st.error("【 USED / 使用済み 】")
    else:
        if st.button(
            "この券を使う 🎁",
            key=f"btn_{ticket_id}",
            use_container_width=True,
        ):
            st.session_state["pending_ticket"] = ticket_id
            st.rerun()

    # 最後のチケットの後には区切り線を表示しない
    if index < len(TICKETS) - 1:
        st.markdown(
            '<div class="ticket-divider"></div>',
            unsafe_allow_html=True,
        )


# =========================================================
# 13. 確認ダイアログを表示
# =========================================================
pending_ticket = st.session_state.get("pending_ticket")

if pending_ticket in TICKET_IDS:
    selected_ticket = next(
        ticket
        for ticket in TICKETS
        if ticket["id"] == pending_ticket
    )

    # ダイアログを開く直前にも最新状態を確認
    try:
        latest_status = load_ticket_status()

        if latest_status[pending_ticket]:
            st.session_state["pending_ticket"] = None
            st.warning(
                "このチケットは別の端末ですでに使用されています。"
            )
            st.rerun()
        else:
            confirm_use_dialog(
                pending_ticket,
                selected_ticket["title"],
            )

    except Exception:
        st.error(
            "チケットの最新状態を確認できませんでした。"
            "時間をおいて再読み込みしてください。"
        )


# =========================================================
# 14. 管理者用リセット機能
# =========================================================
st.write("")
st.write("")
st.divider()

with st.expander("⚙️ 管理者用メニュー"):
    password = st.text_input(
        "管理者用の暗証番号を入力",
        type="password",
        key="admin_password",
    )

    if st.button("管理者認証", key="admin_login"):
        try:
            admin_password = st.secrets["ADMIN_PASSWORD"]

            if hmac.compare_digest(password, admin_password):
                st.session_state["is_admin"] = True
                st.success("管理者として認証しました。")
            else:
                st.session_state["is_admin"] = False
                st.error("暗証番号が違います。")

        except Exception:
            st.error(
                "ADMIN_PASSWORDがSecretsに設定されているか確認してください。"
            )

    if st.session_state.get("is_admin", False):
        st.warning(
            "リセットすると、あなたと相手の画面で共有される"
            "7枚すべてのチケットが未使用に戻ります。"
        )

        if st.button(
            "すべてのチケットを「未使用」に戻す",
            key="reset_all",
            type="primary",
            use_container_width=True,
        ):
            try:
                reset_all_tickets()

                st.session_state["pending_ticket"] = None
                st.session_state["celebrate"] = False
                st.session_state["notice"] = (
                    "すべてのチケットをリセットしました！"
                )

                st.rerun()

            except Exception:
                st.error(
                    "リセットに失敗しました。"
                    "Supabaseの接続や権限を確認してください。"
                )

        if st.button("管理者ログアウト", key="admin_logout"):
            st.session_state["is_admin"] = False
            st.rerun()
