# ♻️ แดชบอร์ดสถิติปริมาณขยะมูลฝอย กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช (DNP Waste Management Dashboard)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

เว็บแอปพลิเคชันสำหรับสำรวจและวิเคราะห์ข้อมูลสถิติปริมาณขยะมูลฝอย การนำไปใช้ประโยชน์ และประสิทธิผลการลดปริมาณขยะของหน่วยงานในสังกัดกรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช พัฒนาด้วย **Python**, **Pandas**, **Plotly** และ **Streamlit**

---

## 📌 ข้อมูลชุดข้อมูล (Dataset Source)

- **ชื่อชุดข้อมูล:** ปริมาณขยะมูลฝอย (Department of National Parks, Wildlife and Plant Conservation)
- **แหล่งที่มา:** [data.go.th (Open Government Data of Thailand)](https://data.go.th/dataset/gdpublish-69-dnp01-11-01)
- **หน่วยงานเจ้าของข้อมูล:** กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช กระทรวงทรัพยากรธรรมชาติและสิ่งแวดล้อม
- **ช่วงปีของข้อมูล:** ปีงบประมาณ พ.ศ. 2568 - 2569 (รวม 579 รายการ ครอบคลุม 54 หน่วยงาน)

---

## 🚀 คุณสมบัติและฟังก์ชันการทำงาน (Features)

### 1. 🎛️ Interactive Widgets (ตัวกรองข้อมูลแบบมีปฏิสัมพันธ์)
- **เลือกปีงบประมาณ:** ตัวเลือกแสดงข้อมูลปี 2568, 2569 หรือข้อมูลรวมทั้งหมด
- **เลือกสังกัด:** ตัวเลือก Radio button กรองระหว่าง *ส่วนกลาง* และ *ส่วนภูมิภาค*
- **เลือกหน่วยงาน:** Multi-select ค้นหาและเปรียบเทียบเฉพาะหน่วยงานที่สนใจ
- **เลือกช่วงเดือน:** Range Slider กำหนดช่วงเดือนในการวิเคราะห์ (มกราคม - ธันวาคม)
- **เลือกตัวชี้วัดการจัดอันดับ:** ปรับเปลี่ยนเกณฑ์ในกราฟแท่งแบบไดนามิก
- **ปุ่มดาวน์โหลดข้อมูล:** Export ข้อมูลที่ผ่านการกรองแล้วเป็นไฟล์ CSV (UTF-8)

### 2. 📊 กราฟและ Data Visualizations (5 รูปแบบ)
1. **กราฟแนวโน้มปริมาณขยะรายเดือน (Stacked Bar + Trend Line):** แสดงขยะที่นำไปใช้ประโยชน์, ขยะที่ส่งกำจัด และแนวโน้มขยะรวม
2. **กราฟสัดส่วนการจัดการขยะ (Donut Chart):** สัดส่วนเปอร์เซ็นต์ระหว่างขยะที่นำไปใช้ประโยชน์ vs ขยะที่ส่งกำจัด
3. **กราฟเปรียบเทียบตามสังกัด (Grouped Bar Chart):** เปรียบเทียบปริมาณขยะและการจัดการระหว่างส่วนกลางและส่วนภูมิภาค
4. **กราฟจัดอันดับหน่วยงาน Top N (Horizontal Bar Chart):** จัดอันดับตามปริมาณขยะ หรือร้อยละการลดขยะ
5. **กราฟการกระจายตัว (Scatter Plot):** ความสัมพันธ์ระหว่างจำนวนบุคลากรเฉลี่ย กับ ปริมาณขยะที่เกิดขึ้น (พร้อมสเกลขนาดตามปริมาณขยะที่ส่งกำจัด)

### 3. 🎯 ดัชนีชี้วัดหลัก (KPI Metrics)
- ปริมาณขยะที่เกิดขึ้นทั้งหมด (กก. / ตัน)
- ปริมาณขยะที่นำไปใช้ประโยชน์ (กก. และ สัดส่วน %)
- ปริมาณขยะที่ส่งกำจัด (กก. และ สัดส่วน %)
- อัตราการลดปริมาณขยะเฉลี่ย (%)
- ปริมาณขยะเฉลี่ยต่อคนต่อวัน (กก./คน/วัน)

---

## 📂 โครงสร้างไฟล์ในโปรเจกต์ (Project Structure)

```text
├── app.py                   # Source Code หลักของ Streamlit Web Application
├── prepare_data.py          # สคริปต์สำหรับการดึง รวม และทำความสะอาดข้อมูล (Data Cleaning)
├── waste_data_cleaned.csv   # ชุดข้อมูลที่ผ่านการทำความสะอาดและบันทึกเป็น UTF-8
├── waste_2568.csv           # ข้อมูลดิบปี 2568
├── waste_2569.csv           # ข้อมูลดิบปี 2569
├── requirements.txt         # รายการ Dependencies สำหรับการรันและ Deploy
├── .gitignore               # กำหนดไฟล์ที่ไม่ต้องนำขึ้น Git
└── README.md                # เอกสารคู่มือโปรเจกต์
```

---

## 💻 การติดตั้งและทดสอบบนเครื่อง (Local Setup)

1. **Clone หรือเปิดโฟลเดอร์โปรเจกต์:**
   ```bash
   cd "Streamlit Data"
   ```

2. **ติดตั้ง Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **รัน Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

4. **เปิดเบราว์เซอร์:**
   เข้าใช้งานผ่าน URL: `http://localhost:8501`

---

## ☁️ ขั้นตอนการ Deploy บน Streamlit Community Cloud

### ขั้นตอนที่ 1: นำ Source Code ขึ้น GitHub
1. สร้าง New Repository บน [GitHub](https://github.com/new) เช่น ตั้งชื่อว่า `dnp-waste-streamlit`
2. รันคำสั่ง Git ในโฟลเดอร์โปรเจกต์:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit for DNP waste dashboard"
   git branch -M main
   git remote add origin https://github.com/Jettarin010/dnp-waste-streamlit.git
   git push -u origin main
   ```

### ขั้นตอนที่ 2: Deploy บน Streamlit Community Cloud
1. ไปที่เว็บไซต์ [share.streamlit.io](https://share.streamlit.io) และลงชื่อเข้าใช้ด้วยบัญชี GitHub
2. กดปุ่ม **"Create app"** (หรือ "New app")
3. กรอกข้อมูลการตั้งค่า:
   - **Repository:** `Jettarin010/dnp-waste-streamlit`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (กำหนดเองได้):** เช่น `dnp-waste-dashboard.streamlit.app`
4. กดปุ่ม **"Deploy!"**
5. รอระบบ Build ประมาณ 1-2 นาที คุณจะได้ URL เว็บไซต์จริงที่ทุกคนสามารถเข้าชมได้ทันที!
