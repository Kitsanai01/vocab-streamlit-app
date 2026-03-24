import streamlit as st

st.set_page_config(page_title="Vocabulary Manager", page_icon="📚", layout="centered")

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

# ---------------- UI ----------------
st.title("📚 Vocabulary Manager")

# Sidebar
st.sidebar.header("➕ Add Vocabulary")
word = st.sidebar.text_input("Word")
definition = st.sidebar.text_input("Definition")

if st.sidebar.button("Add"):
    if word and definition:
        if any(v["word"].lower() == word.lower() for v in st.session_state.vocab):
            st.sidebar.warning("Word already exists")
        else:
            st.session_state.vocab.append({"word": word, "def": definition})
            st.sidebar.success("Added successfully")
    else:
        st.sidebar.warning("Please fill all fields")

st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete Vocabulary")
del_word = st.sidebar.text_input("Word to delete")
if st.sidebar.button("Delete"):
    before = len(st.session_state.vocab)
    st.session_state.vocab = [v for v in st.session_state.vocab if v["word"].lower() != del_word.lower()]
    if len(st.session_state.vocab) < before:
        st.sidebar.success("Deleted")
    else:
        st.sidebar.error("Not found")

# Main display
st.subheader("📖 Vocabulary List")

if st.session_state.vocab:
    for i, v in enumerate(st.session_state.vocab, 1):
        st.write(f"**{i}. {v['word']}** — {v['def']}")
else:
    st.info("No vocabulary yet")

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
st.write(f"Total words: {len(st.session_state.vocab)}")