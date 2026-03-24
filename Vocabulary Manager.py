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
.meaning { flex: 1; text-align: right; }

.section { margin-top: 25px; padding: 8px; border-left: 5px solid #4CAF50; background-color: #111318; border-radius: 8px; }

.highlight { border:2px solid #4CAF50; box-shadow:0 0 15px #4CAF50; }

.az-nav { text-align:center; margin-bottom:10px; }
.az-nav a { margin:4px; padding:6px 10px; border-radius:6px; background:#1c1f26; color:#9ca3af; text-decoration:none; }
.az-nav a:hover { background:#4CAF50; color:white; }

@media (max-width: 768px) {
    .card { flex-direction: column; align-items: flex-start; }
    .meaning { text-align: left; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

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

# ---------------- Actions ----------------
def add_word():
    w = st.session_state.word_input.strip()
    p = st.session_state.pron_input.strip()
    d = st.session_state.def_input.strip()

    if not w or not p or not d:
        st.toast("⚠️ กรอกข้อมูลให้ครบ")
        return

    st.session_state.vocab.append({"word":w,"pron":p,"def":d})
    st.toast(f"✅ เพิ่ม: {w}")
    st.session_state.word_input=""
    st.session_state.pron_input=""
    st.session_state.def_input=""


def delete_word(index):
    word = st.session_state.vocab[index]["word"]
    st.session_state.vocab.pop(index)
    st.toast(f"🗑 ลบ: {word}")


def start_edit(index):
    st.session_state.edit_index = index


def save_edit():
    idx = st.session_state.edit_index
    st.session_state.vocab[idx] = {
        "word": st.session_state.edit_w,
        "pron": st.session_state.edit_p,
        "def": st.session_state.edit_d
    }
    st.toast("✏️ แก้ไขสำเร็จ")
    st.session_state.edit_index = None

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# A-Z Navigation
st.markdown("<div class='az-nav'>" + " ".join([f"<a href='#{l}'>{l}</a>" for l in string.ascii_uppercase]) + "</div>", unsafe_allow_html=True)

# Sidebar Add
st.sidebar.header("➕ Add")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Pronunciation", key="pron_input")
st.sidebar.text_input("Definition", key="def_input")
st.sidebar.button("Add", on_click=add_word)

# Display
st.subheader("📖 Vocabulary")

sorted_vocab = merge_sort(st.session_state.vocab)

if sorted_vocab:
    grouped={}
    for i,v in enumerate(sorted_vocab):
        letter=v["word"][0].upper()
        grouped.setdefault(letter,[]).append((i,v))

    for letter in string.ascii_uppercase:
        if letter in grouped:
            st.markdown(f"<div id='{letter}' class='section'><h3>{letter}</h3></div>", unsafe_allow_html=True)

            for idx,v in grouped[letter]:
                if st.session_state.edit_index == idx:
                    col1,col2,col3 = st.columns(3)
                    with col1:
                        st.text_input("", value=v['word'], key="edit_w")
                    with col2:
                        st.text_input("", value=v['pron'], key="edit_p")
                    with col3:
                        st.text_input("", value=v['def'], key="edit_d")
                    st.button("Save", on_click=save_edit)
                else:
                    col1,col2,col3 = st.columns([4,2,1])
                    with col1:
                        st.markdown(f"**{v['word']}** ({v['pron']})")
                    with col2:
                        st.markdown(v['def'])
                    with col3:
                        if st.button("✏️", key=f"edit{idx}"):
                            start_edit(idx)
                        if st.button("🗑", key=f"del{idx}"):
                            delete_word(idx)

else:
    st.info("No vocabulary yet")

st.markdown("---")
st.write(f"Total: {len(st.session_state.vocab)}")