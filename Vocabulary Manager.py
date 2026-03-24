import streamlit as st

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="centered")

# ---------------- Style ----------------
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 10px; height: 3em; width: 100%; background-color: #4CAF50; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #45a049; }
    .card { padding: 15px; border-radius: 10px; background-color: #1c1f26; margin-bottom: 10px; }
    .section { margin-top: 20px; padding: 10px; border-left: 5px solid #4CAF50; background-color: #111318; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
if "vocab" not in st.session_state:
    st.session_state.vocab = []

# ---------------- Functions ----------------
def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j]["word"].lower() > key["word"].lower():
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]["word"].lower() <= right[j]["word"].lower():
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid]["word"].lower() == target.lower():
            return mid
        elif target.lower() < arr[mid]["word"].lower():
            hi = mid - 1
        else:
            lo = mid + 1
    return -1

# ---------------- Callbacks ----------------
def add_word():
    word = st.session_state.word_input
    definition = st.session_state.def_input

    if word and definition:
        if any(v["word"].lower() == word.lower() for v in st.session_state.vocab):
            st.sidebar.warning("Word already exists")
        else:
            st.session_state.vocab.append({"word": word, "def": definition})
            st.sidebar.success("Added successfully")
            st.session_state.word_input = ""
            st.session_state.def_input = ""
    else:
        st.sidebar.warning("Please fill all fields")


def delete_word():
    del_word = st.session_state.del_input
    before = len(st.session_state.vocab)

    st.session_state.vocab = [
        v for v in st.session_state.vocab
        if v["word"].lower() != del_word.lower()
    ]

    if len(st.session_state.vocab) < before:
        st.sidebar.success("Deleted")
        st.session_state.del_input = ""
    else:
        st.sidebar.error("Not found")

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")
st.caption("Organized A-Z with modern UI ✨")

# Sidebar
st.sidebar.header("➕ Add Vocabulary")
st.sidebar.text_input("Word", key="word_input")
st.sidebar.text_input("Definition", key="def_input")
st.sidebar.button("Add", on_click=add_word, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete Vocabulary")
st.sidebar.text_input("Word to delete", key="del_input")
st.sidebar.button("Delete", on_click=delete_word, use_container_width=True)

# Sorting
st.markdown("---")
st.subheader("🔄 Sorting")
col1, col2 = st.columns(2)

with col1:
    if st.button("Insertion Sort"):
        st.session_state.vocab = insertion_sort(st.session_state.vocab)
        st.success("Sorted using Insertion Sort")

with col2:
    if st.button("Merge Sort"):
        st.session_state.vocab = merge_sort(st.session_state.vocab)
        st.success("Sorted using Merge Sort")

# Display grouped A-Z
st.markdown("---")
st.subheader("📖 Vocabulary (A-Z)")

if st.session_state.vocab:
    sorted_vocab = merge_sort(st.session_state.vocab)
    grouped = {}

    for v in sorted_vocab:
        first_letter = v["word"][0].upper()
        if first_letter not in grouped:
            grouped[first_letter] = []
        grouped[first_letter].append(v)

    for letter in sorted(grouped.keys()):
        st.markdown(f"""
        <div class="section">
            <h3>🔤 {letter}</h3>
        </div>
        """, unsafe_allow_html=True)

        for v in grouped[letter]:
            st.markdown(f"""
            <div class="card">
                <b>{v['word']}</b><br>
                <span style='color:#9ca3af'>{v['def']}</span>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No vocabulary yet")

# Search
st.markdown("---")
st.subheader("🔍 Search")
search_word = st.text_input("Enter word to search")

if st.button("Search"):
    sorted_vocab = merge_sort(st.session_state.vocab)
    idx = binary_search(sorted_vocab, search_word)
    if idx != -1:
        st.success(f"Found: {sorted_vocab[idx]['word']} — {sorted_vocab[idx]['def']}")
    else:
        st.error("Word not found")

# Footer
st.markdown("---")
st.write(f"📊 Total words: {len(st.session_state.vocab)}")