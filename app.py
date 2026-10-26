import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="DNP Waste Management Dashboard",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Prompt', sans-serif;
    }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1b4d3e 0%, #2e7d32 50%, #43a047 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px rgba(27, 77, 62, 0.2);
    }
    .header-box h1 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-box p {
        color: #e8f5e9;
        margin-top: 8px;
        margin-bottom: 0;
        font-size: 1rem;
        opacity: 0.95;
    }
    
    /* Custom KPI Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #616161;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1b4d3e;
        margin-bottom: 4px;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #757575;
    }
    
    /* Section Headings */
    .section-title {
        color: #2e7d32;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #2e7d32;
        padding-left: 10px;
    }
    
    /* Badges */
    .source-badge {
        display: inline-block;
        background-color: #e8f5e9;
        color: #1b4d3e;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading with Caching ---
@st.cache_data
def load_data():
    csv_file = "waste_data_cleaned.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
    else:
        # Fallback raw data url or load raw files
        raw_2568 = "https://catalog.dnp.go.th/dataset/5fd1ccae-e476-4fc9-9348-b1eaed66e00b/resource/ca78a27d-27eb-466b-b76d-040610fbec3f/download/untitled-2026-09-16t100900.990.csv"
        df2568 = pd.read_csv(raw_2568, encoding='cp874')
        raw_2569 = "https://catalog.dnp.go.th/dataset/5fd1ccae-e476-4fc9-9348-b1eaed66e00b/resource/feb98930-8776-4c96-ae6e-796f42d09af1/download/untitled-2026-09-16t101110.786.csv"
        df2569 = pd.read_csv(raw_2569, encoding='cp874')
        df2569 = df2569.rename(columns={
            'นำไปใช้ประโยชน์ (กก.)': 'ใช้ประโยชน์ (กก.)',
            'ร้อยละขยะส่งกำจัดลดลง': 'ร้อยละส่งกำจัดลดลง'
        })
        df = pd.concat([df2568, df2569], ignore_index=True)
        numeric_cols = ['คนเฉลี่ย', 'วันทำงาน', 'โฟมบรรจุอาหาร (ใบ)', 'ขยะที่เกิดขึ้น (กก.)', 'ใช้ประโยชน์ (กก.)', 'ขยะที่ส่งกำจัด (กก.)', 'ร้อยละส่งกำจัดลดลง']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce').fillna(0)
        month_order = {'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4, 'พฤษภาคม': 5, 'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8, 'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12}
        df['ลำดับเดือน'] = df['เดือน'].map(month_order).fillna(99).astype(int)
        df['อัตราการนำไปใช้ประโยชน์ (%)'] = (df['ใช้ประโยชน์ (กก.)'] / df['ขยะที่เกิดขึ้น (กก.)'] * 100).fillna(0).round(2)
        df['ขยะต่อคนต่อวัน (กก.)'] = (df['ขยะที่เกิดขึ้น (กก.)'] / (df['คนเฉลี่ย'] * df['วันทำงาน'])).fillna(0).round(4)
    
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"ไม่สามารถโหลดข้อมูลได้: {e}")
    st.stop()

# --- Sidebar Filters (Interactive Widgets) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Emblem_of_the_Department_of_National_Parks%2C_Wildlife_and_Plant_Conservation.svg/200px-Emblem_of_the_Department_of_National_Parks%2C_Wildlife_and_Plant_Conservation.svg.png", width=90)
st.sidebar.title("🎛️ ตัวกรองข้อมูล (Filters)")
st.sidebar.markdown("เลือกเงื่อนไขเพื่อปรับแต่งการแสดงผล")

# 1. Year Filter
available_years = sorted(df_raw['ปี'].unique())
selected_year = st.sidebar.selectbox(
    "📅 เลือกปีงบประมาณ (พ.ศ.)",
    options=["ทั้งหมด"] + [str(y) for y in available_years],
    index=0
)

# 2. Sector Filter (สังกัด)
available_sectors = sorted(df_raw['สังกัด'].unique())
selected_sector = st.sidebar.radio(
    "🏢 เลือกสังกัด",
    options=["ทั้งหมด"] + list(available_sectors),
    index=0
)

# Filter dataframe progressively
df_filtered = df_raw.copy()

if selected_year != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered['ปี'] == int(selected_year)]

