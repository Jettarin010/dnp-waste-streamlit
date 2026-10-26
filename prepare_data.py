import pandas as pd
import numpy as np

# Load 2568 and 2569
df2568 = pd.read_csv('waste_2568.csv', encoding='cp874')
df2569 = pd.read_csv('waste_2569.csv', encoding='cp874')

# Standardize column names
df2569 = df2569.rename(columns={
    'นำไปใช้ประโยชน์ (กก.)': 'ใช้ประโยชน์ (กก.)',
    'ร้อยละขยะส่งกำจัดลดลง': 'ร้อยละส่งกำจัดลดลง'
})

# Combine
df = pd.concat([df2568, df2569], ignore_index=True)

# Clean numeric columns
numeric_cols = [
    'คนเฉลี่ย', 'วันทำงาน', 'โฟมบรรจุอาหาร (ใบ)',
    'ขยะที่เกิดขึ้น (กก.)', 'ใช้ประโยชน์ (กก.)', 
    'ขยะที่ส่งกำจัด (กก.)', 'ร้อยละส่งกำจัดลดลง'
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', '').str.strip(), 
            errors='coerce'
        ).fillna(0)

# Month order mapping
month_order = {
    'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4,
    'พฤษภาคม': 5, 'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8,
    'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12
}

df['ลำดับเดือน'] = df['เดือน'].map(month_order).fillna(99).astype(int)

# Clean whitespace
df['สังกัด'] = df['สังกัด'].astype(str).str.strip()
df['หน่วยงาน'] = df['หน่วยงาน'].astype(str).str.strip()
df['เดือน'] = df['เดือน'].astype(str).str.strip()

# Add calculated metrics
df['อัตราการนำไปใช้ประโยชน์ (%)'] = np.where(
    df['ขยะที่เกิดขึ้น (กก.)'] > 0,
    (df['ใช้ประโยชน์ (กก.)'] / df['ขยะที่เกิดขึ้น (กก.)']) * 100,
    0.0
).round(2)

df['ขยะต่อคนต่อวัน (กก.)'] = np.where(
    (df['คนเฉลี่ย'] * df['วันทำงาน']) > 0,
    df['ขยะที่เกิดขึ้น (กก.)'] / (df['คนเฉลี่ย'] * df['วันทำงาน']),
    0.0
).round(4)

# Save as UTF-8
output_csv = 'waste_data_cleaned.csv'
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"Successfully processed and saved {len(df)} rows to {output_csv}")
print("Columns:", df.columns.tolist())
print(df.head(2))
