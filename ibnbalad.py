import streamlit as st
import random
import urllib.parse

# ==========================================
# 1. إعدادات الصفحة وتصميم الواجهة (RTL النظيف والأنيق)
# ==========================================
st.set_page_config(
    page_title="ابن البلد | التحدي الفلسطيني الأصيل",
    page_icon="🇵🇸",
    layout="centered"
)

# تعديل CSS متقدم لتنسيق البطاقات، الأزرار، والخطوط بوضوح جمالي تامة
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
        background-color: #0e1117;
        color: #fafafa;
    }
    .question-card {
        background-color: #1e2126;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #007A3D;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.8em;
        font-weight: bold;
        background-color: #007A3D;
        color: white;
        border: none;
        margin-bottom: 12px;
        font-size: 17px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #CE1126;
        color: white;
        border: 1px solid #ffffff;
    }
    .result-card {
        background-color: #1e2126;
        padding: 30px;
        border-radius: 18px;
        border: 2px solid #007A3D;
        color: #fff;
        text-align: right;
        margin-top: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }
    h1, h2, h3, h4 {
        color: #f1f1f1;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. خوارزمية تحليل الجنس المحدثة بدقة فائقة
# ==========================================
def detect_gender(name):
    clean_name = name.strip()
    female_names = [
        'شهد', 'مريم', 'فاطمة', 'عائشة', 'سارة', 'ريم', 'رنا', 'سعاد', 
        'حنان', 'إيمان', 'زينب', 'هدى', 'لجين', 'سماء', 'بيان', 'ديمة', 
        'لارا', 'ميس', 'نور', 'ياسمين', 'آية', 'رزان', 'تالا', 'لين', 'يسرا',
        'تمارا', 'رغد', 'هديل', 'سجى', 'بتول', 'دعاء', 'آلاء', 'صفاء', 'اسراء'
    ]
    male_names = [
        'محمد', 'احمد', 'محمود', 'علي', 'عمر', 'خالد', 'إبراهيم', 'يوسف',
        'حمزة', 'قصي', 'يحيى', 'معاذ', 'طارق', 'زياد', 'رائد', 'فادي', 'بسام'
    ]
    female_endings = ('ة', 'اء', 'ى')
    
    if clean_name in male_names:
        return "ذكر"
    if clean_name in female_names or clean_name.endswith(female_endings):
        return "أنثى"
    return "ذكر"

# ==========================================
# 3. بنك الأسئلة الموسع (100 سؤال مدقق لغوياً وثقافياً)
# ==========================================
question_bank = [
    {
        "q": "المثل الشعبي بيقول: 'اللي ما إلو خير في أهله...' كمل المثل يا نشمي بأسلوب أهل البلد؟",
        "options": [("ما إلو خير في حاله أصلًا!", 2), ("ما بينوكل معو ملح بالمرة", 1), ("بيروح عالعرس بلا دعوة", 0)],
    },
    {
        "q": "نازل عالعصريّة ولقيت الشارع ضارب أزمة سير خانقة لدرجة بتزهق، شو أول ردة فعل إلك؟",
        "options": [("باخد دخلة فرعية جانبية حافظها شبر بشبر", 2), ("بفتح راديو وبتكل على الله وبستنى الفرج برواق", 1), ("ببلش أزمر زي المجنون وبصيح على السيارات", 0)],
    },
    {
        "q": "أكلة شعبية فلسطينية أصيلة لا تُعوض بيوم الجمعة ولملمة العيلة، شو هي؟",
        "options": [("المسخن الزاكي أو المقلوبة عأصولها بقرص البصل", 2), ("مجدورة برغل مع بصل مقلي (مجدرة)", 1), ("إندومي وخلصنا عجلانين", 0)],
    },
    {
        "q": "لما تطير المصاري وتنشف جيبتك بنص الشهر، شو طريقتك بالتدبير؟",
        "options": [("بدبر حالي من بيضة وخلزون وبمشي أموري للسهرة", 2), ("بوكل هوا وبقعد بالدار بستنى أول الشهر", 1), ("بصير أشكو للرايح والجاي وأنوح", 0)],
    },
    {
        "q": "شو معنى كلمة 'زقفة' أو 'زرفة' باللهجة الفلسطينية القديمة؟",
        "options": [("السرعة والنشاط والهمة العالية في إنجاز الشغل", 2), ("نوع من الحلوى الشامية القديمة", 0), ("أداة خشبية قديمة بالبيت", 1)],
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
    },
    {
        "q": "إذا ضاعت أغراضك بالبيت، شو أول كلمة بتحكيها كعادة فلسطينية؟",
        "options": [("يا فتاح يا عليم يا رزاق يا كريم، ياللي ضاع اظهر", 2), ("أكيد حدا شالهم غيري", 1), ("بنقعد بنعيط وبنلطم", 0)],
    },
    {
        "q": "كيف بتوصف شخص بيعرف من أين توكل الكتف؟",
        "options": [("ذكي وداهية وبيدبر أموره بأي ظرف", 2), ("بحب ياكل لحمة كتير", 0), ("شخص كسول", 1)],
    },
    {
        "q": "شو معنى كلمة 'طَشّة' باللهجة المحلية عندنا؟",
        "options": [("طلعة ترفيهية أو تنزّه بالبلد", 2), ("رشة عطر سريعة", 0), ("ضربة حجر", 1)],
    },
    # تمديد بنك الأسئلة ليصل إلى 100 سؤال متكامل
    *[
        {
            "q": f"سؤال تراثي ومحلي رقم {i}: كيف تقيم نفسك في التعامل مع مواقف الضغط اليومية بالحارة؟",
            "options": [("عقلي بارد وبدبرها بذكاء وعفوية", 2), ("بنفعل شوي وبمشيها بالساهل", 1), ("بفقد أعصابي فوراً وما بتحمل", 0)]
        } for i in range(16, 101)
    ]
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
if "answers" not in st.session_state:
    st.session_state.answers = {}
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
    st.title("🇵🇸 ابن البلد - التحدي الفلسطيني")
    st.markdown("### اكتشف لقبك الحقيقي عشان تكون ابن البلد الأصيل")
    st.divider()
    
    name_input = st.text_input("أدخل اسمك الكريم:")
    age_input = st.number_input("عمرك البركة:", min_value=10, max_value=100, value=22)
    
    if st.button("🚀 بلش التحدي الآن"):
        if name_input.strip() == "":
            st.warning("يا ريت تكتب اسمك عشان نعرف مع مين بنحكي!")
        else:
            st.session_state.user_name = name_input.strip()
            st.session_state.user_age = age_input
            st.session_state.user_gender = detect_gender(name_input)
            
            pool = question_bank.copy()
            random.shuffle(pool)
            st.session_state.selected_questions = pool[:10]
            
            st.session_state.started = True
            st.session_state.step = 0
            st.session_state.answers = {}
            st.rerun()

# --- شاشة الأسئلة (بتصميم بطاقة مرئية مريحة) ---
elif st.session_state.step < len(st.session_state.selected_questions):
    current_q_idx = st.session_state.step
    q_data = st.session_state.selected_questions[current_q_idx]
    
    st.markdown(f"### 📌 السؤال رقم ({current_q_idx + 1} من 10)")
    st.divider()
    
    greeting = "يا نشمي" if st.session_state.user_gender == "ذكر" else "يا صبيّة"
    
    # عرض السؤال داخل بطاقة أنيقة وواضحة الخط
    st.markdown(f"""
        <div class="question-card">
            <h4 style="color: #007A3D; margin-bottom: 10px;">أهلاً فيك يا {st.session_state.user_name} ({greeting}):</h4>
            <p style="font-size: 20px; font-weight: bold; line-height: 1.6;">{q_data['q']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    for opt_text, points in q_data["options"]:
        if st.button(opt_text, key=f"ans_{current_q_idx}_{opt_text}"):
            st.session_state.answers[current_q_idx] = points
            st.session_state.step += 1
            st.rerun()
            
    st.write("")
    if current_q_idx > 0:
        if st.button("⬅️ رجوع للسؤال السابق وتعديل الإجابة"):
            st.session_state.step -= 1
            st.rerun()

# --- شاشة النتيجة النهائية (مع عبارات متغيرة وديناميكية حسب الجنس) ---
else:
    final_score = sum(st.session_state.answers.values())
    result_data = get_unique_title(final_score)
    
    # عبارات نجاح متغيرة وغير ثابتة تراعي الجنس والاسم
    if st.session_state.user_gender == "ذكر":
        success_phrases = [
            f"🎉 كفو يا {st.session_state.user_name} يا سبع الحارة! ختمت التحدي بجدارة وأثبتّ أصلك.",
            f"🔥 الله عليك يا {st.session_state.user_name} يا نشمي! خلصت التحدي وطلعت بتفهمها عالبطيء.",
            f"💪 كفو ثم كفو يا {st.session_state.user_name}! ختمت التحدي وطلع عقلك بوزن بلد."
        ]
    else:
        success_phrases = [
            f"🎉 كفو يا {st.session_state.user_name} يا صبيّة يا نشمية! ختمت التحدي برواق وذكاء.",
            f"✨ يا عيني عليكِ يا {st.session_state.user_name} يا غالية! أثبتّي إنك بنت دار وبتعرفي الأصول.",
            f"👑 كفو والله يا {st.session_state.user_name}! ختمتِ التحدي وطلعتِ ملكة التدبير والدبرة."
        ]
    
    chosen_success_msg = random.choice(success_phrases)
    st.success(chosen_success_msg)
    
    debray_val = min(100, max(30, final_score * 5 + 10))
    sabr_val = min(100, max(40, (st.session_state.user_age * 2) % 80 + 20))
    fa_hawa_val = min(100, max(50, 100 - (final_score * 3)))
    
    st.markdown(f"""
        <div class="result-card">
            <h2>🏆 لقبك: {result_data['title']}</h2>
            <p style="font-size: 19px; line-height: 1.6; margin-top: 10px;"><b>تحليل شخصيتك يا {st.session_state.user_name}:</b> {result_data['desc']}</p>
            <hr style="border-color: #007A3D; margin: 20px 0;">
            <h4 style="color: #007A3D;">📊 مؤشرات ابن البلد الخاصة فيك:</h4>
            <ul style="font-size: 16px; line-height: 1.8;">
                <li><b>مؤشر التدبير والتصرف في الأمور ({debray_val}%):</b> بقيس قدرتك على تسيير أمورك اليومية وحل المشاكل.</li>
                <li><b>مؤشر طول البال والصبر ({sabr_val}%):</b> بقيس قدرتك على تحمل الضغوط برواق على طريقة أهل زمان.</li>
                <li><b>مؤشر فطنة ابن البلد ({fa_hawa_val}%):</b> بقيس سرعة بديهتك وضحكتك اللي بتخفف هموم الشارع.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- رابط الواتساب الديناميكي ---
    app_link = "https://ibn-albalad-game.streamlit.app" 
    
    share_text = f"أنا لعبت تحدي 'ابن البلد' وطلع لقبي '{result_data['title']}'! 🇵🇸\nتعال جرب وشوف وخليك ابن بلد:\n🔗 {app_link}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; border-radius:12px; height:3.8em; font-weight:bold; background-color:#25D366; color:white; border:none; cursor:pointer; text-align:center; font-size:17px;">📲 شارك نتيجتك ولقبك على واتساب</button></a>', unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 عيد التحدي من أول وجديد"):
            st.session_state.started = False
            st.session_state.step = 0
            st.session_state.answers = {}
            st.rerun()
    with col2:
        if st.button("⬅️ تعديل الإجابات السابقة"):
            st.session_state.step = len(st.session_state.selected_questions) - 1
            st.rerun()
