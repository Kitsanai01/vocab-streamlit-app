import streamlit as st
import string

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="wide")

# ---------------- Style ----------------
st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }

/* Buttons */
.stButton>button {
    border-radius: 10px;
    font-weight: bold;
}

/* Add button */
div[data-testid="stSidebar"] .stButton:nth-of-type(1) button {
    background-color: #4CAF50;
    color: white;
}

/* Delete button */
div[data-testid="stSidebar"] .stButton:nth-of-type(2) button {
    background-color: #e53935;
    color: white;
}

.card {
    max-width: 800px;
    margin: 10px auto;
    padding: 14px 20px;
    border-radius: 14px;
    background: linear-gradient(145deg,#1c1f26,#14161c);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}

.word-block { flex: 1; }
.word { font-size:18px; font-weight:600; color:#4CAF50; }
.pron { font-size:14px; color:#9ca3af; }
.meaning { flex: 1; text-align: right; }

.section { margin-top: 25px; padding: 8px; border-left: 5px solid #4CAF50; background-color: #111318; border-radius: 8px; }

.highlight {
    border:2px solid #4CAF50;
    box-shadow:0 0 15px #4CAF50;
}

@media (max-width: 768px) {
    .card { flex-direction: column; align-items: flex-start; }
    .meaning { text-align: left; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

# ---------------- Functions ----------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result=[]
    i=j=0
    while i<len(left) and j<len(right):
        if left[i]["word"].lower() <= right[j]["word"].lower():
            result.append(left[i]); i+=1
        else:
            result.append(right[j]); j+=1
    result.extend(left[i:]); result.extend(right[j:])
    return result


def binary_search(arr,target):
    lo,hi=0,len(arr)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if arr[mid]["word"].lower()==target.lower(): return mid
        elif target.lower()<arr[mid]["word"].lower(): hi=mid-1
        else: lo=mid+1
    return -1

# ---------------- Callbacks ----------------
def show_toast(msg, type="success"):
    icons = {"success":"✅","error":"❌","warning":"⚠️","edit":"✏️"}
    st.toast(msg, icon=icons.get(type,"ℹ️"))


def add_word():
    w = st.session_state.word_input.strip()
    p = st.session_state.pron_input.strip()
    d = st.session_state.def_input.strip()

    if not w or not p or not d:
        show_toast("กรอกข้อมูลให้ครบ", "warning")
        return

    if any(v["word"].lower()==w.lower() for v in st.session_state.vocab):
        show_toast(f"'{w}' มีอยู่แล้ว", "warning")
    else:
        st.session_state.vocab.append({"word":w,"pron":p,"def":d})
        show_toast(f"เพิ่ม: {w}", "success")
        st.session_state.word_input=""
        st.session_state.pron_input=""
        st.session_state.def_input=""


def delete_word():
    dw = st.session_state.del_input.strip()
    if not dw:
        show_toast("กรอกคำที่จะลบ", "warning")
        return

    before=len(st.session_state.vocab)
    st.session_state.vocab=[v for v in st.session_state.vocab if v["word"].lower()!=dw.lower()]

    if len(st.session_state.vocab)<before:
        show_toast(f"ลบ: {dw}", "error")
        st.session_state.del_input=""
    else:
        show_toast("ไม่พบคำ", "error")


def edit_word():
    target = st.session_state.edit_target.strip()
    new_word = st.session_state.edit_word.strip()
    new_pron = st.session_state.edit_pron.strip()
    new_def = st.session_state.edit_def.strip()

    for v in st.session_state.vocab:
        if v["word"].lower() == target.lower():
            if new_word: v["word"] = new_word
            if new_pron: v["pron"] = new_pron
            if new_def: v["def"] = new_def
            show_toast(f"แก้ไข: {target}", "edit")
            return

    show_toast("ไม่พบคำที่จะแก้", "error")

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# Search
st.subheader("🔍 Search")
search_word = st.text_input("Search word")
sorted_vocab = merge_sort(st.session_state.vocab)
found_index = binary_search(sorted_vocab, search_word) if search_word else -1

# Sidebar
st.sidebar.header("➕ Add Vocabulary")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Pronunciation", key="pron_input")
st.sidebar.text_input("Definition", key="def_input")
st.sidebar.button("Add", on_click=add_word)

st.sidebar.markdown("---")
st.sidebar.header("✏️ Edit Vocabulary")
st.sidebar.text_input("Word to edit", key="edit_target")
st.sidebar.text_input("New Word", key="edit_word")
st.sidebar.text_input("New Pronunciation", key="edit_pron")
st.sidebar.text_input("New Definition", key="edit_def")
st.sidebar.button("Edit", on_click=edit_word)

st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete")
st.sidebar.text_input("Word to delete", key="del_input")
st.sidebar.button("Delete", on_click=delete_word)

# Display
st.markdown("---")
st.subheader("📖 Vocabulary (A-Z)")

if st.session_state.vocab:
    grouped={}
    for v in sorted_vocab:
        clean=v["word"].strip()
        if not clean: continue
        first=clean[0].upper()
        if not first.isalpha(): first="#"
        grouped.setdefault(first,[]).append(v)

    for letter in string.ascii_uppercase:
        if letter in grouped:
            st.markdown(f"<div class='section'><h3>🔤 {letter}</h3></div>", unsafe_allow_html=True)
            for v in grouped[letter]:
                highlight = "highlight" if search_word and v["word"].lower()==search_word.lower() else ""
                st.markdown(f"""
                <div class='card {highlight}'>
                    <div class='word-block'>
                        <div class='word'>{v['word']}</div>
                        <div class='pron'>{v.get('pron','')}</div>
                    </div>
                    <div class='meaning'>{v['def']}</div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("No vocabulary yet")

st.markdown("---")
st.write(f"📊 Total: {len(st.session_state.vocab)}")