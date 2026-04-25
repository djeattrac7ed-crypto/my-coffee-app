import streamlit as st

# 1. 장바구니(세션 상태) 만들기
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.title("☕ 선생님 커피 주문")
st.write("메뉴와 옵션을 선택하고 장바구니에 담아주세요!")

st.divider()

# 👤 주문자 선택
st.subheader("👤 주문자 선택")
teacher_class = st.selectbox(
    "몇 반 선생님이신가요?", 
    ["선택해주세요", "1반", "2반", "3반", "4반", "5반", "6반"]
)

st.divider()

# 2. 메뉴 선택 영역

st.divider()

# 📸 새롭게 추가된 'AI 이미지 인식' 영역
st.subheader("📸 메뉴판 사진 업로드")
uploaded_file = st.file_uploader("새로운 카페의 메뉴판 사진을 올려주세요.", type=['jpg', 'png', 'jpeg'])

# 메뉴를 저장할 빈 바구니(세션 상태) 만들기
if 'dynamic_menu' not in st.session_state:
    st.session_state.dynamic_menu = ["선택해주세요", "☕ 아메리카노", "🥛 카페라떼"] # 기본 메뉴

# 사진이 업로드 되었다면?
if uploaded_file is not None:
    # 올린 사진을 화면에 작게 보여줍니다.
    st.image(uploaded_file, caption="업로드된 메뉴판", width=300)
    
    if st.button("🤖 AI로 메뉴 읽어오기"):
        with st.spinner("AI가 메뉴판의 글씨를 열심히 읽고 있습니다..."):
            import time
            time.sleep(2) # AI가 생각하는 것처럼 2초간 뜸을 들입니다.
            
            # 🌟 [핵심] 실제로는 여기서 AI에게 사진을 보내고 결과를 받아옵니다!
            # 지금은 사진을 올리면 무조건 아래 메뉴로 바뀌도록 설정해 두었습니다.
            new_menus = ["선택해주세요", "🧋 흑당 버블티", "🍵 쌍화차", "☕ 다방 커피", "🍓 생딸기 주스"]
            
            # 새로 받아온 메뉴로 기존 메뉴판을 갈아끼웁니다!
            st.session_state.dynamic_menu = new_menus
            st.success("✨ 새로운 메뉴판 인식 완료!")

st.divider()

# 2. 메인 메뉴 선택 (고정된 글자가 아니라, 사진을 올리면 바뀌는 변수를 넣습니다)
st.subheader("1. 메뉴 선택")
menu = st.selectbox("음료를 선택하세요", st.session_state.dynamic_menu)

# --- (이 아래부터 3번 옵션 선택, 4번 장바구니 코드는 기존과 동일하게 이어집니다) ---

# 3. 옵션 선택 영역
st.subheader("2. 옵션 선택")
col1, col2 = st.columns(2)

with col1:
    temp = st.radio("온도", ["❄️ ICE", "🔥 HOT"])

with col2:
    size = st.radio("사이즈", ["Tall (기본)", "Grande", "Venti"])

# 4. 장바구니 담기 버튼
st.write("") 
if st.button("🛒 장바구니에 담기"):
    if teacher_class == "선택해주세요":
        st.warning("⚠️ 선생님의 반을 먼저 선택해 주세요!")
    else:
        order = f"[{teacher_class}] {menu} / {temp} / {size}"
        st.session_state.cart.append(order)
        st.success(f"성공! {teacher_class} 선생님의 주문이 담겼습니다.")

st.divider()

# 5. 장바구니 확인 영역 (🌟 이 부분이 크게 업그레이드되었습니다!)
st.subheader("📋 현재 주문 목록")

if len(st.session_state.cart) > 0:
    # 장바구니에 있는 물건 개수만큼 반복합니다.
    for i, item in enumerate(st.session_state.cart):
        # 화면을 8대 2 비율로 나눕니다. (글씨 8, 버튼 2)
        list_col, btn_col = st.columns([8, 2])
        
        with list_col:
            # 8의 공간에 주문 내용을 적습니다.
            st.write(f"**{i+1}번:** {item}")
            
        with btn_col:
            # 2의 공간에 삭제 버튼을 만듭니다. (버튼마다 고유한 이름(key)이 필요합니다)
            if st.button("❌ 삭제", key=f"del_{i}"):
                # 버튼을 누르면 장바구니에서 해당 번호(i)의 주문을 뺍니다.
                st.session_state.cart.pop(i)
                st.rerun() # 화면을 새로고침해서 지워진 걸 바로 보여줍니다.
                
    st.write("") # 빈칸 살짝 띄우기
    if st.button("🗑️ 전체 주문 비우기"):
        st.session_state.cart = []
        st.rerun() 
else:
    st.info("아직 담긴 음료가 없습니다.")
