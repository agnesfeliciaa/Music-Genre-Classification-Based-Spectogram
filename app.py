import streamlit as st
import os
from utils import auth, gambar_tools, model_utils
import time

# ----------------------------
# Mapping global: deskripsi + rekomendasi YouTube
# ----------------------------
genre_info = {
    "blues": {
        "description": (
            "Blues adalah genre musik yang penuh emosi dan sering kali menampilkan melodi lambat dengan lirik yang dalam. Biasanya menggunakan gitar, harmonika, dan vokal ekspresif. "
            "Blues lahir dari jeritan hati yang terdalam. Berasal dari komunitas Afrika-Amerika di Selatan Amerika Serikat pada awal abad ke-20, blues adalah suara dari jiwa yang terluka namun tetap berharap. Dengan struktur akord yang sederhana dan lirik yang menyentuh, blues mengubah rasa sakit menjadi keindahan. "
            "Setiap petikan gitarnya seperti merangkai kisah—tentang cinta yang hilang, perjuangan hidup, dan kerinduan yang mendalam. Tak hanya sebagai musik, blues adalah teman saat sunyi, pelipur lara saat beban terasa berat. "
            "Blues menenangkan pikiran. Waktunya refleksi diri. Rasakan emosinya, bukan sekadar dengar nadanya. "
        ),
        "videos": [
            ("B.B. King – The Thrill Is Gone",        "https://www.youtube.com/watch?v=oica5jG7FpU"),
            ("Elton John - I Guess That's Why They Call It The Blues",    "https://youtu.be/h6KYAVn8ons?si=PCEg1eW0Wo1YhAft"),
            ("Muddy Waters – Mannish Boy",             "https://www.youtube.com/watch?v=8hEYwk0bypY"),
        ]
    },
    "classical": {
        "description": (
            "Musik Klasik adalah genre dengan struktur komposisi kompleks, sering menggunakan orkestra besar dari periode Baroque hingga Modern. "
            "Musik Klasik bukan sekadar alunan nada, tapi karya agung lintas zaman. Dari era Baroque yang megah, Romantik yang penuh gejolak, hingga modern yang penuh eksperimen, musik klasik adalah dunia yang kaya akan detail, teknik, dan emosi. "
            "Bayangkan orkestra besar membawakan simfoni karya Beethoven, atau dentingan piano Mozart mengalun lembut. Musik klasik membuka pintu menuju ketenangan batin, meningkatkan konsentrasi, dan memperkaya jiwa. "
            "Musik klasik cocok untuk meningkatkan fokus dan ketenangan. Ini adalah seni yang tidak lekang oleh waktu. "
        ),
        "videos": [
            ("Beethoven - Moonlight Sonata",           "https://youtu.be/4Tr0otuiQuU?si=b4E0uC6uebayvKYy"),
            ("Mozart – Symphony No.40",                "https://www.youtube.com/watch?v=JTc1mDieQI8"),
            ("Chopin - Nocturne op.9 No.2",            "https://youtu.be/9E6b3swbnWg?si=vZQUu8W7P4aZDu3a"),
        ]
    },
    "country": {
        "description": (
            "Country adalah genre yang berkembang di pedesaan AS, dikenal dengan gitar akustik, banjo, dan tema kehidupan sederhana. "
            "Country adalah suara dari padang rumput yang luas dan hati yang jujur. Genre ini membawamu ke jalan tanah berdebu, ke kehidupan sederhana namun penuh makna di pedesaan. Gitar akustik, banjo, dan harmonika berpadu menyampaikan cerita cinta, kehilangan, keluarga, dan impian. "
            "Country menyuguhkan nostalgia yang hangat—seolah duduk di teras rumah dengan secangkir kopi sambil mengingat masa lalu. "
            "Country membawa suasana tenang dan hangat. Dengarkan dan rasakan rumah di setiap nadanya. "
        ),
        "videos": [
            ("Taylor Swift - You Belong With Me",      "https://youtu.be/VuNIsY6JdUw?si=hZqX8U3d3jxrr346"),
            ("Dolly Parton – Jolene",                  "https://www.youtube.com/watch?v=Ixrje2rXLMA"),
            ("Sugarland - Stay",                       "https://youtu.be/zPG1n1B0Ydw?si=BdNdJ4I1GMzyXiv8"),
        ]
    },
    "disco": {
        "description": (
            "Disco adalah genre dansa tahun 1970-an dengan beat kuat, bass dominan, dan penggunaan synthesizer. "
            "Disco adalah ledakan warna dan semangat. Lahir di akhir 70-an, disco mendominasi klub malam dengan dentuman ritme yang menggoda dan lampu disko yang berputar tiada henti. "
            "Dengan beat yang groovy, synth yang funky, dan lirik penuh keceriaan, disco mengajak semua untuk bangkit, menari, dan melupakan sejenak dunia luar. "
            "Saatnya bergoyang! Disco penuh energi dan kebebasan. Ini bukan hanya musik, tapi perayaan hidup. "
        ),
        "videos": [
            ("Bee Gees – Stayin' Alive",               "https://www.youtube.com/watch?v=I_izvAbhExY"),
            ("Donna Summer – Hot Stuff",               "https://www.youtube.com/watch?v=1IdEhvuNxV8"),
            ("Chic – Le Freak",                        "https://www.youtube.com/watch?v=h1qQ1SKNlgY"),
        ]
    },
    "hiphop": {
        "description": (
            "Hip-Hop adalah budaya yang mencakup rap, DJing, dan breakdance, lahir di Bronx pada 1970-an dengan beat dan lirik protes. "
            "Hip-Hop adalah suara perlawanan, ekspresi diri, dan budaya yang tak bisa diabaikan. Lahir dari jalanan Bronx, hip-hop tumbuh menjadi gerakan global—menggabungkan rap, beat, breakdance, hingga seni visual graffiti. "
            "Dengan lirik yang tajam dan ritme yang intens, hip-hop menyuarakan kenyataan yang tak semua orang berani ungkapkan: ketidakadilan, identitas, dan mimpi besar dari tempat kecil. "
            "Hip-Hop membakar semangatmu! Ini adalah musik yang berbicara lantang. Bergeraklah, suarakan dirimu!"
        ),
        "videos": [
            ("Tupac – California Love",                "https://www.youtube.com/watch?v=5wBTdfAkqGU"),
            ("The Notorious B.I.G. – Juicy",           "https://www.youtube.com/watch?v=_JZom_gVfuw"),
            ("Kendrick Lamar – HUMBLE.",               "https://www.youtube.com/watch?v=tvTRZJ-4EyI"),
        ]
    },
    "jazz": {
        "description": (
            "Jazz adalah genre dengan improvisasi tinggi, berakar pada blues dan ragtime, populer sejak awal abad ke-20. "
            "Jazz adalah kebebasan dalam bentuk suara. Lahir di New Orleans dari perpaduan budaya Afro-Amerika, jazz merayakan improvisasi, spontanitas, dan interaksi musikal. Setiap pertunjukan jazz adalah unik, penuh kejutan, dan hidup. "
            "Dengan permainan solo yang menawan, harmoni yang kaya, dan groove yang mengalir, jazz membawa pendengarnya menjelajah emosi tanpa batas. "
            "Jazz adalah alunan kebebasan. Nikmati momentumnya. Biarkan dirimu hanyut dalam arusnya."
        ),
        "videos": [
            ("Miles Davis – So What",                  "https://www.youtube.com/watch?v=zqNTltOGh5c"),
            ("John Coltrane – My Favorite Things",     "https://www.youtube.com/watch?v=qWG2dsXV5HI"),
            ("Louis Armstrong – What a Wonderful World","https://youtu.be/rBrd_3VMC3c?si=ooIOHjLbAqRE_cn0"),
        ]
    },
    "metal": {
        "description": (
            "Metal adalah genre keras dengan distorsi gitar kuat, vokal intens, dan tema pemberontakan. "
            "Metal adalah ledakan emosi yang liar dan jujur. Lahir dari akar hard rock dan berkembang menjadi kekuatan mentah, metal dikenal lewat distorsi gitar, double pedal drum, dan vokal yang mengguncang jiwa. "
            "Ini bukan sekadar suara keras—metal adalah pelarian bagi yang merasa terasing, perjuangan bagi yang lelah berdiam, dan kekuatan bagi yang ingin bangkit. "
            "Metal keras dan berani. Hadapi tantanganmu dengan kepala tegak. Ini musik bagi jiwa yang tak pernah menyerah. "
        ),
        "videos": [
            ("Metallica – Enter Sandman",              "https://www.youtube.com/watch?v=CD-E-LDc384"),
            ("System Of A Down - Chop Suey",         "https://youtu.be/CSvFpBOe8eY?si=Zd1h5BxG_K-ifNf3"),
            ("Black Sabbath – Paranoid",               "https://www.youtube.com/watch?v=0qanF-91aJo"),
        ]
    },
    "pop": {
        "description": (
            "Pop adalah genre ringan dan catchy, mengutamakan melodi mudah diingat dan lirik universal. "
            "Pop adalah musik yang menyatukan dunia. Dengan melodi yang catchy, produksi yang bersih, dan lirik yang mudah diingat, pop mengisi hari-hari kita dengan semangat, cinta, dan kesenangan. "
            "Dari cinta pertama hingga patah hati, dari pesta hingga waktu tenang di kamar, pop selalu ada. Pop terus berevolusi, mengikuti zaman, tapi selalu punya satu tujuan: membuatmu merasa lebih baik. "
            "Pop menyenangkan dan ringan. Tetap positif dan berdansa dalam hidup."
        ),
        "videos": [
            ("Michael Jackson – Billie Jean",          "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"),
            ("Taylor Swift – Shake It Off",            "https://www.youtube.com/watch?v=nfWlot6h_JM"),
            ("Dua Lipa – Levitating",                  "https://www.youtube.com/watch?v=TUVcZfQe-Kw"),
        ]
    },
    "reggae": {
        "description": (
            "Reggae lahir di Jamaika tahun 1960-an, dikenal dengan ritme offbeat santai dan lirik damai. "
            "Reggae adalah denyut kehidupan yang damai dan merdeka. Berasal dari Jamaika, reggae mengajarkan cinta, perjuangan tanpa kekerasan, dan persatuan lewat irama santai dan lirik penuh makna. "
            "Musik ini bukan hanya untuk didengar, tapi dirasakan—dengan tubuh yang rileks dan hati yang terbuka. "
            "Reggae menenangkan dan santai. Chill out dan biarkan dunia berjalan tanpa terburu-buru."
        ),
        "videos": [
            ("Bob Marley – No Woman No Cry",           "https://youtu.be/IT8XvzIfi4U?si=zC8J0ZOZSTKPQxF3"),
            ("Jimmy Cliff – The Harder They Come",     "https://youtu.be/pmc5H6zAi6M?si=tPq1OGuO00OPvicN"),
            ("Peter Tosh – Legalize It",               "https://youtu.be/w_C2m6E367M?si=jhoWwJ0zVoaOiIs2"),
        ]
    },
    "rock": {
        "description": (
            "Rock adalah genre energik dengan gitar elektrik, bass, drum, dan vokal kuat. "
            "Rock adalah jiwa pemberontakan yang hidup dalam setiap nada. Dari akar blues hingga cabang grunge dan alternatif, rock adalah suara mereka yang ingin bebas, yang berani berbeda. "
            "Gitar menggeram, drum menghentak, dan vokal membara. Rock menyalakan api dalam diri, memberi energi untuk melawan arus dan berkata: “Ini aku, dan aku tak akan tunduk.” "
            "Rock penuh semangat dan kebebasan. Kamu bisa! Hiduplah dengan irama yang kamu pilih."
        ),
        "videos": [
            ("Queen – Bohemian Rhapsody",              "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"),
            ("Nirvana – Smells Like Teen Spirit",      "https://www.youtube.com/watch?v=hTWKbfoikeg"),
            ("AC/DC – Back In Black",                  "https://www.youtube.com/watch?v=pAgnJDJN4VA"),
        ]
    },
}