if selected_sector != "ทั้งหมด":
    df_filtered = df_filtered[df_filtered['สังกัด'] == selected_sector]

# 3. Agency Filter (หน่วยงาน)
available_agencies = sorted(df_filtered['หน่วยงาน'].unique())
selected_agencies = st.sidebar.multiselect(
    "🏛️ เลือกหน่วยงาน (เลือกได้หลายหน่วยงาน)",
    options=available_agencies,
    default=[]
)
if selected_agencies:
    df_filtered = df_filtered[df_filtered['หน่วยงาน'].isin(selected_agencies)]

# 4. Month Range Filter
month_names = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
selected_month_range = st.sidebar.select_slider(
    "🗓️ ช่วงเดือนที่ต้องการวิเคราะห์",
    options=month_names,
    value=('มกราคม', 'ธันวาคม')
)

start_idx = month_names.index(selected_month_range[0]) + 1
end_idx = month_names.index(selected_month_range[1]) + 1
df_filtered = df_filtered[(df_filtered['ลำดับเดือน'] >= start_idx) & (df_filtered['ลำดับเดือน'] <= end_idx)]

# Sidebar Info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 ข้อมูลชุดข้อมูล")
st.sidebar.markdown("""
- **แหล่งข้อมูล:** [data.go.th](https://data.go.th/dataset/gdpublish-69-dnp01-11-01)
- **หน่วยงาน:** กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช
- **กระทรวง:** ทรัพยากรธรรมชาติและสิ่งแวดล้อม
""")

# --- Main Dashboard Header ---
st.markdown("""
<div class="header-box">
    <h1>♻️ แดชบอร์ดสถิติปริมาณขยะมูลฝอย กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช</h1>
    <p>ระบบติดตาม วิเคราะห์ปริมาณขยะมูลฝอย การนำไปใช้ประโยชน์ และประสิทธิผลการลดปริมาณขยะของหน่วยงาน</p>
    <a href="https://data.go.th/dataset/gdpublish-69-dnp01-11-01" target="_blank" class="source-badge">
        🌐 Open Government Data of Thailand (data.go.th)
    </a>
</div>
""", unsafe_allow_html=True)

# Check if data exists after filtering
if df_filtered.empty:
    st.warning("⚠️ ไม่พบข้อมูลตามเงื่อนไขตัวกรองที่คุณเลือก กรุณาปรับเปลี่ยนตัวกรองในแถบด้านซ้าย")
    st.stop()

# --- Key Metrics / KPIs ---
total_waste = df_filtered['ขยะที่เกิดขึ้น (กก.)'].sum()
total_reused = df_filtered['ใช้ประโยชน์ (กก.)'].sum()
total_disposed = df_filtered['ขยะที่ส่งกำจัด (กก.)'].sum()
avg_reduction = df_filtered['ร้อยละส่งกำจัดลดลง'].mean()
total_staff = df_filtered['คนเฉลี่ย'].sum()
avg_waste_per_person = df_filtered['ขยะต่อคนต่อวัน (กก.)'].mean()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        label="📦 ปริมาณขยะทั้งหมด",
        value=f"{total_waste:,.1f} กก.",
        delta=f"{(total_waste/1000):,.2f} ตัน"
    )
with col2:
    reused_pct = (total_reused / total_waste * 100) if total_waste > 0 else 0
    st.metric(
        label="🔄 นำไปใช้ประโยชน์",
        value=f"{total_reused:,.1f} กก.",
        delta=f"{reused_pct:.1f}% ของทั้งหมด"
    )
with col3:
    disposed_pct = (total_disposed / total_waste * 100) if total_waste > 0 else 0
    st.metric(
        label="🚛 ขยะส่งกำจัด",
        value=f"{total_disposed:,.1f} กก.",
        delta=f"{disposed_pct:.1f}% ของทั้งหมด",
        delta_color="inverse"
    )
with col4:
    st.metric(
        label="🎯 ร้อยละการลดขยะเฉลี่ย",
        value=f"{avg_reduction:.2f}%",
        delta="เป้าหมายลดขยะ"
    )
