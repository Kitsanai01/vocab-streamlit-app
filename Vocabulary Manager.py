import streamlit as st
import string

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="wide")

# ---------------- Style ----------------
st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }

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

.meaning {
    flex: 1;
    text-align: right;
    font-size:15px;
    color:#e5e7eb;
}

.section {
    margin-top: 25px;
    padding: 8px;
    border-left: 5px solid #4CAF50;
    background-color: #111318;
    border-radius: 8px;
}

.az-nav a { margin-right:8px; text-decoration:none; color:#9ca3af; }
.az-nav a:hover { color:#4CAF50; }

.highlight {
    border:2px solid #4CAF50;
    box-shadow:0 0 15px #4CAF50;
}

@media (max-width: 768px) {
    .card {
        flex-direction: column;
        align-items: flex-start;
        text-align: left;
    }
    .meaning {
        text-align: left;
        margin-top: 5px;
    }
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
def add_word():
    w = st.session_state.word_input.strip()
    p = st.session_state.pron_input.strip()
    d = st.session_state.def_input.strip()

    if not w or not p or not d:
        st.toast("⚠️ กรุณากรอกข้อมูลให้ครบ")
        return

    if any(v["word"].lower()==w.lower() for v in st.session_state.vocab):
        st.toast(f"❗ '{w}' มีอยู่แล้ว", icon="❗")
    else:
        st.session_state.vocab.append({"word":w,"pron":p,"def":d})
        st.toast(f"✅ เพิ่ม: {w}")
        st.session_state.word_input=""
        st.session_state.pron_input=""
        st.session_state.def_input=""

def delete_word():
    dw = st.session_state.del_input.strip()
    if not dw:
        st.toast("⚠️ กรุณากรอกคำที่จะลบ")
        return

    before=len(st.session_state.vocab)
    st.session_state.vocab=[v for v in st.session_state.vocab if v["word"].lower()!=dw.lower()]

    if len(st.session_state.vocab)<before:
        st.toast(f"🗑 ลบ: {dw}")
        st.session_state.del_input=""
    else:
        st.toast(f"❌ ไม่พบ '{dw}'")

def edit_word():
    target = st.session_state.edit_target.strip()
    new_w = st.session_state.edit_word_input.strip()
    new_p = st.session_state.edit_pron_input.strip()
    new_d = st.session_state.edit_def_input.strip()

    if not target:
        st.toast("⚠️ กรุณากรอกคำที่ต้องการแก้")
        return

    found = False
    for v in st.session_state.vocab:
        if v["word"].lower() == target.lower():
            if new_w:
                v["word"] = new_w
            if new_p:
                v["pron"] = new_p
            if new_d:
                v["def"] = new_d

            st.toast(f"✏️ แก้ไข: {target}")
            found = True
            break

    if not found:
        st.toast(f"❌ ไม่พบ '{target}'")

    # เคลียร์ช่อง
    st.session_state.edit_target = ""
    st.session_state.edit_word_input = ""
    st.session_state.edit_pron_input = ""
    st.session_state.edit_def_input = ""

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# 🔍 Search
st.subheader("🔍 Search")
search_word = st.text_input("Search word")
found_index = -1
sorted_vocab = merge_sort(st.session_state.vocab)

if st.button("Search"):
    found_index = binary_search(sorted_vocab, search_word)
    if found_index != -1:
        st.toast(f"พบ: {sorted_vocab[found_index]['word']}", icon="🔍")
    else:
        st.toast("ไม่พบคำ", icon="❌")

# Sidebar
st.sidebar.header("➕ Add Vocabulary")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Pronunciation", key="pron_input")
st.sidebar.text_input("Definition", key="def_input")

add_disabled = not (
    st.session_state.word_input.strip() and
    st.session_state.pron_input.strip() and
    st.session_state.def_input.strip()
)

st.sidebar.button("Add", on_click=add_word, disabled=add_disabled)

st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete")
st.sidebar.text_input("Word to delete", key="del_input")
st.sidebar.button("Delete", on_click=delete_word)

st.sidebar.markdown("---")
st.sidebar.header("✏️ Edit Vocabulary")

st.sidebar.text_input("Word to edit", key="edit_target")
st.sidebar.text_input("New Word", key="edit_word_input")
st.sidebar.text_input("New Pronunciation", key="edit_pron_input")
st.sidebar.text_input("New Definition", key="edit_def_input")

st.sidebar.button("Edit", on_click=edit_word)

# A-Z Navigation
st.markdown("<div class='az-nav'>" + " ".join([f"<a href='#{l}'>{l}</a>" for l in string.ascii_uppercase]) + "</div>", unsafe_allow_html=True)

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
            st.markdown(f"<div id='{letter}' class='section'><h3>🔤 {letter}</h3></div>", unsafe_allow_html=True)
            for idx,v in enumerate(grouped[letter]):
                highlight_class = "highlight" if found_index != -1 and sorted_vocab[found_index]['word'] == v['word'] else ""
                st.markdown(f"""
                <div class='card {highlight_class}'>
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