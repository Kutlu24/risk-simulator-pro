# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 00:33:05 2025

@author: kutlu
"""

import streamlit as st
import pandas as pd

# 1. TEMEL VERİ VE AYARLAR (Önceki kodla aynı)
#---------------------------------------------------
data = {
    'Ülke': ['Yeni Zelanda', 'İzlanda', 'İsviçre', 'Uruguay', 'İrlanda', 'Kosta Rika', 'Şili', 'Avustralya', 
             'Kanada', 'Finlandiya', 'Portekiz', 'Malezya', 'Botsvana', 'Arjantin', 'Japonya', 'İtalya', 'Çin', 'Rusya', 'Hindistan'],
    'Coğrafi İzolasyon': [9, 10, 5, 7, 8, 7, 9, 9, 7, 4, 7, 6, 8, 9, 8, 6, 4, 3, 5],
    'Nükleer Risk': [10, 10, 10, 10, 10, 10, 10, 9, 6, 5, 6, 7, 10, 10, 7, 6, 5, 4, 6],
    'Politik Tarafsızlık': [10, 9, 10, 10, 10, 10, 8, 6, 4, 3, 5, 7, 9, 8, 5, 5, 3, 3, 6],
    'Ekonomik Dayanıklılık': [8, 7, 10, 7, 8, 6, 7, 9, 9, 8, 7, 8, 5, 3, 9, 7, 8, 5, 6],
    'İç Sosyal İstikrar': [9, 10, 10, 9, 9, 9, 6, 8, 9, 10, 8, 7, 8, 4, 9, 7, 6, 4, 6],
    'Altyapı ve Sağlık': [9, 9, 10, 8, 9, 7, 7, 9, 9, 10, 8, 8, 5, 6, 10, 9, 8, 7, 5],
    'Halkın Hazırlıklılığı': [6, 6, 10, 5, 5, 4, 5, 7, 6, 10, 5, 4, 3, 4, 8, 6, 7, 8, 5],
    'İklim Dayanıklılığı': [8, 6, 7, 9, 7, 8, 8, 7, 9, 7, 6, 7, 6, 9, 5, 5, 5, 8, 7],
    'Enerji Bağımsızlığı': [6, 10, 7, 8, 5, 8, 6, 9, 10, 7, 3, 8, 4, 7, 3, 2, 4, 9, 4],
    'Siber Güvenlik': [8, 8, 9, 6, 8, 5, 6, 9, 9, 9, 7, 7, 3, 5, 9, 8, 8, 6, 6],
    'Demografik Dayanıklılık': [8, 7, 6, 7, 8, 8, 7, 9, 9, 5, 4, 7, 8, 6, 2, 2, 3, 3, 9]
}
df = pd.DataFrame(data)

scenario_weights = {
    '1': {'name': 'Genel Dengeli Kriz', 'weights': {'Coğrafi İzolasyon': 0.15, 'Nükleer Risk': 0.15, 'Politik Tarafsızlık': 0.10, 'Ekonomik Dayanıklılık': 0.10, 'İç Sosyal İstikrar': 0.10, 'Altyapı ve Sağlık': 0.10, 'Halkın Hazırlıklılığı': 0.05, 'İklim Dayanıklılığı': 0.05, 'Enerji Bağımsızlığı': 0.05, 'Siber Güvenlik': 0.05, 'Demografik Dayanıklılık': 0.05}},
    '2': {'name': 'Rusya-NATO Çatışması', 'weights': {'Coğrafi İzolasyon': 0.25, 'Nükleer Risk': 0.25, 'Politik Tarafsızlık': 0.20, 'Ekonomik Dayanıklılık': 0.05, 'İç Sosyal İstikrar': 0.05, 'Altyapı ve Sağlık': 0.0, 'Halkın Hazırlıklılığı': 0.05, 'İklim Dayanıklılığı': 0.0, 'Enerji Bağımsızlığı': 0.10, 'Siber Güvenlik': 0.05, 'Demografik Dayanıklılık': 0.0}},
    '3': {'name': 'Çin-ABD Gerilimi (Ekonomi Krizi)', 'weights': {'Coğrafi İzolasyon': 0.15, 'Nükleer Risk': 0.05, 'Politik Tarafsızlık': 0.15, 'Ekonomik Dayanıklılık': 0.25, 'İç Sosyal İstikrar': 0.10, 'Altyapı ve Sağlık': 0.05, 'Halkın Hazırlıklılığı': 0.0, 'İklim Dayanıklılığı': 0.10, 'Enerji Bağımsızlığı': 0.05, 'Siber Güvenlik': 0.10, 'Demografik Dayanıklılık': 0.0}},
    '4': {'name': 'Hürmüz Krizi (Enerji Şoku)', 'weights': {'Coğrafi İzolasyon': 0.10, 'Nükleer Risk': 0.0, 'Politik Tarafsızlık': 0.05, 'Ekonomik Dayanıklılık': 0.20, 'İç Sosyal İstikrar': 0.15, 'Altyapı ve Sağlık': 0.05, 'Halkın Hazırlıklılığı': 0.0, 'İklim Dayanıklılığı': 0.10, 'Enerji Bağımsızlığı': 0.30, 'Siber Güvenlik': 0.0, 'Demografik Dayanıklılık': 0.05}},
    '5': {'name': 'İklim Krizi ve Su Savaşları', 'weights': {'Coğrafi İzolasyon': 0.15, 'Nükleer Risk': 0.0, 'Politik Tarafsızlık': 0.05, 'Ekonomik Dayanıklılık': 0.10, 'İç Sosyal İstikrar': 0.20, 'Altyapı ve Sağlık': 0.10, 'Halkın Hazırlıklılığı': 0.0, 'İklim Dayanıklılığı': 0.30, 'Enerji Bağımsızlığı': 0.0, 'Siber Güvenlik': 0.0, 'Demografik Dayanıklılık': 0.10}},
    '6': {'name': 'Teknolojik Enerji Devrimi', 'weights': {'Coğrafi İzolasyon': 0.0, 'Nükleer Risk': 0.0, 'Politik Tarafsızlık': 0.05, 'Ekonomik Dayanıklılık': 0.30, 'İç Sosyal İstikrar': 0.20, 'Altyapı ve Sağlık': 0.10, 'Halkın Hazırlıklılığı': 0.0, 'İklim Dayanıklılığı': 0.0, 'Enerji Bağımsızlığı': 0.0, 'Siber Güvenlik': 0.20, 'Demografik Dayanıklılık': 0.15}}
}
#---------------------------------------------------


# 2. HESAPLAMA FONKSİYONU
#---------------------------------------------------
def calculate_scores(df, scenario_id):
    scenario = scenario_weights[scenario_id]
    weights = scenario['weights']
    score_columns = list(weights.keys())
    
    # Her kategori puanını kendi ağırlığıyla çarp ve topla
    df['Ağırlıklı Puan'] = (df[score_columns] * pd.Series(weights)).sum(axis=1)
    
    sorted_df = df.sort_values(by='Ağırlıklı Puan', ascending=False).reset_index(drop=True)
    return sorted_df, scenario['name']
#---------------------------------------------------


# 3. STREAMLIT ARAYÜZÜ
#---------------------------------------------------
st.set_page_config(page_title="Küresel Risk Simülatörü", layout="wide")

st.title("🌍 Dinamik Küresel Risk Simülatörü")
st.markdown("""
Bu araç, farklı küresel kriz senaryolarına göre ülkelerin dayanıklılığını analiz eder. 
Her senaryo, farklı faktörlere (ekonomi, coğrafya, enerji vb.) farklı ağırlıklar vererek ülkelerin sıralamasını dinamik olarak değiştirir.
""")

# Senaryo seçimi için bir dropdown menü (selectbox) oluştur
scenario_name_to_id = {v['name']: k for k, v in scenario_weights.items()}
selected_scenario_name = st.selectbox(
    'Lütfen analiz etmek istediğiniz senaryoyu seçin:',
    list(scenario_name_to_id.keys())
)

# Seçilen senaryoya göre hesaplamaları yap
selected_id = scenario_name_to_id[selected_scenario_name]
result_df, scenario_name = calculate_scores(df.copy(), selected_id)

# Sonuçları göster
st.header(f"📊 Senaryo Sonuçları: {scenario_name}")

# Sayfayı iki sütuna böl
col1, col2 = st.columns((1, 1.2)) # Sütunların genişlik oranları

with col1:
    st.subheader("Ülke Sıralaması")
    # Puanları formatlayıp göster
    display_df = result_df[['Ülke', 'Ağırlıklı Puan']].copy()
    display_df['Ağırlıklı Puan'] = display_df['Ağırlıklı Puan'].map('{:.2f}'.format)
    st.dataframe(display_df, height=620)

with col2:
    st.subheader("Puanların Görsel Karşılaştırması")
    # Grafik için veriyi hazırla
    chart_data = result_df.set_index('Ülke')['Ağırlıklı Puan']
    st.bar_chart(chart_data)

    with st.expander("ℹ️ Bu Senaryo Neden Önemli? (Açıklama)"):
        if selected_id == '1':
            st.write("Tüm faktörlerin dengeli bir şekilde hesaba katıldığı temel bir başlangıç noktasıdır.")
        elif selected_id == '2':
            st.write("Coğrafi uzaklık, tarafsızlık ve nükleer hedeflerden uzak durma en önemli faktörler haline gelir. Güney yarımküre ülkeleri ve izole adalar öne çıkar.")
        elif selected_id == '3':
            st.write("Ekonomik kendine yeterlilik, güçlü sanayi ve teknoloji bağımlılığının azlığı kritik önem kazanır. Pasifik'ten uzak, Atlantik odaklı ekonomiler avantajlıdır.")
        elif selected_id == '4':
            st.write("Enerji bağımsızlığı her şeyin önüne geçer. Net enerji ihracatçıları (Kanada, Avustralya) ve yenilenebilir enerjide lider olanlar (İzlanda, Uruguay) krizin kazananları olur.")
        elif selected_id == '5':
            st.write("Su ve gıda kaynaklarına sahip, ılıman iklimli, göç yollarından uzakta ve sosyal olarak uyumlu ülkeler en güvenli yerler haline gelir. İzolasyon ve kaynak zenginliği anahtardır.")
        elif selected_id == '6':
            st.write("Fosil yakıtlara dayalı olmayan, yüksek teknolojili, çeşitlendirilmiş ve inovatif ekonomiler bu devrimden kârlı çıkar. Genç ve eğitimli nüfus büyük bir avantajdır.")
#---------------------------------------------------