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
st.write("صور باركود المنتج بالمقصف للتحقق من المكونات.")

allergy_options = ["فراولة", "شوكولاتة", "ألبان", "مكسرات", "سكر"]
user_allergies = st.sidebar.multiselect("حدد المواد الممنوعة:", allergy_options, default=["فراولة", "شوكولاتة"])

st.divider()

camera_image = st.camera_input("📸 تصوير باركود المنتج")

if camera_image:
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    detected_barcodes = decode(cv_img)
    
    if detected_barcodes:
        for barcode in detected_barcodes:
            barcode_data = barcode.data.decode('utf-8')
            st.success(f"تم قراءة الباركود: {barcode_data}")
            
            if barcode_data in cafeteria_items:
                item = cafeteria_items[barcode_data]
                st.write(f"**المنتج:** {item['الاسم']}")
                st.write(f"**المكونات:** {', '.join(item['المكونات'])}")
                
                matched = [a for a in user_allergies if a in item["الفئات"]]
                if matched:
                    st.error(f"🚨 تحذير! المنتج يحتوي على: {', '.join(matched)}")
                else:
                    st.success("✅ المنتج آمن.")
            else:
                st.warning(f"⚠️ الباركود ({barcode_data}) غير مسجل.")
    else:
        st.warning("⚠️ لم يتم العثور على باركود واضح.")

st.divider()
selected_name = st.selectbox("أو اختر المنتج يدويًا:", [item["الاسم"] for item in cafeteria_items.values()])
