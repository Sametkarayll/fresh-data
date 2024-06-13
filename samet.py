import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Excel dosyasını yükle
excel_path = "bilisim23.xlsx"
data = pd.read_excel(excel_path)
df = pd.DataFrame(data)
df=df.drop(columns=["Unnamed: 0.1","Unnamed: 0"])
# CSS Stili
st.markdown(
    """
    <style>
    body {
        background-color: #add8e6; /* Ana arka plan rengi */
        color: #ADD8E6;
    }
    .sidebar {
        background-color: #4b8baf; /* Menü arka plan rengi */
        padding: 20px;
        border-right: 1px solid #ccc;
        height: 100vh;
    }
    .main-content {
        padding: 20px;
    }
    .stButton button {
        padding: 15px 30px;
        font-size: 18px;
        background-color: #00008B;
        color: #ADD8E6;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .stButton button:hover {
        background-color: #00008B;
    }
    .dataframe tbody tr th {
        font-size: 20px; /* Tablo başlıkları için yazı boyutu */
    }
    .dataframe tbody tr td {
        font-size: 18px; /* Tablo içeriği için yazı boyutu */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sol Menü
st.sidebar.title('Menü')

# Menü Butonları
if st.sidebar.button('Top 20', key='section1'):
    st.subheader('En Çok İstihdam Edilen 20 Pozisyon')
    most_common_positions = data['Pozisyon'].value_counts().head(20)
    st.dataframe(most_common_positions)

# 'Grafikler' ve 'Bireysel Grafik' butonlarının durumunu koruyacak şekilde ayarla
if 'grafikler_tiklandi_mi' not in st.session_state:
    st.session_state.grafikler_tiklandi_mi = False

if 'bireysel_grafik_tiklandi_mi' not in st.session_state:
    st.session_state.bireysel_grafik_tiklandi_mi = False

if st.sidebar.button('Grafikler', key='section2'):
    st.session_state.grafikler_tiklandi_mi = not st.session_state.grafikler_tiklandi_mi

# Eğer Grafikler butonuna tıklandıysa, Grafik 1 ve Grafik 2 butonlarını göster
if st.session_state.grafikler_tiklandi_mi:
    if st.sidebar.button('Meslek İstatistikleri', key='section5'):
        st.session_state.bireysel_grafik_tiklandi_mi = not st.session_state.bireysel_grafik_tiklandi_mi

    if st.session_state.bireysel_grafik_tiklandi_mi:
        st.subheader('')
        st.write('')

        # Kullanıcıdan meslek girişi al
        input_pozisyon_bireysel = st.text_input("Bireysel grafik oluşturmak istediğiniz mesleği giriniz: ")

        # Belirtilen pozisyona göre filtreleme
        df_filtered_bireysel = df[df['Pozisyon'] == input_pozisyon_bireysel]

        if df_filtered_bireysel.empty:
            st.write(f"{input_pozisyon_bireysel} pozisyonu için veri bulunamadı.")
        else:
            # Tarihe göre sayıları almak
            yearly_counts_bireysel = df_filtered_bireysel['Tarih'].value_counts().sort_index()

            # Çalışma şekillerini almak
            working_style_counts_bireysel = df_filtered_bireysel['Calisma Sekli'].value_counts()

            # Grafikleri çizme
            col1_bireysel, col2_bireysel = st.columns(2)

            # Yıllık sayılar grafiği
            with col1_bireysel:
                st.subheader(f'{input_pozisyon_bireysel} Pozisyonunun Yıllara Göre Sayısı')
                plt.figure(figsize=(10, 6))
                sns.barplot(x=yearly_counts_bireysel.index, y=yearly_counts_bireysel.values, palette='viridis')
                plt.xlabel('Yıl')
                plt.ylabel('Sayı')
                plt.xticks(rotation=45)
                st.pyplot(plt)

            # Çalışma şekilleri grafiği
            with col2_bireysel:
                st.subheader(f'{input_pozisyon_bireysel} Pozisyonunun Çalışma Şekilleri')
                plt.figure(figsize=(10, 6))
                sns.barplot(x=working_style_counts_bireysel.index, y=working_style_counts_bireysel.values, palette='viridis')
                plt.xlabel('Çalışma Şekli')
                plt.ylabel('Sayı')
                plt.xticks(rotation=45)
                st.pyplot(plt)

    if st.sidebar.button('Genel İstatistikler', key='section6'):
        st.subheader('')
        st.write('')
        
        #Grafik1
        st.set_option('deprecation.showPyplotGlobalUse', False)
        pozisyon_sayim = df['Pozisyon'].value_counts().head(10).reset_index()
        pozisyon_sayim.columns = ['Pozisyon', 'Sayım']
        en_cok_10_pozisyon = pozisyon_sayim['Pozisyon'].tolist()
        df_filtered = df[df['Pozisyon'].isin(en_cok_10_pozisyon)]
        konum_pozisyon_sayim = df_filtered.groupby(['Konum', 'Pozisyon']).size().reset_index(name='Sayım')

        plt.figure(figsize=(20, 10))
        sns.barplot(x='Konum', y='Sayım', hue='Pozisyon', data=konum_pozisyon_sayim)
        plt.title('Konuma Göre En Çok Bulunan 10 Pozisyon')
        plt.xlabel('Konum')
        plt.ylabel('Sayım')
        plt.legend(title='Pozisyon', loc='upper right')
        st.title('Konuma Göre En Çok Bulunan 10 Pozisyon')
        st.pyplot(plt)
        
        #Grafik2
        st.set_option('deprecation.showPyplotGlobalUse', False)
        pozisyon_sayim = df['Pozisyon'].value_counts().head(3).reset_index()
        pozisyon_sayim.columns = ['Pozisyon', 'Sayım']
        en_cok_10_pozisyon = pozisyon_sayim['Pozisyon'].tolist()
        df_filtered = df[df['Pozisyon'].isin(en_cok_10_pozisyon)]
        g = sns.FacetGrid(df_filtered, col='Pozisyon', col_wrap=3, height=4)
        g.map(sns.histplot, 'Konum')

        for ax in g.axes.flatten():
            for label in ax.get_xticklabels():
                label.set_rotation(90)
                label.set_ha('right')

        g.add_legend()
        plt.subplots_adjust(top=1)
        plt.suptitle('Pozisyonlara Göre Konum Dağılımları')
        st.title('Pozisyonlara Göre Konum Dağılımları')
        st.pyplot(plt)

        #Grafik3
        st.set_option('deprecation.showPyplotGlobalUse', False)
        meslekler = df['Pozisyon'].value_counts().head(10).index.tolist()
        plt.figure(figsize=(14, 8))
        for meslek in meslekler:
            meslek_df = df[df['Pozisyon'] == meslek]
            yil_sayim = meslek_df['Tarih'].value_counts().sort_index().reset_index()
            yil_sayim.columns = ['Tarih', 'Sayım']
            sns.lineplot(x='Tarih', y='Sayım', data=yil_sayim, label=meslek, marker='o')

        plt.title('Öne Çıkan Mesleklerin Yıllara Göre Dağılımı')
        plt.xlabel('Yıl')
        plt.ylabel('Sayım')
        plt.xticks(rotation=45)
        plt.legend(title='Pozisyon', loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        st.title('Öne Çıkan Mesleklerin Yıllara Göre Dağılımı')
        st.pyplot(plt)

        #Grafik4
        st.set_option('deprecation.showPyplotGlobalUse', False)
        top_10_meslek = df['Pozisyon'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        top_10_meslek.plot(kind='bar', ax=ax)
        plt.title('Öne Çıkan Mesleklerin Dağılımı')
        plt.xlabel('Meslek')
        plt.ylabel('Adet')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.title('Öne Çıkan Mesleklerin Dağılımı')
        st.pyplot(fig)

        #Grafik5
        st.set_option('deprecation.showPyplotGlobalUse', False)
        top_10_meslek = df['Pozisyon'].value_counts().head(10).index.tolist()
        filtered_df = df[df['Pozisyon'].isin(top_10_meslek)]
        meslekler_konum = filtered_df.groupby('Pozisyon')['Konum'].value_counts().unstack().fillna(0)
        st.title('En Çok Tekrar Eden 10 Mesleğin Konuma Göre Dağılımı')
        st.bar_chart(meslekler_konum)

        #Grafik6
        top_10_meslek = df['Pozisyon'].value_counts().head(10).index.tolist()
        filtered_df = df[df['Pozisyon'].isin(top_10_meslek)]
        meslekler_calisma_sekli = filtered_df.groupby('Pozisyon')['Calisma Sekli'].value_counts().unstack().fillna(0)
        st.title('Öne Çıkan Mesleklerin Çalışma Şekline Göre Dağılımı')
        st.bar_chart(meslekler_calisma_sekli)

if st.sidebar.button('Hakkımızda', key='section3'):
    st.write("Mehmet Hanifi Işık")
    st.write("Github: https://github.com/MehmetHanifi1")
    st.write("Linkedin:https://www.linkedin.com/in/hanifi-i%C5%9F%C4%B1k-0416bb291/ ")
    
    st.write("Abdulsamet Karayel")
    st.write("Github: https://github.com/SametKarayl23")
    st.write("Linkedin:https://www.linkedin.com/in/samet-i%C5%9F%C4%B1k-0536bb291/ ")
    
    st.write("Esra Sena Karaaslan")
    st.write("Github: https://github.com/SenaKaraslan44")
    st.write("Linkedin:https://www.linkedin.com/in/esra-i%C5%9F%C4%B1k-4456bb291/")
    
    st.write("Reyyan Erva Gökkaya")
    st.write("Github: https://github.com/Reyyanerva01")
    st.write("Linkedin:https://www.linkedin.com/in/reyyan-i%C5%9F%C4%B1k-0416bb291/")

if st.sidebar.button('Veriler', key='section4'):
    st.write('Veriler')
    st.write(df.head(2460))
