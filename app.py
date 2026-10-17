import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="كاشف الحساسية الذكي", page_icon="🤖", layout="centered")

st.title("🤖 كاشف الحساسية بالذكاء الاصطناعي")
st.write("صور أي منتج في المقصف (شيبس، عصير، ساندوتش)، والذكاء الاصطناعي بيعرفه فوراً ويحلل مكوناته.")

allergy_options = ["فراولة", "شوكولاتة", "ألبان", "مكسرات", "بيض", "سمسم", "سكر", "جلوتين"]
user_allergies = st.sidebar.multiselect("حدد المواد الممنوعة عليك:", allergy_options, default=["فراولة", "شوكولاتة", "مكسرات"])

st.divider()

camera_image = st.camera_input("📸 صور المنتج")

if camera_image:
    image = Image.open(camera_image)
    st.image(image, caption="المنتج الملتقط", use_container_width=True)
    
    with st.spinner("جاري فحص المنتج..."):
        try:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            prompt = f"""
            أنت مساعد ذكي لكشف الحساسية الغذائية في المقصف المدرسي.
            حلل صورة المنتج (مثل الشيبس، العصائر، الساندوتشات، المخبوزات، أو الحلويات المتوفرة في المتاجر).
            أجب بدقة عن التالي:
            1. اسم المنتج التجاري أو نوعه بدقة.
            2. أهم المكونات الموجودة فيه عادةً.
            3. هل يحتوي على أي من هذه المواد الممنوعة على المستخدم: {', '.join(user_allergies)}؟
            
            كن دقيقاً، واذكر تحذيراً واضحة إذا وُجدت المادة الممنوعة.
            """
            
            response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents=[image, prompt]
)
            
            st.markdown("### 📋 نتيجة التحليل:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"خطأ في الاتصال: تأكد من إضافة مفتاح الـ API في Streamlit Secrets. التفاصيل: {e}")
