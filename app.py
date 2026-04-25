import streamlit as st

# 1. 장바구니 공간 준비
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("☕ 우리 1학년 스마트 사이렌 오더")
st.write("메뉴판 사진을 확인하고, 원하시는 메뉴와 옵션을 담아주세요!")

st.divider()

# --- (위쪽 장바구니 준비 및 타이틀 코드는 동일) ---

# --- (위쪽 장바구니 준비 및 타이틀 코드는 동일) ---

# --- 📸 1단계: 여러 장의 공용 메뉴판 보여주기 (탭 기능 적용) ---
st.subheader("📸 이번 주 카페 메뉴판")

# 사진 개수에 맞춰서 탭(버튼)을 만듭니다.
tab1, tab2, tab3 = st.tabs(["메뉴 1페이지", "메뉴 2페이지", "메뉴 3페이지"])

with tab1:
    try:
        st.image("menu1.jpg", use_container_width=True)
    except:
        st.info("⚠️ menu1.jpg 파일을 찾을 수 없습니다.")

with tab2:
    try:
        st.image("menu2.jpg", use_container_width=True)
    except:
        st.info("⚠️ menu2.jpg 파일을 찾을 수 없습니다.")

with tab3:
    try:
        st.image("menu3.jpg", use_container_width=True)
    except:
        st.info("⚠️ menu3.jpg 파일을 찾을 수 없습니다.")

st.divider()

# --- (이 아래부터 2단계 주문자 입력 부분은 동일하게 이어집니다) ---

# --- 👤 2단계: 주문자 및 메뉴 입력 ---
col_name, col_menu = st.columns(2)

with col_name:
    teacher_class = st.selectbox(
        "몇 반 선생님인가요?", 
        ["선택", "1반", "2반", "3반", "4반", "5반", "6반", "전담/부장"]
    )

with col_menu:
    # 사진을 보고 메뉴명을 자유롭게 적을 수 있도록 text_input을 사용합니다.
    menu_name = st.text_input("메뉴명을 입력해 주세요", placeholder="예: 아메리카노, 민트초코 등")

st.divider()

# --- 🧊 3단계: 필수/세부 옵션 선택 ---
st.subheader("✨ 세부 옵션 선택")
c1, c2, c3 = st.columns(3)

with c1:
    temp = st.radio("온도", ["❄️ ICE", "🔥 HOT"])

with c2:
    size = st.radio("사이즈", ["소(기본)", "중", "대"])

with c3:
    # 요청하신 '당도' 옵션을 추가했습니다.
    sweet = st.radio("당도(시럽)", ["기본", "덜 달게", "달게"])

st.write("")

# --- 🛒 4단계: 장바구니 담기 ---
if st.button("🛒 장바구니에 담기", use_container_width=True):
    if teacher_class == "선택" or menu_name == "":
        st.warning("⚠️ 반 선택과 메뉴명 입력을 완료해 주세요!")
    else:
        # 주문 내역을 예쁘게 정리
        order_detail = f"[{teacher_class}] {menu_name} ({temp}/{size}/당도:{sweet})"
        st.session_state.cart.append(order_detail)
        st.success(f"'{menu_name}' 주문이 추가되었습니다!")

st.divider()

# --- 📋 5단계: 최종 주문 목록 확인 ---
st.subheader("📋 전체 주문 현황")
if st.session_state.cart:
    for i, item in enumerate(st.session_state.cart):
        l_col, r_col = st.columns([8, 2])
        with l_col:
            st.write(f"**{i+1}.** {item}")
        with r_col:
            if st.button("❌ 삭제", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    st.write("")
    if st.button("🗑️ 전체 주문 초기화"):
        st.session_state.cart = []
        st.rerun()
else:
    st.write("아직 주문 내역이 없습니다.")
