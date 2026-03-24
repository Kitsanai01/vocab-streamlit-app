import streamlit as st
import string

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
html { scroll-behavior: smooth; }

.main { background-color: #0e1117; color: #ffffff; }

/* Sticky Top */
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
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
}

.word { color:#4CAF50; font-weight:600; }
.pron { color:#9ca3af; font-size:13px; }
.meaning { color:#e5e7eb; }

/* Section */
.section {
    margin-top: 25px;
    padding: 8px;
    border-left: 5px solid #4CAF50;
    background-color: #111318;
    border-radius: 8px;
}

/* Highlight */
.highlight {
    border:2px solid #4CAF50;
    box-shadow:0 0 10px #4CAF50;
}

/* Floating A-Z */
.floating-nav {
    position: fixed;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1000;
}
.floating-nav a {
    display:block;
    margin:4px 0;
    padding:5px 7px;
    font-size:12px;
    border-radius:5px;
    background:#1c1f26;
    color:#aaa;
    text-decoration:none;
}
.floating-nav a.active {
    background:#4CAF50;
    color:white;
}

/* Scroll Top */
.scroll-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #4CAF50;
    color: white;
    padding: 10px;
    border-radius: 50%;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

# ---------------- FUNCTIONS ----------------
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

# ---------------- CALLBACKS ----------------
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

# Sticky Search
st.markdown("<div class='sticky'>", unsafe_allow_html=True)
search_word = st.text_input("🔍 Search (Realtime)")
st.markdown("</div>", unsafe_allow_html=True)

sorted_vocab = merge_sort(st.session_state.vocab)

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

# ---------------- DISPLAY ----------------
st.markdown("---")

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
                highlight = "highlight" if search_word and search_word.lower() in v["word"].lower() else ""

                st.markdown(f"""
                <div class='card {highlight}'>
                    <div>
                        <div class='word'>{v['word']}</div>
                        <div class='pron'>{v.get('pron','')}</div>
                    </div>
                    <div class='meaning'>{v['def']}</div>
                </div>
                """, unsafe_allow_html=True)

# Floating A-Z + JS
st.markdown(f"""
<div class="floating-nav">
{''.join([f"<a href='#{l}' id='nav-{l}'>{l}</a>" for l in string.ascii_uppercase])}
</div>

<div class="scroll-top" onclick="window.scrollTo({{top:0, behavior:'smooth'}})">⬆</div>

<script>
window.addEventListener("scroll", function() {{
    let sections = document.querySelectorAll("[id]");
    let scrollPos = document.documentElement.scrollTop;

    let current = "";

    sections.forEach(sec => {{
        if (sec.offsetTop <= scrollPos + 100) {{
            current = sec.id;
        }}
    }});

    document.querySelectorAll(".floating-nav a").forEach(a => a.classList.remove("active"));

    if (current) {{
        let active = document.getElementById("nav-" + current);
        if (active) active.classList.add("active");
    }}
}});
</script>
""", unsafe_allow_html=True)

st.write(f"📊 Total: {len(st.session_state.vocab)}")