# ----------------------------
# Inisialisasi Model & Folder
# ----------------------------
if "model" not in st.session_state:
    st.session_state.model = model_utils.load_model_from_file("music_genre.h5")

UPLOAD_FOLDER = "uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
st.set_page_config(page_title="🎵 Music Genre Classifier", layout="centered")

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None

# menu = ["Login", "Register"] if not st.session_state.logged_in else ["Home", "Profile", "Logout"]
menu = ["Login", "Register"] if not st.session_state.logged_in else ["Home", "Profile", "Evaluasi Model", "Logout"]

choice = st.sidebar.selectbox("Menu", menu)

# ----------------------------
# Register
# ----------------------------
if choice == "Register":
    st.title("🔐 Registrasi Akun Baru")
    username = st.text_input("Username")
    email    = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm  = st.text_input("Konfirmasi Password", type="password")
    if st.button("Register"):
        ok, msg = auth.register_user(username, email, password, confirm)
        if ok:
            st.success(msg)
            st.info("Silakan lanjut login.")
        else:
            st.error(msg)

# ----------------------------
# Login
# ----------------------------
elif choice == "Login":
    st.title("🔑 Login Pengguna")
    email    = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if auth.login_user(email, password):
            user = auth.load_users()[email]
            st.session_state.logged_in = True
            st.session_state.username  = user["username"]
            st.session_state.email     = email
            st.success(f"Selamat datang, {user['username']}!")
            st.rerun()
        else:
            st.error("Email atau password salah.")

