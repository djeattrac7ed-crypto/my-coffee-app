import streamlit as st

# 1. 장바구니 준비
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("☕ 음료 오더")
st.info("💡 한 분이 여러 잔을 주문하시려면, 메뉴를 고르고 '담기'를 반복해 주세요!")

# --- 📸 1단계: 공용 메뉴판 (탭 기능) ---
st.subheader("📸 메뉴판 확인")
tab1, tab2 = st.tabs(["메뉴판 1", "메뉴판 2"])
with tab1:
    try: st.image("menu1.jpg", use_container_width=True)
    except: st.write("사진 없음")
with tab2:
    try: st.image("menu2.jpg", use_container_width=True)
    except: st.write("사진 없음")

st.divider()

# --- 👤 2단계: 주문자 및 메뉴 입력 ---
# '반 선택'을 한 번 하면 초기화되지 않도록 구성했습니다.
teacher_class = st.selectbox(
    "몇 반 선생님이신가요? (본인 혹은 대리 주문자)", 
    ["선택", "1반", "2반", "3반", "4반", "5반", "6반"]
)

menu_name = st.text_input("음료 이름을 입력해 주세요", placeholder="예: 아메리카노, 아이스티 등")

# --- 🧊 3단계: 세부 옵션 ---
c1, c2, c3 = st.columns(3)
with c1:
    temp = st.radio("온도", ["❄️ ICE", "🔥 HOT"])
with c2:
    size = st.radio("사이즈", ["소(기본)", "중", "대"])
with c3:
    sweet = st.radio("당도", ["기본", "덜 달게", "더 달게"])

# --- 🛒 4단계: 장바구니 담기 (연속 주문 핵심) ---
if st.button("➕ 이 메뉴 장바구니에 담기", use_container_width=True):
    if teacher_class == "선택" or menu_name == "":
        st.warning("⚠️ 반 선택과 메뉴명 입력을 확인해 주세요!")
    else:
        order_detail = f"[{teacher_class}] {menu_name} ({temp}/{size}/당도:{sweet})"
        st.session_state.cart.append(order_detail)
        # 성공 메시지를 짧게 띄워 '연속 주문' 흐름을 방해하지 않게 합니다.
        st.toast(f"✅ {menu_name}이 담겼습니다! 다른 메뉴를 더 고르셔도 됩니다.")

st.divider()

# --- 📋 5단계: 최종 주문 목록 확인 및 전송 준비 ---
st.subheader("📋 우리 팀 전체 주문 현황")

if st.session_state.cart:
    # 한 사람이 여러 개를 시켰을 때 보기 편하게 리스트로 나열
    for i, item in enumerate(st.session_state.cart):
        l_col, r_col = st.columns([8, 2])
        with l_col:
            st.write(f"**{i+1}.** {item}")
        with r_col:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    st.write("")
    # 🌟 꿀기능: 카톡 전송용 텍스트 복사
    all_orders = "\n".join(st.session_state.cart)
    st.text_area("카톡 전달용 텍스트 (아래를 복사해서 카톡에 붙여넣으세요)", value=all_orders, height=150)
    
    if st.button("🗑️ 전체 비우기"):
        st.session_state.cart = []
        st.rerun()
else:
    st.info("아직 주문 내역이 없습니다. 메뉴를 선택하고 담아주세요!")
