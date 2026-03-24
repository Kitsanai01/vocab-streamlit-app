import streamlit as st
import string

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="wide")

# ---------------- Style ----------------
st.markdown("""
<style>
html { scroll-behavior: smooth; }

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

</style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

if "search_result" not in st.session_state:
    st.session_state.search_result = None

if "search_not_found" not in st.session_state:
    st.session_state.search_not_found = False

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
def search_word_fn():
    target = st.session_state.search_input.strip()
    sorted_vocab = merge_sort(st.session_state.vocab)

    idx = binary_search(sorted_vocab, target)

    if idx != -1:
        st.session_state.search_result = sorted_vocab[idx]["word"]
        st.session_state.search_not_found = False
    else:
        st.session_state.search_result = None
        st.session_state.search_not_found = True

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
        st.toast(f"✅ เพิ่ม: '{w}' เรียบร้อยแล้ว")
        st.session_state.word_input=""
        st.session_state.pron_input=""
        st.session_state.def_input=""

def delete_word():
    dw = st.session_state.del_input.strip()
    before=len(st.session_state.vocab)

    st.session_state.vocab=[v for v in st.session_state.vocab if v["word"].lower()!=dw.lower()]

    if len(st.session_state.vocab)<before:
        st.toast(f"🗑 ลบ: '{dw}' เรียบร้อยแล้ว")
        st.session_state.del_input=""
    else:
        st.toast(f"❌ ไม่พบ '{dw}'")

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# 🔍 Search
st.subheader("🔍 Search")
st.text_input("Search word", key="search_input")
st.button("Search", on_click=search_word_fn)

# ❗ แสดงข้อความถ้าไม่เจอ
if st.session_state.search_not_found:
    st.error("❌ ไม่พบคำศัพท์นี้ในระบบ")

# Sidebar
st.sidebar.header("➕ Add Vocabulary")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Pronunciation", key="pron_input")
st.sidebar.text_input("Definition", key="def_input")
st.sidebar.button("Add", on_click=add_word)

st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete")
st.sidebar.text_input("Word to delete", key="del_input")
st.sidebar.button("Delete", on_click=delete_word)

# A-Z Navigation
st.markdown("<div class='az-nav'>" + " ".join([f"<a href='#{l}'>{l}</a>" for l in string.ascii_uppercase]) + "</div>", unsafe_allow_html=True)

# ---------------- Display ----------------
st.markdown("---")

sorted_vocab = merge_sort(st.session_state.vocab)

if st.session_state.vocab:
    grouped={}
    for v in sorted_vocab:
        first=v["word"][0].upper()
        if not first.isalpha(): first="#"
        grouped.setdefault(first,[]).append(v)

    for letter in string.ascii_uppercase:
        if letter in grouped:
            st.markdown(f"<div id='{letter}' class='section'><h3>{letter}</h3></div>", unsafe_allow_html=True)

            for v in grouped[letter]:
                highlight = ""
                scroll_id = ""

                # ⭐ highlight + scroll target
                if st.session_state.search_result == v["word"]:
                    highlight = "highlight"
                    scroll_id = f"id='target-word'"

                st.markdown(f"""
                <div {scroll_id} class='card {highlight}'>
                    <div class='word-block'>
                        <div class='word'>{v['word']}</div>
                        <div class='pron'>{v.get('pron','')}</div>
                    </div>
                    <div class='meaning'>{v['def']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ⭐ scroll ไปคำที่เจอ
    if st.session_state.search_result:
        st.markdown("""
        <script>
        const el = window.parent.document.getElementById("target-word");
        if(el){
            el.scrollIntoView({behavior:"smooth", block:"center"});
        }
        </script>
        """, unsafe_allow_html=True)

else:
    st.info("No vocabulary yet")

st.write(f"📊 Total: {len(st.session_state.vocab)}")