import streamlit as st
import cv2
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode

st.set_page_config(page_title="كاشف الحساسية الغذائية", page_icon="⚠️", layout="centered")

cafeteria_items = {
    "6281002200204": {"الاسم": "شوكولاتة سنيكرز", "المكونات": ["فول سوداني", "شوكولاتة", "كاراميل", "حليب"], "الفئات": ["شوكولاتة", "مكسرات", "ألبان"]},
    "789101": {"الاسم": "عصير فراولة طبيعي", "المكونات": ["فراولة", "ماء", "سكر"], "الفئات": ["فراولة", "سكر"]},
    "112233": {"الاسم": "ساندوتش جبن", "المكونات": ["خبز", "جبن", "زبدة"], "الفئات": ["ألبان"]}
}

st.title("🛡️ كاشف المواد الحساسة")

allergy_options = ["فراولة", "شوكولاتة", "ألبان", "مكسرات", "سكر"]
user_allergies = st.sidebar.multiselect("حدد المواد الممنوعة:", allergy_options, default=["فراولة", "شوكولاتة"])

st.divider()

# الطريقة الأولى: الكاميرا
st.subheader("📸 تصوير الباركود")
camera_image = st.camera_input("صور الباركود")

if camera_image:
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    detected_barcodes = decode(cv_img)
    
    if detected_barcodes:
        for barcode in detected_barcodes:
            barcode_data = barcode.data.decode('utf-8')
            if barcode_data in cafeteria_items:
                item = cafeteria_items[barcode_data]
                st.success(f"المنتج: {item['الاسم']}")
                st.write(f"المكونات: {', '.join(item['المكونات'])}")
                matched = [a for a in user_allergies if a in item["الفئات"]]
                if matched:
                    st.error(f"🚨 تحذير! يحتوي على: {', '.join(matched)}")
                else:
                    st.success("✅ آمن.")
            else:
                st.warning(f"⚠️ باركود غير مسجل: {barcode_data}")
    else:
        st.warning("⚠️ ما لقيت باركود واضح. استخدم البحث السريع بالأسفل 👇")

st.divider()

# الطريقة الثانية: بحث سريع يفك الحشرة
st.subheader("⚡ بحث سريع بالاسم (بدون كاميرا)")
item_names = [item["الاسم"] for item in cafeteria_items.values()]
selected_name = st.selectbox("اختر المنتج:", item_names)

for code, item in cafeteria_items.items():
    if item["الاسم"] == selected_name:
        st.write(f"**المكونات:** {', '.join(item['المكونات'])}")
        matched = [a for a in user_allergies if a in item["الفئات"]]
        if matched:
            st.error(f"🚨 تحذير! يحتوي على: {', '.join(matched)}")
        else:
            st.success("✅ آمن.")
