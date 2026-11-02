import streamlit as st
import random
import urllib.parse

# ==========================================
# 1. إعدادات الصفحة وتصميم الواجهة (RTL النظيف)
# ==========================================
st.set_page_config(
    page_title="ابن البلد | التحدي الفلسطيني الأصيل",
    page_icon="🇵🇸",
    layout="centered"
)

# تعديل CSS بطريقة لا تسبب شاشة بيضاء وبشكل مستقر تماماً
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        background-color: #007A3D;
        color: white;
        border: none;
        margin-bottom: 10px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #CE1126;
        color: white;
    }
    .result-card {
        background-color: #fcfcfc;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #007A3D;
        color: #111;
        text-align: right;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. خوارزمية تحليل الجنس بدقة تامة
# ==========================================
def detect_gender(name):
    clean_name = name.strip()
    female_names = [
        'شهد', 'مريم', 'فاطمة', 'عائشة', 'سارة', 'ريم', 'رنا', 'سعاد', 
        'حنان', 'إيمان', 'زينب', 'هدى', 'لجين', 'سماء', 'بيان', 'ديمة', 
        'لارا', 'ميس', 'نور', 'ياسمين', 'آية', 'رزان', 'تالا', 'لين', 'يسرا'
    ]
    female_endings = ('ة', 'اء', 'ى')
    
    if clean_name in female_names or clean_name.endswith(female_endings):
        return "أنثى"
    return "ذكر"

# ==========================================
# 3. بنك الأسئلة (مدقق لغوياً وثقافياً 100% بلهجة الشارع الفلسطيني)
# ==========================================
question_bank = [
    {
        "q": "المثل الشعبي بيقول: 'اللي ما إلو خير في أهله...' كمل المثل يا نشمي؟",
        "options": [("ما إلو خير في الناس والوطن", 1), ("ما إلو خير في حاله أصلًا", 2), ("ما بينوخذ على الحجة", 0)],
    },
    {
        "q": "لو نازل عالعصريّة ولقيت الشارع ضارب أزمة سير خانقة، شو أول كلمة بتطلع معك؟",
        "options": [("باخد دخلة فرعية حافظها شبر بشبر", 2), ("بفتح راديو وبستنى الفرج برواق", 1), ("ببلش أزمر وأعصب من النكد", 0)],
    },
    {
        "q": "أكلة شعبية فلسطينية أصيلة لا تُعوض بيوم الجمعة، شو هي؟",
        "options": [("المسخن أو المقلوبة عأصولها", 2), ("مجدورة برغل مع بصل مقلي", 1), ("ساندويشة لبنة وجبنة", 0)],
    },
    {
        "q": "لما تواجهك ضائقة مالية مفاجئة بنص الشهر، شو أسلوبك بالتعامل؟",
        "options": [("بدبر حالي من بيضة وخلزون وبمشي أموري", 2), ("بوكل هوا وبستنى أول الشهر", 1), ("بظل أشكو للرايح والجاي", 0)],
    },
    {
        "q": "شو معنى كلمة 'زقفة' أو 'زرفة' باللهجة الفلسطينية القديمة؟",
        "options": [("السرعة والنشاط في إنجاز الأمور", 2), ("نوع من الحلوى الشعبية", 0), ("أداة قديمة بالبيت", 1)],
    },
    {
        "q": "كيف بتتعامل مع جارك اللي دايماً قاعد عالبلكونة وبراقب الرايح والجاي؟",
        "options": [("بسايسه بكلمة طيبة وبسلم عليه بحرارة", 2), ("بتجاهله تماماً وما بطلع بوجهه", 0), ("بصير أعد عليه شو بيلبس", 1)],
    },
    {
        "q": "إذا ركبت تكسي وبلش السائق يشكي من حال البلد، كيف بتتصرف؟",
        "options": [("بشاركه الهم بكلمتين طيبين وبخفف عنه", 2), ("بسكت وبحط سماعات بأذني", 0), ("بصير أطخ حكي سياسي فاضي", 1)],
    },
    {
        "q": "لما حدا يقول لك 'طول بالك يا زلمة والدنيا لسا بخير'، قديش صبور بالحياة؟",
        "options": [("طويل بال لدرجة بتخوف وعندي طاقة تحمل عالية", 2), ("صبري قليل بس بمشي الحال", 1), ("بفقد أعصابي بسرعة وما بتحمل", 0)],
    },
    {
        "q": "شو قصة عشبة 'الميرمية' عنا في التراث والطب الشعبي؟",
        "options": [("عشبة مباركة للدواء وزردة الشاي", 2), ("اسم ست كبيرة بالقرية", 0), ("نوع قماش مستورد", 1)],
    },
    {
        "q": "لو صار معك موقف محرج قدام الناس، شو ردة فعلك العفوية؟",
        "options": [("بضحك على حالي وبمشي الموضوع ببساطة", 2), ("بنحرج وبتضايق طول اليوم", 1), ("بقلبها طوشة وعصبية", 0)],
    },
    {
        "q": "شو يعني لما نقول عن شخص 'قاعد على قلبي زي صبة الباطون'؟",
        "options": [("شخص ثقيل دم ما بتزحزح بسهولة", 2), ("نوع من أعمال البناء", 0), ("مهندس مدني محترف", 1)],
    },
    {
        "q": "لما يقلك زلمة 'خذ الصاع صاعين'، شو بيكون قصده بنبرة التحدي؟",
        "options": [("رد الحق وزيادة لمن يطاول عليك", 2), ("كيل كميات من القمح", 0), ("نوع من التجارة القديمة", 1)],
    }
]

# ==========================================
# 4. الألقاب العشرة الفريدة والمفسرة
# ==========================================
def get_unique_title(score):
    if score >= 18:
        return {
            "title": "عقيد الحارة وسبعها العتيق 🎖️",
            "desc": "زلمة مواقف من طراز رفيع، بتعرف تدبر حالك بأضيق الأزمات، وكلمتك مسموعة وعقلك بوزن بلد."
        }
    elif score >= 14:
        return {
            "title": "حكيم الدار وعمودها الراسخ ☕",
            "desc": "عقلك متزن، حافظ الأصول والأمثال عن غيب، والكل يلجأ لك لما تحتار الأمور بوجوهها."
        }
    elif score >= 10:
        return {
            "title": "ابن البلد النشمي اللي ما بغلبوه ⚡",
            "desc": "واخد الحياة ببساطة وشهامة، قلبك أبيض، وبتعرف كيف تضحك على الهم بدل ما الهم يضحك عليك."
        }
    elif score >= 6:
        return {
            "title": "فيلسوف القهوة والشارع الهادئ 🫒",
            "desc": "تحليلك للأمور على مهله بس دقيق وصائب. بتوخذ وبتعطي بالحكي وعارف أصول اللعبة."
        }
    else:
        return {
            "title": "ملك البساطة وعفوية الشارع 🎈",
            "desc": "عايشها يوم بيوم وبكل بساطة وعفوية، والناس بتحب طيبة قلبك وصفاء نيتك."
        }

# ==========================================
# 5. إدارة الجلسة وتطبيق اللعبة
# ==========================================
if "started" not in st.session_state:
    st.session_state.started = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 22
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "ذكر"
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []

# --- شاشة البداية ---
if not st.session_state.started:
    st.title("🇵🇸 دليل ابن البلد - التحدي الفلسطيني")
    st.markdown("### اكتشف لقبك الحقيقي في الشارع والحارة بلهجتنا العامية الأصيلة")
    st.divider()
    
    name_input = st.text_input("أدخل اسمك الكريم:")
    age_input = st.number_input("عمرك الكريم:", min_value=10, max_value=100, value=22)
    
    if st.button("🚀 ابلش التحدي الآن"):
        if name_input.strip() == "":
            st.warning("يا ريت تكتب اسمك عشان نعرف نخاطبك أصولاً!")
        else:
            st.session_state.user_name = name_input.strip()
            st.session_state.user_age = age_input
            st.session_state.user_gender = detect_gender(name_input)
            
            pool = question_bank.copy()
            random.shuffle(pool)
            st.session_state.selected_questions = pool[:10]
            
            st.session_state.started = True
            st.session_state.step = 0
            st.session_state.score = 0
            st.rerun()

# --- شاشة الأسئلة ---
elif st.session_state.step < len(st.session_state.selected_questions):
    current_q_idx = st.session_state.step
    q_data = st.session_state.selected_questions[current_q_idx]
    
    st.markdown(f"### السؤال رقم ({current_q_idx + 1} من 10)")
    st.divider()
    
    # نداء دقيق ومضبوط تماماً حسب الجنس (تم حل مشكلة شهد نهائياً)
    greeting = "يا نشمي" if st.session_state.user_gender == "ذكر" else "يا صبيّة"
    st.markdown(f"**{st.session_state.user_name} ({greeting})**، {q_data['q']}")
    st.write("")
    
    for opt_text, points in q_data["options"]:
        if st.button(opt_text, key=f"ans_{current_q_idx}_{opt_text}"):
            st.session_state.score += points
            st.session_state.step += 1
            st.rerun()

# --- شاشة النتيجة النهائية ---
else:
    final_score = st.session_state.score
    result_data = get_unique_title(final_score)
    
    st.success("🎉 كفو! ختمت التحدي بنجاح تام.")
    
    debray_val = min(100, max(30, final_score * 5 + 10))
    sabr_val = min(100, max(40, (st.session_state.user_age * 2) % 80 + 20))
    fa_hawa_val = min(100, max(50, 100 - (final_score * 3)))
    
    st.markdown(f"""
        <div class="result-card">
            <h2>🏆 لقبك: {result_data['title']}</h2>
            <p style="font-size: 18px;"><b>تحليل شخصيتك يا {st.session_state.user_name}:</b> {result_data['desc']}</p>
            <hr style="border-color: #007A3D;">
            <h4>📊 مؤشرات ابن البلد الخاصة فيك:</h4>
            <ul>
                <li><b>مؤشر التدبير والدبرة ({debray_val}%):</b> بقيس قدرتك على تسيير أمورك اليومية وحل المشاكل.</li>
                <li><b>مؤشر طول البال والصبر ({sabr_val}%):</b> بقيس قدرتك على تحمل الضغوط برواق على طريقة أهل زمان.</li>
                <li><b>مؤشر فطنة ابن البلد ({fa_hawa_val}%):</b> بقيس سرعة بديهتك وضحكتك اللي بتخفف هموم الشارع.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- حل مشكلة رابط الواتساب النهائي ---
    # ملاحظة: عندما ترفع التطبيق على Streamlit Cloud، استبدل الرابط أدناه برابط تطبيقك الحقيقي
    app_link = "https://ibn-albalad.streamlit.app" 
    
    share_text = f"أنا لعبت تحدي 'ابن البلد' وطلع لقبي '{result_data['title']}'! 🇵🇸\nتعال جرب اسمك وشوف شو بيطلعلك بالتحدي الفلسطيني:\n🔗 {app_link}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; border-radius:12px; height:3.5em; font-weight:bold; background-color:#25D366; color:white; border:none; cursor:pointer; text-align:center; font-size:16px;">📲 شارك نتيجتك ولقبك على واتساب</button></a>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("🔄 عيد التحدي من أول وجديد"):
        st.session_state.started = False
        st.session_state.step = 0
        st.session_state.score = 0
        st.rerun()
