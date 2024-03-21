import streamlit as st
import pandas as pd 
from query import *
from streamlit_dynamic_filters import DynamicFilters
#set page
st.set_page_config(page_title="Bilgi Paneli",page_icon="🌓",layout="wide")
UI()
# Excel dosyasını oku
excel_file = 'Getiri_21032024_13_47.xlsx'

# Tüm sayfaları oku ve dfs adlı bir sözlüğe ekle
xls = pd.ExcelFile(excel_file)
dfs = {}
for sheet_name in xls.sheet_names:
    dfs[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)

# İlk sayfayı DataFrame'e oku
first_df = dfs[xls.sheet_names[0]]

# Sadece "Hisse" sütununun içeriğini filtreleme kriteri olarak kullan
hisse_filter = st.sidebar.selectbox(
    label="Filter by 'Hisse'",
    options=list(first_df['Hisse'].unique())
)

# Filtreli DataFrame'i oluştur
filtered_df = first_df[first_df['Hisse'] == hisse_filter]

# Tüm sütunları içeren bir liste oluştur
all_columns = list(filtered_df.columns)

# "Hisse" sütununu listeden çıkar
all_columns.remove('Hisse')

# Seçilebilecek sütunları göstermek için bir çoklu seçim alanı oluştur
selected_columns = st.sidebar.multiselect(
    label="Select columns to display",
    options=all_columns,
    default=all_columns
)

# Sadece seçilen sütunları içeren bir DataFrame oluştur
display_df = filtered_df[selected_columns]

# Filtreleri oluştur
filters = list(display_df.columns)
# "Hisse" sütunu filtrelere eklenir, diğer sütunlar sadece görünürlük için kullanılır
# Bu nedenle "Hisse" sütunu dışındaki sütunlara boş bir değer atanır
filters_except_hisse = [col if col == "Hisse" else "" for col in filters]

# DynamicFilters objesi oluştur
dynamic_filters = DynamicFilters(display_df, filters_except_hisse)

# Filtreleri görüntüle
dynamic_filters.display_filters(location='sidebar')

# DataFrame'i görüntüle
st.write("Original DataFrame:")
st.write(display_df)

# Filtrelenmiş DataFrame'i görüntüle
st.write("Filtered DataFrame:")
filtered_df = dynamic_filters.display_df()
st.write(filtered_df)