with col5:
    st.metric(
        label="👤 ขยะเฉลี่ยต่อคนต่อวัน",
        value=f"{avg_waste_per_person:.3f} กก.",
        delta="กก./คน/วัน"
    )

st.markdown("---")

# --- Visualizations Section ---
tab1, tab2, tab3 = st.tabs(["📊 การวิเคราะห์แนวโน้มและสัดส่วน", "🏆 จัดอันดับหน่วยงาน", "📋 ตารางข้อมูล & ดาวน์โหลด"])

with tab1:
    st.markdown('<div class="section-title">📈 กราฟแนวโน้มปริมาณขยะรายเดือน & สัดส่วนการจัดการ</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        # 1. Monthly Trend Bar/Line Chart
        monthly_df = df_filtered.groupby(['ลำดับเดือน', 'เดือน'])[['ขยะที่เกิดขึ้น (กก.)', 'ใช้ประโยชน์ (กก.)', 'ขยะที่ส่งกำจัด (กก.)']].sum().reset_index()
        monthly_df = monthly_df.sort_values('ลำดับเดือน')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=monthly_df['เดือน'],
            y=monthly_df['ใช้ประโยชน์ (กก.)'],
            name='นำไปใช้ประโยชน์ (กก.)',
            marker_color='#2e7d32'
        ))
        fig_trend.add_trace(go.Bar(
            x=monthly_df['เดือน'],
            y=monthly_df['ขยะที่ส่งกำจัด (กก.)'],
            name='ขยะส่งกำจัด (กก.)',
            marker_color='#e53935'
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df['เดือน'],
            y=monthly_df['ขยะที่เกิดขึ้น (กก.)'],
            name='ขยะที่เกิดขึ้นรวม (กก.)',
            mode='lines+markers',
            line=dict(color='#ff9800', width=3),
            marker=dict(size=8)
        ))
        fig_trend.update_layout(
            title="<b>แนวโน้มปริมาณขยะรายเดือน (กก.)</b>",
            barmode='stack',
            xaxis_title="เดือน",
            yaxis_title="ปริมาณขยะ (กก.)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=60, b=20),
            plot_bgcolor='rgba(240,244,241,0.3)'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with chart_col2:
        # 2. Donut Chart: Reused vs Disposed
        labels = ['นำไปใช้ประโยชน์ (Recycled/Reused)', 'ส่งไปกำจัด (Disposed)']
        values = [total_reused, total_disposed]
        colors = ['#2e7d32', '#ef5350']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.55,
            marker_colors=colors,
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        fig_donut.update_layout(
            title="<b>สัดส่วนการจัดการขยะมูลฝอย</b>",
            showlegend=False,
            margin=dict(l=20, r=20, t=60, b=20),
            annotations=[dict(
                text=f'รวม<br><b>{total_waste:,.0f}</b><br>กก.',
                x=0.5, y=0.5, font_size=16, showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # 3. Sector Comparison
    st.markdown('<div class="section-title">🏛️ เปรียบเทียบปริมาณขยะตามสังกัด (ส่วนกลาง vs ส่วนภูมิภาค)</div>', unsafe_allow_html=True)
    sector_summary = df_filtered.groupby('สังกัด')[['ขยะที่เกิดขึ้น (กก.)', 'ใช้ประโยชน์ (กก.)', 'ขยะที่ส่งกำจัด (กก.)']].sum().reset_index()
    
    fig_sector = px.bar(
        sector_summary,
        x='สังกัด',
        y=['ใช้ประโยชน์ (กก.)', 'ขยะที่ส่งกำจัด (กก.)'],
        barmode='group',
        title="<b>เปรียบเทียบการจัดการขยะระหว่างสังกัด</b>",
        color_discrete_map={'ใช้ประโยชน์ (กก.)': '#2e7d32', 'ขยะที่ส่งกำจัด (กก.)': '#e53935'},
        labels={'value': 'ปริมาณขยะ (กก.)', 'variable': 'ประเภทการจัดการ'}
    )
    fig_sector.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,244,241,0.3)'
    )
    st.plotly_chart(fig_sector, use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">🏆 จัดอันดับหน่วยงานตามปริมาณขยะและประสิทธิภาพ</div>', unsafe_allow_html=True)
    
    rank_col1, rank_col2 = st.columns([1, 3])
    with rank_col1:
        metric_choice = st.selectbox(
            "📊 เลือกตัวชี้วัดสำหรับการจัดอันดับ",
            options=["ขยะที่เกิดขึ้น (กก.)", "ขยะที่ส่งกำจัด (กก.)", "ใช้ประโยชน์ (กก.)", "ร้อยละส่งกำจัดลดลง"],
            index=0
        )
        top_n = st.slider("🔢 จำนวนอันดับที่ต้องการแสดง (Top N)", min_value=5, max_value=25, value=10)
    
    with rank_col2:
        if metric_choice == "ร้อยละส่งกำจัดลดลง":
            agency_ranked = df_filtered.groupby('หน่วยงาน')[metric_choice].mean().reset_index()
        else:
            agency_ranked = df_filtered.groupby('หน่วยงาน')[metric_choice].sum().reset_index()
            
        agency_ranked = agency_ranked.sort_values(by=metric_choice, ascending=False).head(top_n)
        
        fig_rank = px.bar(
            agency_ranked,
            x=metric_choice,
            y='หน่วยงาน',
            orientation='h',
            title=f"<b>Top {top_n} หน่วยงาน: {metric_choice}</b>",
            color=metric_choice,
            color_continuous_scale="Greens" if "ประโยชน์" in metric_choice or "ลดลง" in metric_choice else "Reds",
            text_auto='.1f'
        )
        fig_rank.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor='rgba(240,244,241,0.3)'
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    # Correlation Scatter Plot
    st.markdown('<div class="section-title">🔍 ความสัมพันธ์ระหว่างจำนวนคนเฉลี่ย กับ ปริมาณขยะที่เกิดขึ้น</div>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        df_filtered,
        x='คนเฉลี่ย',
        y='ขยะที่เกิดขึ้น (กก.)',
        size='ขยะที่ส่งกำจัด (กก.)',
        color='สังกัด',
        hover_name='หน่วยงาน',
        hover_data=['เดือน', 'ขยะต่อคนต่อวัน (กก.)', 'ร้อยละส่งกำจัดลดลง'],
        title="<b>Scatter Plot: จำนวนบุคลากร vs ปริมาณขยะ (ขนาดจุดแสดงปริมาณขยะที่ส่งกำจัด)</b>",
        color_discrete_map={'ส่วนกลาง': '#1565c0', 'ส่วนภูมิภาค': '#2e7d32'}
    )
    fig_scatter.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(240,244,241,0.3)'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.markdown('<div class="section-title">📋 ข้อมูลดิบและตัวเลือกการส่งออก (Raw Data & Export)</div>', unsafe_allow_html=True)
    
    st.write(f"แสดงข้อมูลที่ผ่านการกรองแล้วทั้งหมด **{len(df_filtered):,}** รายการ:")
    
    # Column selector for table display
    show_cols = st.multiselect(
        "เลือกคอลัมน์ที่ต้องการแสดงผลในตาราง:",
        options=list(df_filtered.columns),
        default=['ปี', 'สังกัด', 'หน่วยงาน', 'เดือน', 'คนเฉลี่ย', 'ขยะที่เกิดขึ้น (กก.)', 'ใช้ประโยชน์ (กก.)', 'ขยะที่ส่งกำจัด (กก.)', 'ร้อยละส่งกำจัดลดลง', 'ขยะต่อคนต่อวัน (กก.)']
    )
    
    st.dataframe(
        df_filtered[show_cols],
        use_container_width=True,
        hide_index=True
    )
    
    # Download CSV Button
    csv_export = df_filtered.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลที่กรองแล้ว (CSV Format)",
        data=csv_export,
        file_name="filtered_dnp_waste_data.csv",
        mime="text/csv",
        help="คลิกเพื่อบันทึกไฟล์ข้อมูลเป็น UTF-8 CSV"
    )

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #757575; font-size: 0.85rem; padding: 1rem;">
    🌱 พัฒนาด้วย <b>Streamlit</b> และ <b>Plotly</b> | ชุดข้อมูล: กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช ผ่าน 
    <a href="https://data.go.th/dataset/gdpublish-69-dnp01-11-01" target="_blank" style="color: #2e7d32;">data.go.th</a>
</div>
""", unsafe_allow_html=True)