# ----------------------------
# Home
# ----------------------------
elif choice == "Home" and st.session_state.logged_in:
    
    st.title("🎧 Klasifikasi Genre dari Gambar Spectrogram")
    st.write(f"Hai, **{st.session_state.username}**! Unggah spektrogram (.png).")

    uploaded = st.file_uploader("Unggah file", type=["png"])
    if uploaded:
        path = os.path.join(UPLOAD_FOLDER, uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.read())

        st.subheader("🔎 Visualisasi Spectrogram")
        st.image(path, use_container_width=True)

        st.subheader("🧠 Hasil Prediksi Genre")
        pred, prob = model_utils.predict_genre_with_probability(path, st.session_state.model)

        # Kotak biru hasil prediksi
        st.markdown(
            "<div style='background-color:#f0f8ff;padding:15px;border:2px solid #6fa3ef;border-radius:10px;"
            "font-weight:bold;text-align:center;color:#005b99;'>"
            f"🎶 Genre Terdeteksi: {pred} ({prob*100:.2f}%)"
            "</div><br>",
            unsafe_allow_html=True
        )

        # Kotak merah probabilitas
        st.markdown(
            "<div style='background-color:#fff0f0;padding:15px;border:2px solid #ff6f6f;border-radius:10px;"
            "font-weight:bold;text-align:center;color:#cc0000;'>"
            f"🔢 Probabilitas: {prob*100:.2f}%"
            "</div><br>",
            unsafe_allow_html=True
        )

        st.subheader("🔋 Proses Prediksi")
        p = st.progress(0)
        for i in range(100):
            p.progress(i+1)
            time.sleep(0.01)
        st.success("Proses Prediksi Selesai!")

        # Normalisasi key dan lookup
        key = pred.strip().lower().replace(" ", "").replace("-", "")
        info = genre_info.get(key)

        if info:
            # HTML kotak biru besar
            html = (
                "<div style='background-color:#e6f7ff;border:2px solid #6fa3ef;"
                "border-radius:10px;padding:20px;margin-top:20px;'>"
                "<h4 style='margin:0;color:#005b99;'>ℹ️ Tentang Genre Ini</h4>"
                f"<p style='color:#003366; text-align:justify;'>{info['description']}</p>"
                "<h4 style='margin-top:10px;color:#005b99;'>📺 Rekomendasi Video YouTube</h4>"
                "<div style='display:flex;gap:10px;justify-content:center;'>"
            )
            for title, url in info["videos"]:
                vid = url.split("v=")[-1]
                html += (
                    "<div style='flex:1;text-align:center;'>"
                    f"<a href='{url}' target='_blank' style='text-decoration:none;'>"
                    f"<img src='https://img.youtube.com/vi/{vid}/0.jpg' "
                    "style='width:100%;border-radius:8px;' />"
                    f"<p style='margin:5px 0 0;color:#003366;font-weight:bold;'>{title}</p>"
                    "</a></div>"
                )
            html += "</div></div>"

            # render HTML
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning(f"Tidak ada rekomendasi untuk genre: {pred}")

