import streamlit as st
from models import Member, Transaction, Split, calculate_balances
import pandas as pd


# 初始化 Streamlit 應用的會話狀態
if 'members' not in st.session_state:
    st.session_state['members'] = []
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

def display_and_save_transactions_dataframe():
    if st.session_state.transactions:
        data = {
            "品項名稱": [t.item_name for t in st.session_state.transactions],
            "金額": [t.amount for t in st.session_state.transactions],
            "付款人": [t.payer.name for t in st.session_state.transactions],
            "日期": [t.date.strftime("%Y-%m-%d") for t in st.session_state.transactions],
            "備註": [t.note for t in st.session_state.transactions]
        }
        df = pd.DataFrame(data)

        # Display DataFrame with custom styles
        st.dataframe(df, width=1500)  # General width for the DataFrame
        
        # Custom CSS to fix column widths
        st.markdown("""
            <style>
            .dataframe th:nth-child(1), .dataframe td:nth-child(1) {width: 200px !important;} /* Column 1 "品項名稱" */
            .dataframe th:nth-child(2), .dataframe td:nth-child(2) {width: 100px !important;} /* Column 2 "金額" */
            </style>
            """, unsafe_allow_html=True)

        # CSV download button
        if st.button('保存交易記錄為 CSV'):
            csv = df.to_csv(index=False)
            st.download_button(
                label="下載 CSV",
                data=csv,
                file_name='transactions.csv',
                mime='text/csv',
            )
    else:
        st.write("目前沒有交易記錄。")
        

# 添加成員的函數
def add_member():
    if st.session_state.member_name :
        st.session_state.members.append(Member(st.session_state.member_name, ""))
        st.success(f'成員 {st.session_state.member_name} 已新增')
        st.session_state.member_name = ""

# 添加交易的函數
def add_transaction(transaction_category, amount, payer_name, splits, equal_split, note):
    payer = next((m for m in st.session_state.members if m.name == payer_name), None)
    if not payer:
        st.error("付款人未找到，請確認付款人已經添加到成員列表中。")
        return

    transaction = Transaction(transaction_category, float(amount), payer, note)
    if equal_split:
        split_share = float(amount) / len(st.session_state.members)
        for member in st.session_state.members:
            if member.name != payer_name:
                transaction.add_split(Split(member, split_share))
    else:
        for split in splits:
            member = next((m for m in st.session_state.members if m.name == split), None)
            if not member:
                st.error(f"成員 {split} 未找到，請確認成員已經添加到成員列表中。")
                return
            split_share = float(amount) / len(splits)
            transaction.add_split(Split(member, split_share))

    st.session_state.transactions.append(transaction)
    st.success('交易已成功記錄。')


st.title('🛫出遊分帳系統')

# 成員管理介面
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('✚新增成員')
        st.text_input('成員名稱', key="member_name")
        st.button('新增成員', on_click=add_member)
        
    with col2:
        st.subheader('🧑‍🧑‍🧒所有成員')
        if st.session_state.members:
            for member in st.session_state.members:
                st.write(f"👤 {member.name}")

# 交易記錄介面
with st.container():
    st.subheader('💸新增交易')
    transaction_category = st.selectbox('品項類別', ['🍽️飲食', '🚊交通', '🎮娛樂', '🏠住宿', '🛍️購物', '🎫票卷', '其他'], key="transaction_category")
    transaction_note = st.text_input('備註', key="transaction_note")  
    transaction_amount = st.text_input('金額', key="transaction_amount")
    transaction_payer = st.selectbox('付款人', [m.name for m in st.session_state.members], key="transaction_payer")
    equal_split = st.checkbox('所有人均分')
    splits = []
    if not equal_split:
        splits = st.multiselect('分帳', [m.name for m in st.session_state.members if m.name != transaction_payer], key="transaction_splits")
    if st.button('記錄交易'):
        add_transaction(transaction_category, transaction_amount, transaction_payer, splits, equal_split, transaction_note)


# 債務計算介面
with st.container():
    st.subheader('📊計算債務')
    if st.button('顯示債務關係'):
        balances = calculate_balances(st.session_state.transactions)
        st.write('債務關係：')
        st.write(balances)


with st.container():
    st.subheader("🧾 所有交易的 DataFrame")
    display_and_save_transactions_dataframe()         