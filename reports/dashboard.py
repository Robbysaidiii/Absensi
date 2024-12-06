import streamlit as st

# Menampilkan halaman dashboard setelah login
def show_dashboard():
    st.title("Dashboard")
    st.write("Selamat datang di Dashboard!")
    st.write("Anda berhasil login.")

# Inisialisasi session state untuk login jika belum ada
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.experimental_rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"  # Mengarahkan pengguna ke halaman Home setelah logout
        st.experimental_rerun()

# Menentukan halaman login dan logout
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Halaman-halaman lainnya
dashboard = st.Page(
    "reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page(
    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
)
search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

# Routing halaman utama berdasarkan status login
if st.session_state.logged_in:
    # Menampilkan menu navigasi untuk pengguna yang sudah login
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    # Menampilkan halaman login jika belum login
    pg = st.navigation([login_page])

pg.run()
