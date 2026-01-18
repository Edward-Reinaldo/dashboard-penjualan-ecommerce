import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Analisis Penjualan E-commerce",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# THEME MANAGEMENT (tetap ada, tapi tidak digunakan untuk CSS)
# =============================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# =============================
# LOAD SOFT UI CSS (HANYA LIGHT STYLE - SESUAI REFERENSI)
# =============================
def load_soft_ui_css():
    # Hanya satu tema: Soft UI Light
    css = """
    /* Soft UI-inspired theme – inspired by https://demos.creative-tim.com/soft-ui-dashboard */
    .main { 
        padding: 1.5rem; 
        background-color: #f0f2f5; 
        color: #111827; 
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .main-header {
        background: linear-gradient(195deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    .main-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.2rem;
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    .kpi-card {
        background: white;
        padding: 1.25rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transition: transform 0.25s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        color: #6c757d;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        color: #111827;
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .kpi-subvalue {
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    .section-header {
        color: #111827;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 2rem 0 1.25rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    .chart-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        height: 100%;
    }
    .chart-title {
        color: #111827;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .status-completed {
        background-color: #4CAF50;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }
    .status-cancelled {
        background-color: #F44336;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    .sidebar-title {
        color: #111827;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f1f5f9;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton button {
        background: linear-gradient(195deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
    }
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    .dataframe th {
        background-color: #f1f5f9 !important;
        color: #111827;
        font-weight: 600;
        padding: 0.75rem !important;
    }
    .dataframe td {
        padding: 0.5rem !important;
        border-color: #e2e8f0 !important;
        color: #111827;
    }
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #e9ecef;
    }
    .grid-container {
        display: grid;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .main { padding: 1rem; }
        .kpi-value { font-size: 1.4rem; }
    }
    """
    return css

# Terapkan CSS Soft UI (abaikan state theme, selalu gunakan light ala Soft UI)
st.markdown(f"<style>{load_soft_ui_css()}</style>", unsafe_allow_html=True)

# =============================
# LOAD DATA & PREPROCESSING
# =============================
@st.cache_data
def load_data():
    df = pd.read_excel("all_months_clean.xlsx")
    df.columns = df.columns.str.strip()
    df["Waktu Pesanan Dibuat"] = pd.to_datetime(df["Waktu Pesanan Dibuat"])
    df["Tanggal"] = df["Waktu Pesanan Dibuat"].dt.date
    df["Jam"] = df["Waktu Pesanan Dibuat"].dt.hour
    df["Hari"] = df["Waktu Pesanan Dibuat"].dt.day_name()
    df["Bulan_Period"] = df["Waktu Pesanan Dibuat"].dt.to_period("M").astype(str)
    df["Bulan_Label"] = df["Waktu Pesanan Dibuat"].dt.strftime("%b %Y")
    df["product_categories"] = df["product_categories"].str.strip()
    df["is_cancelled"] = df["Status Pesanan"] == "Batal"
    df["is_completed"] = df["Status Pesanan"] == "Selesai"
    order_agg = df.groupby("order_id").agg({
        "Total Pembayaran": "first",
        "total_qty": "first",
        "total_weight_gr": "first",
        "Status Pesanan": "first",
        "Provinsi": "first",
        "Kota/Kabupaten": "first",
        "Metode Pembayaran": "first",
        "Opsi Pengiriman": "first",
        "is_cancelled": "first",
        "is_completed": "first",
        "num_product_categories": "first",
        "Alasan Pembatalan": "first",
        "Ongkos Kirim Dibayar oleh Pembeli": "first",
        "Perkiraan Ongkos Kirim": "first",
        "Estimasi Potongan Biaya Pengiriman": "first"
    }).reset_index()
    return df, order_agg

# =============================
# LOAD RAW DATA
# =============================
df_raw, order_agg_raw = load_data()

