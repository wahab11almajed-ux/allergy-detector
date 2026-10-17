import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="كاشف الحساسية الغذائية", page_icon="⚠️", layout="centered")

# قاعدة بيانات تجريبية لأصناف المقصف والمكونات
cafeteria_items = {
    "123456": {"الاسم": "فطيرة شوكولاتة", "المكونات": ["دقيق", "شوكولاتة", "سكر", "حليب"], "الفئات": ["شوكولاتة", "ألبان", "سكر"]},
    "789101": {"الاسم": "عصير فراولة طبيعي", "المكونات": ["فراولة", "ماء", "سكر"], "الفئات": ["فراولة", "سكر"]},
    "112233": {"الاسم": "ساندوتش جبن", "المكونات": ["خبز", "جبن", "زبدة"], "الفئات": ["ألبان"]}
}

st.title("🛡️ كاشف المواد الحساسة عبر الكاميرا")
st.write("وجه كاميرا الجوال على باركود المنتج أو التقط صورة للمكونات لفحصها.")

# إعدادات المستخدم (مسببات الحساسية)
st.sidebar.header("إعدادات الحساسية")
allergy_options = ["فراولة", "شوكولاتة", "ألبان", "مكسرات", "بيض", "سمسم", "سكر"]
user_allergies = st.sidebar.multiselect("حدد المواد الممنوعة:", allergy_options, default=["فراولة", "شوكولاتة"])

st.divider()

# خيار استخدام كاميرا الجوال مباشرة
camera_image = st.camera_input("📸 تصوير المنتج أو الباركود")

if camera_image:
    img = Image.open(camera_image)
    st.image(img, caption="الصورة الملتقطة", use_column_width=True)
    
    st.info("جاري تحليل المكونات...")
    
    detected_code = "789101" # مثال افتراضي لنتيجة الكاميرا
    
    if detected_code in cafeteria_items:
        item = cafeteria_items[detected_code]
        st.write(f"**المنتج التعرف عليه:** {item['الاسم']}")
        st.write(f"**المكونات:** {', '.join(item['المكونات'])}")
        
        matched = [a for a in user_allergies if a in item["الفئات"]]
        if matched:
            st.error(f"🚨 تحذير خطير! المنتج يحتوي على: {', '.join(matched)}")
        else:
            st.success("✅ المنتج آمن.")
    else:
        st.warning("⚠️ لم يتم التعرف على المنتج، أضفه لقاعدة البيانات.")

st.divider()

selected_name = st.selectbox("أو اختر المنتج يدويًا:", [item["الاسم"] for item in cafeteria_items.values()])