import streamlit as st
import string

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="wide")

# ---------------- Style ----------------
st.markdown("""
<style>
html {
    scroll-behavior: smooth;
}

.main { background-color: #0e1117; color: #ffffff; }

/* Sticky */
.sticky {
    position: sticky;
    top: 0;
    z-index: 999;
    background: rgba(14,17,23,0.9);
    backdrop-filter: blur(10px);
    padding: 10px;
}

/* Card */
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
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}

.word { font-size:18px; font-weight:600; color:#4CAF50; }
.pron { font-size:14px; color:#9ca3af; }

.meaning { color:#e5e7eb; }

.section {
    margin-top: 25px;
    padding: 8px;
    border-left: 5px solid #4CAF50;
    background-color: #111318;
    border-radius: 8px;
}

.section.active {
    border-left: 5px solid #FFD700;
    box-shadow: 0 0 15px rgba(255,215,0,0.6);
}

/* A-Z */
.az-nav a {
    margin: 4px;
    padding: 6px 10px;
    border-radius: 6px;
    background: #1c1f26;
    color: #9ca3af;
    text-decoration: none;
}

.az-nav a:hover {
    background: #4CAF50;
    color: white;
}

/* Highlight search */
.highlight {
    border:2px solid #4CAF50;
    box-shadow:0 0 15px #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

if "active_letter" not in st.session_state:
    st.session_state.active_letter = ""

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
        st.toast(f"❗ '{w}' มีอยู่แล้ว")
    else:
        st.session_state.vocab.append({"word":w,"pron":p,"def":d})
        st.toast(f"✅ เพิ่ม: {w}")
        st.session_state.word_input=""
        st.session_state.pron_input=""
        st.session_state.def_input=""

def delete_word():
    dw = st.session_state.del_input.strip()
    before=len(st.session_state.vocab)
    st.session_state.vocab=[v for v in st.session_state.vocab if v["word"].lower()!=dw.lower()]
    if len(st.session_state.vocab)<before:
        st.toast(f"🗑 ลบ: {dw}")
        st.session_state.del_input=""
    else:
        st.toast(f"❌ ไม่พบ '{dw}'")

def edit_word():
    target = st.session_state.edit_target.strip()
    for v in st.session_state.vocab:
        if v["word"].lower()==target.lower():
            if st.session_state.edit_word_input:
                v["word"]=st.session_state.edit_word_input
            if st.session_state.edit_pron_input:
                v["pron"]=st.session_state.edit_pron_input
            if st.session_state.edit_def_input:
                v["def"]=st.session_state.edit_def_input
            st.toast(f"✏️ แก้ไข: {target}")
            break

    st.session_state.edit_target=""
    st.session_state.edit_word_input=""
    st.session_state.edit_pron_input=""
    st.session_state.edit_def_input=""

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# ⭐ Sticky Search + A-Z
st.markdown("<div class='sticky'>", unsafe_allow_html=True)

search_word = st.text_input("🔍 Search (Realtime)")

# realtime search
sorted_vocab = merge_sort(st.session_state.vocab)
found_word = search_word.lower()

# A-Z
az_html = "<div class='az-nav'>"
for l in string.ascii_uppercase:
    az_html += f"<a href='#{l}' onclick=\"window.location.hash='{l}'\">{l}</a>"
az_html += "</div>"

st.markdown(az_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("➕ Add")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Pron", key="pron_input")
st.sidebar.text_input("Def", key="def_input")
st.sidebar.button("Add", on_click=add_word)

st.sidebar.header("🗑 Delete")
st.sidebar.text_input("Word", key="del_input")
st.sidebar.button("Delete", on_click=delete_word)

st.sidebar.header("✏️ Edit")
st.sidebar.text_input("Target", key="edit_target")
st.sidebar.text_input("New Word", key="edit_word_input")
st.sidebar.text_input("New Pron", key="edit_pron_input")
st.sidebar.text_input("New Def", key="edit_def_input")
st.sidebar.button("Edit", on_click=edit_word)

# ---------------- Display ----------------
st.markdown("---")

if st.session_state.vocab:
    grouped={}
    for v in sorted_vocab:
        first=v["word"][0].upper()
        if not first.isalpha(): first="#"
        grouped.setdefault(first,[]).append(v)

    for letter in string.ascii_uppercase:
        if letter in grouped:
            active_class = "active" if letter == st.session_state.active_letter else ""
            st.markdown(f"<div id='{letter}' class='section {active_class}'><h3>{letter}</h3></div>", unsafe_allow_html=True)

            for v in grouped[letter]:
                highlight = ""
                if search_word and search_word.lower() in v["word"].lower():
                    highlight = "highlight"

                st.markdown(f"""
                <div class='card {highlight}'>
                    <div>
                        <div class='word'>{v['word']}</div>
                        <div class='pron'>{v.get('pron','')}</div>
                    </div>
                    <div class='meaning'>{v['def']}</div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("No vocabulary yet")

st.write(f"📊 Total: {len(st.session_state.vocab)}")