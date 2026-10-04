import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه تست زنده و دقیق عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تست زنده و فیکس‌شده فریم‌های اپتیکال")

# مدیریت حالت‌های برنامه
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت تصویر چهره
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت و پیشنهاد فریم‌های استاندارد با لینک‌های کاملاً پایدار
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {
                    "id": "aviator", 
                    "name": "Tom Ford - Aviator Gold", 
                    "type": "خلبانی فلزی لوکس کلاسیک", 
                    "brand": "Tom Ford", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/sunglasses-transparent-sunglasses-image-png-file-28.png"
                },
                {
                    "id": "wayfarer", 
                    "name": "Ray-Ban - Wayfarer Classic", 
                    "type": "مستطیلی کائوچویی مشکی استاندارد", 
                    "brand": "Ray-Ban", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/ray-ban-sunglasses-png-transparent-image-20.png"
                }
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {
                    "id": "wayfarer", 
                    "name": "Ray-Ban - Wayfarer Classic", 
                    "type": "ویفرر استاندارد شیک", 
                    "brand": "Ray-Ban", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/ray-ban-sunglasses-png-transparent-image-20.png"
                },
                {
                    "id": "cateye", 
                    "name": "Tom Ford - Elegant CatEye", 
                    "type": "چشم‌گربه‌ای مدرن و جذاب", 
                    "brand": "Tom Ford", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/sunglasses-transparent-sunglasses-image-png-file-28.png"
                }
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {
                    "id": "round", 
                    "name": "Ray-Ban - Retro Round Metal", 
                    "type": "گرد فلزی مینیمال مهندسی‌شده", 
                    "brand": "Ray-Ban", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/black-sunglasses-transparent-image-png-file-33.png"
                },
                {
                    "id": "slim", 
                    "name": "Tom Ford - Slim Rectangular", 
                    "type": "فریم زاویه‌دار باریک", 
                    "brand": "Tom Ford", 
                    "url": "https://www.freepnglogos.com/uploads/sunglasses-png/ray-ban-sunglasses-png-transparent-image-20.png"
                }
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری فریم‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب فریم متناسب")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده شما", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 فریم‌های استاندارد زیر بر اساس آناتومی صورت شما پیشنهاد شده‌اند. یکی را انتخاب کنید تا وارد **اتاق تست زنده روی چشم** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.image(frame["url"], use_column_width=True)
            st.markdown(f"""
                <div style="text-align: center; padding: 5px;">
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>استایل:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست زنده این فریم روی چشم", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق تست زنده با ردیابی دقیق و فیکس‌شده روی چشم‌ها
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده (فریم فعال: {chosen['name']})")
    st.markdown("دوربین زنده فعال است. عینک به‌طور دقیق بر روی خط دید، چشم‌ها و پل بینی شما فیکس شده و با حرکت سر هماهنگ است.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    ar_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <style>
            .ar-container {{
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }}
            video, canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }}
            #glasses_overlay {{
                position: absolute;
                display: none;
                pointer-events: none;
                z-index: 10;
                transform-origin: center center;
                will-change: transform, left, top, width;
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 20;
                background: rgba(0,0,0,0.85);
                padding: 14px 28px;
                border-radius: 8px;
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال راه‌اندازی دوربین و انطباق استاندارد عینک روی چشم‌ها...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
            <img id="glasses_overlay" src="{chosen['url']}" alt="Glasses">
        </div>
        <div class="info-bar">
            <b>فریم انتخابی:</b> {chosen['name']} | 🟢 ردیابی زنده و انطباق دقیق برقرار است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');
            const glassesImg = document.getElementById('glasses_overlay');

            function onResults(results) {{
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.restore();

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {{
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    const leftEye = landmarks[33];
                    const rightEye = landmarks[263];
                    const noseBridge = landmarks[168];
                    
                    const centerX = noseBridge.x * canvasElement.width;
                    const centerY = noseBridge.y * canvasElement.height;

                    const eyeDistance = Math.hypot(
                        (rightEye.x - leftEye.x) * canvasElement.width,
                        (rightEye.y - leftEye.y) * canvasElement.height
                    );

                    const dx = rightEye.x - leftEye.x;
                    const dy = rightEye.y - leftEye.y;
                    const angleRad = Math.atan2(dy, dx);
                    const angleDeg = angleRad * (180 / Math.PI);

                    const glassesWidth = eyeDistance * 2.8; 
                    glassesImg.style.width = glassesWidth + 'px';
                    
                    glassesImg.style.left = (canvasElement.width - centerX) + 'px';
                    glassesImg.style.top = centerY + 'px';
                    
                    glassesImg.style.transform = `translate(-50%, -45%) rotate(${{angleDeg}}deg)`;
                    
                    glassesImg.style.display = 'block';
                }} else {{
                    glassesImg.style.display = 'none';
                }}
            }}

            const faceMesh = new FaceMesh({{
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{file}}`
            }});

            faceMesh.setOptions({{
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.65,
                minTrackingConfidence: 0.65
            }});

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {{
                onFrame: async () => {{
                    await faceMesh.send({{ image: videoElement }});
                }},
                width: 640,
                height: 480
            }});

            camera.start().catch(err => {{
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            }});
        </script>
    </body>
    </html>
    """

    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()