# ----------------------------
# Profile
# ----------------------------
elif choice == "Profile" and st.session_state.logged_in:
    st.title("👤 Profil Pengguna")
    st.write(f"Email: **{st.session_state.email}**")
    new_name = st.text_input("Ubah Username", value=st.session_state.username)
    if st.button("Simpan Perubahan"):
        if auth.update_username(st.session_state.email, new_name):
            st.session_state.username = new_name
            st.success("Username berhasil diperbarui!")
        else:
            st.error("Gagal memperbarui username.")

# ----------------------------
# Logout
# ----------------------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username  = None
    st.session_state.email     = None
    st.success("Berhasil logout.")
    st.rerun()

# ----------------------------
# Evaluasi Model
# ----------------------------
elif choice == "Evaluasi Model" and st.session_state.logged_in:
    st.title("📊 Evaluasi Akurasi Model")

    test_folder = st.text_input("Masukkan path folder dataset uji (berisi subfolder genre):", "test_data")

    if st.button("Evaluasi Sekarang"):
        with st.spinner("Evaluasi model..."):
            class_labels = list(genre_info.keys())
            report, acc = model_utils.evaluate_model_on_folder(st.session_state.model, test_folder, class_labels)

        st.subheader("✅ Akurasi Keseluruhan")
        st.success(f"{acc * 100:.2f}%")

        st.subheader("📋 Precision, Recall, F1-score per Genre")
        for label in genre_info.keys():
            if label in report:
                st.markdown(f"**{label.capitalize()}**")
                st.write({
                    "Precision": f"{report[label]['precision']:.2f}",
                    "Recall": f"{report[label]['recall']:.2f}",
                    "F1-score": f"{report[label]['f1-score']:.2f}",
                    "Support": int(report[label]['support']),
                })

        st.subheader("📊 Rata-rata Makro")
        avg = report["macro avg"]
        st.info(
            f"Precision: {avg['precision']:.2f} | Recall: {avg['recall']:.2f} | F1-score: {avg['f1-score']:.2f}"
        )