# =============================
# SIDEBAR FILTERS
# =============================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #111827; margin: 0;">⚙️ Kontrol Dashboard</h2>
            <p style="color: #6c757d; margin: 0.5rem 0 0 0;">Filter & Pengaturan</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Tetap tampilkan toggle, tapi tidak berpengaruh (untuk kompatibilitas logika)
    st.markdown('<div class="sidebar-title">🎨 Tema</div>', unsafe_allow_html=True)
    theme_toggle = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == 'dark'), on_change=toggle_theme)
    # Catatan: CSS tidak berubah berdasarkan toggle — tetap Soft UI light

    # Tanggal
    min_date = df_raw["Waktu Pesanan Dibuat"].min().date()
    max_date = df_raw["Waktu Pesanan Dibuat"].max().date()
    date_range = st.date_input(
        "Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

    # Provinsi
    provinces = sorted(order_agg_raw["Provinsi"].unique())
    selected_provinces = st.multiselect(
        "Pilih provinsi:",
        options=provinces,
        default=provinces,
        label_visibility="collapsed"
    )

    # Status
    selected_status = st.radio(
        "Status Order:",
        options=["Semua", "Selesai", "Batal"],
        index=0,
        label_visibility="collapsed"
    )

    # Metode Pembayaran
    payment_methods = sorted(order_agg_raw["Metode Pembayaran"].dropna().unique())
    selected_payments = st.multiselect(
        "Pilih metode pembayaran:",
        options=payment_methods,
        default=payment_methods,
        label_visibility="collapsed"
    )

# =============================
# APPLY FILTERS
# =============================
df = df_raw.copy()
order_agg = order_agg_raw.copy()

if len(date_range) == 2:
    start, end = date_range
    mask = (df["Waktu Pesanan Dibuat"].dt.date >= start) & (df["Waktu Pesanan Dibuat"].dt.date <= end)
    df = df[mask]
    order_agg = order_agg[order_agg["order_id"].isin(df["order_id"].unique())]

if selected_provinces:
    df = df[df["Provinsi"].isin(selected_provinces)]
    order_agg = order_agg[order_agg["Provinsi"].isin(selected_provinces)]

if selected_status == "Selesai":
    df = df[df["is_completed"]]
    order_agg = order_agg[order_agg["is_completed"]]
elif selected_status == "Batal":
    df = df[df["is_cancelled"]]
    order_agg = order_agg[order_agg["is_cancelled"]]

if selected_payments:
    df = df[df["Metode Pembayaran"].isin(selected_payments)]
    order_agg = order_agg[order_agg["Metode Pembayaran"].isin(selected_payments)]

# =============================
# DASHBOARD HEADER
# =============================
st.markdown("""
<div class="main-header">
    <h1>Dashboard Analisis Penjualan E-commerce</h1>
    <p>Analisis Data Penjualan April 2024 - Real-time Performance Monitoring</p>
</div>
""", unsafe_allow_html=True)

# =============================
# KPI METRICS SECTION
# =============================
col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

def create_kpi_card(title, value, subtitle, color="#b566ea", subcolor="#6c757d"):
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subvalue">{subtitle}</div>
    </div>
    """

with col1:
    st.markdown(create_kpi_card("TOTAL ORDER", f"{len(order_agg):,}", "Semua transaksi"), unsafe_allow_html=True)
with col2:
    total_sales = order_agg[order_agg['is_completed']]['Total Pembayaran'].sum()
    st.markdown(create_kpi_card("TOTAL PENJUALAN", f"Rp {total_sales/1e6:.1f}M", "Dari order sukses"), unsafe_allow_html=True)
with col3:
    completed_orders = order_agg['is_completed'].sum()
    completion_rate = (completed_orders / len(order_agg) * 100)
    st.markdown(create_kpi_card("ORDER SELESAI", f"{completed_orders:,}", f"<span style='color: #4CAF50;'>{completion_rate:.1f}% Tingkat penyelesaian</span>", color="#8B4CAF", subcolor="#904CAF"), unsafe_allow_html=True)
with col4:
    cancelled_orders = order_agg['is_cancelled'].sum()
    cancellation_rate = (cancelled_orders / len(order_agg) * 100)
    st.markdown(create_kpi_card("ORDER DIBATALKAN", f"{cancelled_orders:,}", f"<span style='color: #F44336;'>{cancellation_rate:.1f}% Tingkat pembatalan</span>", color="#B836F4", subcolor="#9836F4"), unsafe_allow_html=True)
with col5:
    avg_order_value = order_agg[order_agg['is_completed']]['Total Pembayaran'].mean()
    st.markdown(create_kpi_card("RATA-RATA NILAI ORDER", f"Rp {avg_order_value:,.0f}", "Per transaksi sukses"), unsafe_allow_html=True)

# =============================
# ROW 1: MAP
# =============================
with st.container():
    st.markdown('<div class="chart-title">Peta Penjualan per Provinsi</div>', unsafe_allow_html=True)
    try:
        with open("gabungan_38_wilayah_batas_provinsi.geojson", "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        feature_key = "name"
        province_sales = order_agg[order_agg['is_completed']].groupby("Provinsi").agg({
            "Total Pembayaran": "sum",
            "order_id": "nunique"
        }).reset_index()
        province_sales.columns = ["Provinsi", "Total Penjualan", "Jumlah Order"]
        province_sales["Provinsi"] = (
            province_sales["Provinsi"]
            .str.replace(r"\s*\(.*?\)\s*", "", regex=True)
            .str.strip()
            .str.title()
        )
        special_mapping = {
            "Dki Jakarta": "Daerah Khusus Ibukota Jakarta",
            "Di Yogyakarta": "Daerah Istimewa Yogyakarta",
            "Nanggroe Aceh Darussalam": "Aceh",
            "Bangka Belitung": "Kepulauan Bangka Belitung",
            "Papua Barat": "Papua Barat",
            "Papua": "Papua",
        }
        province_sales["Provinsi"] = province_sales["Provinsi"].replace(special_mapping)

        fig = go.Figure(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=province_sales["Provinsi"],
            z=province_sales["Total Penjualan"],
            featureidkey=f"properties.{feature_key}",
            colorscale=[[0, "#EAA7FF"], [0.5, "#B12DDA"], [1, "#8109E3"]],
            colorbar=dict(title="Penjualan (Rp)", tickprefix="Rp "),
            marker_opacity=0.8,
            marker_line_width=1,
            hovertemplate="<b>%{location}</b><br>Penjualan: Rp %{z:,.0f}<br><extra></extra>",
        ))
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=3.5,
            mapbox_center={"lat": -2.5489, "lon": 118.0149},
            height=400,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error("File GeoJSON tidak ditemukan.")

# =============================
# ROW 2: GEO & PAYMENT ANALYSIS
# =============================
st.markdown('<div class="section-header">Sebaran Wilayah & Preferensi Transaksi</div>', unsafe_allow_html=True)

with st.container():
    tab1, tab2 = st.tabs(["Performa Penjualan Provinsi & Kota", "Metode Pembayaran"])
    with tab1:
        col1, col2 = st.columns([2, 1], gap="medium")
        with col1:
            st.markdown('<div class="chart-title">Top 10 Provinsi Penjualan Tertinggi</div>', unsafe_allow_html=True)
            province_sales = order_agg[order_agg['is_completed']].groupby("Provinsi").agg({
                "Total Pembayaran": "sum",
                "order_id": "nunique"
            }).reset_index()
            province_sales.columns = ["Provinsi", "Total Penjualan", "Jumlah Order"]
            province_sales = province_sales.sort_values("Total Penjualan", ascending=False)
            top10 = province_sales.head(10).sort_values("Total Penjualan", ascending=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=top10["Provinsi"],
                x=top10["Total Penjualan"],
                orientation='h',
                marker_color="#8966ea",
                hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<br>%{customdata} order<br><extra></extra>',
                customdata=top10["Jumlah Order"],
                text=[f'Rp {x/1e6:.1f}M' if x >= 1e6 else f'Rp {x/1e3:.0f}K' for x in top10["Total Penjualan"]],
                textposition='outside'
            ))
            fig.update_layout(
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#e2e8f0', tickprefix='Rp ', tickformat=',.0f'),
                yaxis=dict(showgrid=False, categoryorder='total ascending'),
                hovermode='y unified',
                margin=dict(t=30, b=30, l=150, r=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown('<div class="chart-title">Pilih Provinsi</div>', unsafe_allow_html=True)
            selected_province = st.selectbox(
                "Pilih provinsi untuk detail:",
                options=province_sales["Provinsi"].tolist(),
                index=0,
                key="province_select"
            )
            if selected_province:
                city_data = order_agg[
                    (order_agg['is_completed']) &
                    (order_agg['Provinsi'] == selected_province)
                ].groupby("Kota/Kabupaten").agg({
                    "Total Pembayaran": "sum",
                    "order_id": "nunique"
                }).reset_index()
                city_data.columns = ["Kota/Kabupaten", "Total Penjualan", "Jumlah Order"]
                if not city_data.empty:
                    st.markdown(f'<div class="chart-title">Top 5 Kota di {selected_province}</div>', unsafe_allow_html=True)
                    top5_cities = city_data.sort_values("Total Penjualan", ascending=False).head(5)
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=top5_cities["Kota/Kabupaten"],
                        y=top5_cities["Total Penjualan"],
                        marker_color="#AC4CAF",
                        hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<br><extra></extra>',
                        text=[f'Rp {x:,.0f}' for x in top5_cities["Total Penjualan"]],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        height=250,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        xaxis=dict(tickangle=45),
                        yaxis=dict(tickprefix='Rp ')
                    )
                    st.plotly_chart(fig, use_container_width=True)
    with tab2:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.markdown('<div class="chart-title">Distribusi Metode Pembayaran</div>', unsafe_allow_html=True)
            payment_counts = order_agg[order_agg['is_completed']]['Metode Pembayaran'].value_counts().reset_index()
            payment_counts.columns = ["Metode", "Jumlah Order"]
            top_5 = payment_counts.head(5)
            others = payment_counts.iloc[5:]
            if not others.empty:
                others_sum = others["Jumlah Order"].sum()
                others_row = pd.DataFrame({"Metode": ["Lainnya"], "Jumlah Order": [others_sum]})
                payment_methods_df = pd.concat([top_5, others_row], ignore_index=True)
            else:
                payment_methods_df = top_5
            total = payment_methods_df["Jumlah Order"].sum()
            payment_methods_df["Persentase"] = (payment_methods_df["Jumlah Order"] / total * 100).round(1)
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=payment_methods_df["Metode"],
                values=payment_methods_df["Jumlah Order"],
                hole=.4,
                hovertemplate='<b>%{label}</b><br>%{value} order<br>%{percent}<br><extra></extra>',
                textinfo='percent',
                textposition='inside',
                marker=dict(colors=px.colors.qualitative.Set3, line=dict(color='white', width=2)),
            ))
            fig.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown('<div class="chart-title">Detail Statistik Pembayaran</div>', unsafe_allow_html=True)
            completed_orders = order_agg[order_agg['is_completed']]
            if not completed_orders.empty and "Metode Pembayaran" in completed_orders.columns:
                valid_payments = completed_orders.dropna(subset=["Metode Pembayaran"])
                if not valid_payments.empty:
                    payment_stats = valid_payments.groupby("Metode Pembayaran").agg({
                        "Total Pembayaran": ["sum", "mean"]
                    }).round(0)
                    payment_stats.columns = ["Total Pembayaran", "Rata-rata Pembayaran"]
                    payment_stats = payment_stats.sort_values("Total Pembayaran", ascending=False).head(10)
                    payment_stats["Total Pembayaran"] = payment_stats["Total Pembayaran"].apply(
                        lambda x: f"Rp {x/1e6:.1f}M" if x >= 1e6 else f"Rp {x/1e3:.0f}K"
                    )
                    payment_stats["Rata-rata Pembayaran"] = payment_stats["Rata-rata Pembayaran"].apply(
                        lambda x: f"Rp {x:,.0f}"
                    )
                    st.dataframe(
                        payment_stats.reset_index(),
                        use_container_width=True,
                        hide_index=True,
                        height=350
                    )

# =============================
# ROW 3: OPERATIONAL & CANCELLATION
# =============================
st.markdown('<div class="section-header">Tinjauan Biaya Kirim & Pembatalan Order</div>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.markdown('<div class="chart-title">Perbandingan Komponen & Subsidi Logistik</div>', unsafe_allow_html=True)
        shipping_data = order_agg[order_agg['is_completed']].copy()
        shipping_data = shipping_data[shipping_data['Perkiraan Ongkos Kirim'] > 0]
        shipping_comparison = shipping_data[['Perkiraan Ongkos Kirim', 'Ongkos Kirim Dibayar oleh Pembeli', 'Estimasi Potongan Biaya Pengiriman']].copy()
        shipping_comparison['Subsidi Platform'] = shipping_comparison['Estimasi Potongan Biaya Pengiriman']
        fig = go.Figure()
        fig.add_trace(go.Box(
            x=['Perkiraan Ongkir'] * len(shipping_comparison),
            y=shipping_comparison['Perkiraan Ongkos Kirim'],
            marker_color="#aa66ea",
            boxmean=True,
            showlegend=False,
            hovertemplate='<b>Perkiraan Ongkir</b><br>Rp %{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Box(
            x=['Dibayar Pembeli'] * len(shipping_comparison),
            y=shipping_comparison['Ongkos Kirim Dibayar oleh Pembeli'],
            marker_color="#934CAF",
            boxmean=True,
            showlegend=False,
            hovertemplate='<b>Dibayar Pembeli</b><br>Rp %{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Box(
            x=['Subsidi Platform'] * len(shipping_comparison),
            y=shipping_comparison['Subsidi Platform'],
            marker_color="#7300A0",
            boxmean=True,
            showlegend=False,
            hovertemplate='<b>Subsidi Platform</b><br>Rp %{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title="", tickangle=0, tickfont=dict(size=12), showgrid=False),
            yaxis=dict(
                title="Biaya (Rp)",
                showgrid=True,
                gridcolor='#e2e8f0',
                tickformat=',.0f',
                tickprefix='Rp '
            ),
            hovermode='x unified',
            margin=dict(t=30, b=50, l=50, r=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="chart-title">Analisis Pembatalan Order</div>', unsafe_allow_html=True)
        cancelled_orders = order_agg[order_agg['is_cancelled']]
        if len(cancelled_orders) > 0:
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Total Pembatalan", f"{len(cancelled_orders):,}")
            with col_stat2:
                cancel_rate = (len(cancelled_orders) / len(order_agg)) * 100
                st.metric("Tingkat Pembatalan", f"{cancel_rate:.1f}%")
            def classify_cancellation(text):
                if pd.isna(text):
                    return "Tidak Diketahui", "Tidak Diketahui", "Tidak Diketahui"
                text_lower = str(text).lower()
                sistem_keywords = ["paket hilang", "pengiriman gagal", "gagal mengirimkan pesanan tepat waktu", "pesanan belum dibayar"]
                pembeli_keywords = ["menemukan yang lebih murah", "need to change delivery addres", "penjual tidak responsif", "ubah alamat pengiriman", "ubah pesanan", "ubah voucher", "proses pembayaran sulit", "tidak ingin membeli lagi", "berubah pikiran", "lainnya/berubah pikiran"]
                normalized = text
                short_name = text
                if "Ubah Pesanan" in text or "Perlu mengubah Pesanan" in text:
                    normalized = "Ubah pesanan yang ada"
                    short_name = "Ubah Pesanan"
                elif "Perlu mengubah alamat pengiriman" in text or "Need to change delivery addres" in text:
                    normalized = "Perlu mengubah alamat pengiriman"
                    short_name = "Ubah Alamat"
                elif "Lainnya/berubah pikiran" in text or ("Lainnya" in text and "berubah pikiran" in text):
                    normalized = "Lainnya/berubah pikiran"
                    short_name = "Berubah Pikiran"
                elif "Pengiriman gagal" in text:
                    normalized = "Pengiriman gagal"
                    short_name = "Pengiriman Gagal"
                elif any(kw in text for kw in ["Pesanan belum dibayar"]):
                    normalized = "Pesanan belum dibayar"
                    short_name = "Belum Bayar"
                elif any(kw in text for kw in ["Gagal mengirimkan pesanan tepat waktu"]):
                    normalized = "Gagal mengirimkan pesanan tepat waktu"
                    short_name = "Gagal Kirim Tepat Waktu"
                elif any(kw in text for kw in ["Paket hilang"]):
                    normalized = "Paket hilang dalam perjalanan"
                    short_name = "Paket Hilang"
                elif "Lainnya" == text.strip():
                    normalized = "Lainnya"
                    short_name = "Lainnya"
                else:
                    short_name = text[:20] + "..." if len(text) > 20 else text
                if any(kw in normalized.lower() for kw in [k.lower() for k in sistem_keywords]):
                    return normalized, "Dibatalkan oleh Sistem", short_name
                elif any(kw in normalized.lower() for kw in [k.lower() for k in pembeli_keywords]):
                    return normalized, "Dibatalkan oleh Pembeli", short_name
                else:
                    return normalized, "Dibatalkan oleh Pembeli", short_name
            cancelled_orders[['Alasan', 'Jenis', 'Alasan_Short']] = cancelled_orders['Alasan Pembatalan'].apply(
                lambda x: pd.Series(classify_cancellation(x))
            )
            st.markdown("##### Jenis Pembatalan")
            jenis_counts = cancelled_orders['Jenis'].value_counts().reset_index()
            jenis_counts.columns = ["Jenis", "Jumlah"]
            fig1 = go.Figure()
            colors = ["#A836F4", "#d25fff"]
            fig1.add_trace(go.Bar(
                x=jenis_counts["Jenis"],
                y=jenis_counts["Jumlah"],
                marker_color=colors[:len(jenis_counts)],
                text=jenis_counts["Jumlah"],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>%{y} order<extra></extra>'
            ))
            fig1.update_layout(
                height=250,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(title="Jenis Pembatalan"),
                yaxis=dict(title="Jumlah Order", showgrid=True, gridcolor='#e2e8f0'),
                margin=dict(t=30, b=40, l=50, r=30)
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("##### Top Alasan Pembatalan")
            reason_counts = cancelled_orders['Alasan_Short'].value_counts().head(10).reset_index()
            reason_counts.columns = ["Alasan", "Jumlah"]
            if len(reason_counts) > 0:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    y=reason_counts["Alasan"],
                    x=reason_counts["Jumlah"],
                    orientation='h',
                    marker_color="#e666ea",
                    hovertemplate='<b>%{y}</b><br>%{x} order<extra></extra>',
                    text=reason_counts["Jumlah"],
                    textposition='outside'
                ))
                fig2.update_layout(
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis=dict(title="Jumlah Order", showgrid=True, gridcolor='#e2e8f0'),
                    yaxis=dict(title="Alasan Pembatalan", showgrid=False),
                    margin=dict(t=30, b=40, l=150, r=30)
                )
                st.plotly_chart(fig2, use_container_width=True)
            with st.expander("Analisis Pembatalan per Jam"):
                cancelled_hourly = df[df['is_cancelled']].groupby("Jam").size().reset_index()
                cancelled_hourly.columns = ["Jam", "Jumlah Pembatalan"]
                total_hourly = df.groupby("Jam").size().reset_index()
                total_hourly.columns = ["Jam", "Total Order"]
                hourly_data = total_hourly.merge(cancelled_hourly, on="Jam", how="left")
                hourly_data["Jumlah Pembatalan"] = hourly_data["Jumlah Pembatalan"].fillna(0)
                hourly_data["Persentase Batal"] = (hourly_data["Jumlah Pembatalan"] / hourly_data["Total Order"] * 100).round(2)
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=hourly_data["Jam"],
                    y=hourly_data["Jumlah Pembatalan"],
                    mode='lines',
                    name='Jumlah Pembatalan',
                    line=dict(color="#9E36F4", width=3),
                    fill='tozeroy',
                    fillcolor='rgba(244, 67, 54, 0.15)',
                    hovertemplate='<b>Jam %{x}:00</b><br>Jumlah Batal: %{y}<extra></extra>'
                ))
                fig3.update_layout(
                    title="Pola Pembatalan per Jam",
                    xaxis=dict(title="Jam", tickmode='linear', dtick=2),
                    yaxis=dict(title="Jumlah Order", showgrid=True, gridcolor='#e2e8f0'),
                    yaxis2=dict(title="Persentase (%)", overlaying='y', side='right', showgrid=False),
                    hovermode='x unified',
                    height=300,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(t=40, b=30, l=50, r=50),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig3, use_container_width=True)

# =============================
# ROW 4: TIME ANALYSIS
# ============================= .u
st.markdown('<div class="section-header">Analisis Pola Waktu & Order</div>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([7, 3], gap="medium")
    with col1:
        st.markdown('<div class="chart-title">Distribusi Order per Jam</div>', unsafe_allow_html=True)
        hourly_orders = df[df['is_completed']].groupby("Jam").agg({
            "order_id": "nunique",
            "Total Pembayaran": "sum"
        }).reset_index()
        hourly_orders.columns = ["Jam", "Jumlah Order", "Total Penjualan"]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=hourly_orders["Jam"],
                y=hourly_orders["Jumlah Order"],
                mode='lines+markers',
                name='Jumlah Order',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8),
                hovertemplate='<b>Jam %{x}:00</b><br>%{y} order<br><extra></extra>'
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Bar(
                x=hourly_orders["Jam"],
                y=hourly_orders["Total Penjualan"],
                name='Total Penjualan',
                marker_color='rgba(102, 126, 234, 0.4)',
                hovertemplate='<b>Jam %{x}:00</b><br>Rp %{y:,.0f}<br><extra></extra>'
            ),
            secondary_y=True
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#111827'),
            xaxis=dict(title="Jam", showgrid=True, gridcolor='#e2e8f0', tickmode='linear', tick0=0, dtick=2),
            yaxis=dict(title="Jumlah Order", showgrid=True, gridcolor='#e2e8f0'),
            yaxis2=dict(title="Total Penjualan (Rp)", showgrid=False, tickprefix='Rp '),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(t=40, b=50, l=50, r=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="chart-title">Insights Waktu Operasional</div>', unsafe_allow_html=True)
        peak_hour = hourly_orders.loc[hourly_orders['Jumlah Order'].idxmax()]
        peak_sales_hour = hourly_orders.loc[hourly_orders['Total Penjualan'].idxmax()]
        low_hour = hourly_orders.loc[hourly_orders['Jumlah Order'].idxmin()]
        st.markdown(f"""<div style="background: linear-gradient(195deg, #5d02bf 0%, #764ba2); color: white; padding: 0.8rem 1rem; border-radius: 12px; margin-bottom: 0.5rem; font-size: 0.9rem;"><div style="font-size: 0.8rem; opacity: 0.9;">Jam Puncak Order</div><div style="font-size: 1.6rem; font-weight: 700;">{int(peak_hour['Jam'])}:00</div><div style="font-size: 0.75rem;">{int(peak_hour['Jumlah Order'])} order</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background: linear-gradient(195deg, #a902bf 0%, #764ba2); color: white; padding: 0.8rem 1rem; border-radius: 12px; margin-bottom: 0.5rem; font-size: 0.9rem;"><div style="font-size: 0.8rem; opacity: 0.9;">Jam Penjualan Tertinggi</div><div style="font-size: 1.6rem; font-weight: 700;">{int(peak_sales_hour['Jam'])}:00</div><div style="font-size: 0.75rem;">Rp {peak_sales_hour['Total Penjualan']/1e6:.1f}M</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="background: linear-gradient(195deg, #bf02af 0%, #764ba2); color: white; padding: 0.8rem 1rem; border-radius: 12px; font-size: 0.9rem;"><div style="font-size: 0.8rem; opacity: 0.9;">Jam Terendah</div><div style="font-size: 1.6rem; font-weight: 700;">{int(low_hour['Jam'])}:00</div><div style="font-size: 0.75rem;">{int(low_hour['Jumlah Order'])} order</div></div>""", unsafe_allow_html=True)

# =============================
# DATA TABLE
# =============================
st.markdown('<div class="section-header">Data Detail Transaksi</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chart-title">Tabel Data Order</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        show_completed = st.checkbox("✅ Tampilkan hanya order selesai", value=True, key="show_completed")
        show_cancelled = st.checkbox("❌ Tampilkan hanya order dibatalkan", value=False, key="show_cancelled")
    with col2:
        show_rows = st.select_slider("Jumlah baris:", options=[10, 25, 50, 100, 200], value=50)
    with col3:
        st.write("")
    if st.button("🔄 Refresh Tampilan", use_container_width=True):
        st.rerun()
    display_df = order_agg.copy()
    if show_completed and not show_cancelled:
        display_df = display_df[display_df['is_completed']]
    elif show_cancelled and not show_completed:
        display_df = display_df[display_df['is_cancelled']]
    display_df = display_df.head(show_rows)
    formatted_df = display_df.copy()
    formatted_df['Total Pembayaran'] = formatted_df['Total Pembayaran'].apply(lambda x: f'Rp {x:,.0f}')
    formatted_df['Status Pesanan'] = formatted_df.apply(
        lambda row: f"<span class='status-completed'>✓ {row['Status Pesanan']}</span>" if row['is_completed']
        else f"<span class='status-cancelled'>✗ {row['Status Pesanan']}</span>",
        axis=1
    )
    display_columns = ['order_id', 'Status Pesanan', 'Total Pembayaran', 'total_qty', 'Provinsi', 'Kota/Kabupaten', 'Metode Pembayaran', 'Opsi Pengiriman']
    st.dataframe(formatted_df[display_columns], use_container_width=True, height=400, hide_index=True)

# =============================
# FOOTER
# =============================
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div><strong>Dashboard Analisis Penjualan E-commerce</strong><br>Data Periode April 2024</div>
        <div style="text-align: right;"><strong>Update Terakhir</strong><br>9 Januari 2024</div>
    </div>
    <div style="border-top: 1px solid #e9ecef; padding-top: 1rem; color: #6c757d; font-size: 0.8rem;">
        © 2024 E-commerce Analytics • Dibuat dengan Streamlit & Plotly
    </div>
</div>
""", unsafe_allow_html=True)