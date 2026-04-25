import streamlit as st

# 1. 장바구니 공간 준비
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="선생님 전용 사이렌 오더", layout="centered")
st.title("☕ 음료 오더")

# --- 📸 1단계: 메뉴판 확인 (모든 사진 펼쳐보기) ---
st.subheader("📸 메뉴판")

# 사진 파일 이름들을 리스트로 만듭니다. (파일이 더 있다면 뒤에 계속 추가 가능)
menu_files = ["menu1.jpg", "menu2.jpg"]

for file_name in menu_files:
    try:
        # 모든 사진을 클릭 없이 바로 보여줍니다.
        st.image(file_name, use_container_width=True, caption=f"메뉴판: {file_name}")
    except:
        st.info(f"⚠️ {file_name} 파일을 찾을 수 없습니다. 깃허브에 업로드했는지 확인해 주세요.")

st.divider()

# --- 👤 2단계: 주문자 및 메뉴 입력 ---
col_who, col_what = st.columns(2)
with col_who:
    teacher_class = st.selectbox(
        "주문자 선택", 
        ["선택", "1반", "2반", "3반", "4반", "5반", "6반"]
    )
with col_what:
    menu_name = st.text_input("메뉴명 입력", placeholder="예: 아메리카노, 고구마케이크")

st.divider()

# --- 🧊 3단계: 퍼스널 옵션 선택 ---
st.subheader("✨ 퍼스널 옵션")

# 안내 문구
st.caption("📢 **안내:** 커피전문점에 따라 커스텀이 불가능한 경우, **기본 레시피**로 주문됩니다.")

# 첫 번째 줄: 온도, 사이즈, 샷
c1, c2, c3 = st.columns(3)
with c1:
    temp = st.radio("온도", ["❄️ ICE", "🔥 HOT"])
with c2:
    size = st.radio("사이즈", ["톨(기본)", "중", "대"])
with c3:
    shot = st.radio("샷 선택", ["기본샷", "샷 추가"])

# 두 번째 줄: 우유, 당도, 얼음(조건부)
c4, c5, c6 = st.columns(3)
with c4:
    milk = st.selectbox("우유 변경", ["일반 우유", "저지방 우유", "두유", "오트(귀리)"])
with c5:
    sweet = st.radio("당도", ["기본", "덜 달게", "더 달게"])
with c6:
    # 핫(HOT) 선택 시 얼음 옵션 숨기기
    if temp == "❄️ ICE":
        ice = st.radio("얼음 양", ["기본", "적게", "많이"])
    else:
        ice = "없음 (HOT)"
        st.write("❄️ 얼음 선택 불가")

# 기타 요구사항 입력
memo = st.text_input("기타 요구사항 (직접 입력)", placeholder="예: 시나몬 가루 많이, 컵홀더 두 개 등")

# --- 🛒 4단계: 장바구니 담기 ---
if st.button("🛒 이 설정으로 장바구니 담기", use_container_width=True):
    if teacher_class == "선택" or menu_name == "":
        st.warning("⚠️ 주문자와 메뉴명을 입력해 주세요!")
    else:
        options = f"{temp}/{size}/{shot}/{milk}/당도:{sweet}/얼음:{ice}"
        if memo:
            options += f" / 요청:{memo}"
            
        order_detail = f"[{teacher_class}] {menu_name} ({options})"
        st.session_state.cart.append(order_detail)
        st.toast(f"✅ {menu_name}이 담겼습니다!")

st.divider()

# --- 📋 5단계: 주문 목록 및 카톡 복사 ---
st.subheader("📋 우리 팀 전체 주문 현황")

if st.session_state.cart:
    for i, item in enumerate(st.session_state.cart):
        l_col, r_col = st.columns([9, 1])
        with l_col:
            st.write(f"**{i+1}.** {item}")
        with r_col:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    st.write("")
    all_orders = "☕ [커피 주문 목록]\n" + "\n".join(st.session_state.cart)
    st.text_area("아래를 복사해서 카톡에 전달하세요", value=all_orders, height=200)
    
    if st.button("🗑️ 전체 주문 초기화"):
        st.session_state.cart = []
