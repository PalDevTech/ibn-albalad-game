import streamlit as st
import random
import urllib.parse

# ==========================================
# 1. إعدادات الصفحة والتصميم المتجاوب (RTL)
# ==========================================
st.set_page_config(
    page_title="ابن البلد | التحدي الفلسطيني الأصيل",
    page_icon="🇵🇸",
    layout="centered"
)

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
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #007A3D;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px;
        height: auto;
        min-height: 3.5em;
        padding: 12px;
        font-weight: bold;
        background-color: #007A3D;
        color: white;
        border: none;
        margin-bottom: 10px;
        font-size: 16px;
        white-space: normal !important;
        word-wrap: break-word !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #CE1126;
        color: white;
    }
    .feedback-box-correct {
        background-color: #1b4d3e;
        border: 2px solid #007A3D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #d4edda;
    }
    .feedback-box-wrong {
        background-color: #5c1d24;
        border: 2px solid #CE1126;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #f8d7da;
    }
    .result-card {
        background-color: #1e2126;
        padding: 22px;
        border-radius: 18px;
        border: 2px solid #007A3D;
        color: #fff;
        text-align: right;
        margin-top: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }
    @media (max-width: 768px) {
        h1 { font-size: 24px !important; }
        h3 { font-size: 18px !important; }
        .question-card, .result-card { padding: 15px; }
        div.stButton > button { font-size: 14px; min-height: 3.8em; }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. خوارزمية تحليل الجنس بدقة فائقة
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
# 3. بنك الأسئلة الموسع (مدقق لغويّاً وثقافياً)
# (الخيار الأول في كل قاموس هو الإجابة الصحيحة بوزن 2، ويتم خلطه عشوائياً برمجياً)
# ==========================================
raw_question_bank = [
    {
        "q": "المثل الشعبي بيقول: 'اللي ما إلو خير في أهله...' كمل المثل باللهجة الفلسطينية الصحيحة؟",
        "options": [("ما إلو خير في حاله أصلًا!", 2), ("ما بينوكل معه ملح بالمرة", 1), ("بيروح عالعرس بلا دعوة", 0)],
    },
    {
        "q": "لو نازل عالعصريّة ولقيت الشارع ضارب أزمة سير خانقة، شو أول ردة فعل إلك؟",
        "options": [("باخد دخلة فرعية جانبية حافظها شبر بشبر", 2), ("بفتح راديو وبتوكل على الله وبستنى الفرج برواق", 1), ("ببلش أزمر زي المجنون وبصيح على السيارات", 0)],
    },
    {
        "q": "أكلة شعبية فلسطينية أصيلة لا تُعوض بيوم الجمعة ولملمة العيلة، شو هي؟",
        "options": [("صينية مسخن بالزيت البلدى والبصل المحمر أو مقلوبة عأصولها", 2), ("مجدورة برغل مع بصل مقلي (مجدرة)", 1), ("إندومي وخلصنا عجلانين", 0)],
    },
    {
        "q": "لما تطير المصاري وتنشف جيبتك بنص الشهر، شو طريقتك بالتدبير؟",
        "options": [("بدبر حالي بذكاء وبمشي أموري للسهرة", 2), ("بوكل هوا وبقعد بالدار بستنى أول الشهر", 1), ("بصير أشكو للرايح والجاي وأنوح", 0)],
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
    {
        "q": "ما المعنى المجازي للمثل الشعبي: 'مثل اللي بيبيع مي بحارة السقايين'؟",
        "options": [("يتشاطر ويتذاكى على ناس أصلًا أصحاب المهنة أو الخبراء فيها", 2), ("شخص يبيع الماء للناس العطشى في الصيف", 1), ("تاجر صادق ومخلص بعمله التجاري", 0)],
    },
    {
        "q": "إذا حدا حكى لك 'يا فتاح يا عليم'، شو الجواب العفوي المتداول بعدها؟",
        "options": [("يا رزاق يا كريم", 2), ("صباح الخير", 0), ("الحمد لله", 1)],
    },
    {
        "q": "لما نقول عن شخص إنه 'بيوخذ الأمور برواق'، شو المقصود؟",
        "options": [("هادئ وعاقل ولا يتسرع بقراراته", 2), ("يمشي ببطء شديد", 0), ("كسول ولا يعمل", 1)],
    },
    {
        "q": "شو أصل كلمة 'الزعتر البري' في جبال فلسطين؟",
        "options": [("نبات جبلي أصيل يدخل في التراث والفطور", 2), ("زهرة مستوردة", 0), ("نوع شجر مثمر", 1)],
    },
    {
        "q": "كيف بتتصرف لو واجهك موقف صعب ومش عارف راسك من رجليك؟",
        "options": [("باخد نفس وبستشير حدا ثقة وبدبرها", 2), ("بترك الشغل وبهرب", 0), ("بعصب وبصيح", 1)],
    },
    {
        "q": "شو معنى تعبير 'قلبه أبيض' عنا بالحارة؟",
        "options": [("طيب القلب ولا يحمل غل أو حقد", 2), ("لونه أبيض", 0), ("مريض بالقلب", 1)],
    },
    {
        "q": "شو معنى كلمة 'طوشة' باللهجة الفلسطينية؟",
        "options": [("مشاجرة أو خناقة بين شخصين أو أكثر", 2), ("حفلة غنائية", 0), ("رحلة عائلية", 1)],
    },
    {
        "q": "إذا واحد حكى لك 'يا زلمة اعقل واثقل'، شو بينصحك؟",
        "options": [("بتكون هادي وبتتصرف بتعقل وحكمة", 2), ("بتنام بدري", 0), ("بتسافر برات البلد", 1)],
    },
    {
        "q": "شو معنى كلمة 'دبرني' باللهجة العامية؟",
        "options": [("ساعدني بحل المشكلة أو المأزق", 2), ("أعطيني مصاري فوراً", 0), ("خذني معك عالبازار", 1)],
    },
    {
        "q": "لما يقلك شخص 'أنا ابن البلد وباعرف خباياها'، شو بيقصد؟",
        "options": [("مطلع على تفاصيل وأصول المكان وعايشها", 2), ("ساكن بآخر الدنيا", 0), ("زائر جديد", 1)],
    },
    {
        "q": "شو معنى كلمة 'سلطنة' لما حدا يقعد يشرب قهوة؟",
        "options": [("حالة من المزاج العالي والروقان التام", 2), ("نعاس شديد", 0), ("تعب وإرهاق", 1)],
    },
    {
        "q": "إذا حدا حكى لك 'خَيّي' أو 'يا خيو'، قديش بتعني الكلمة بالمجتمع؟",
        "options": [("تدل على الأخوة والمحبة والشهامة العالية", 2), ("مجرد كلمة عادية", 0), ("استهزاء", 1)],
    },
    {
        "q": "شو معنى تعبير 'حارق دمه' على الفاضي؟",
        "options": [("منفعل ومقيد أعصابه لأشياء تافهة", 2), ("يعمل تحت الشمس", 0), ("طباخ شاطر", 1)],
    },
    {
        "q": "لما تحكي لأحد 'يا ريت نلتقي عالبساطة'، شو مقصودها؟",
        "options": [("جلسة هادئة وعفوية بدون تكلف وتصنع", 2), ("جلوس على الأرض", 0), ("موعد عمل رسمي", 1)],
    },
    {
        "q": "شو معنى 'عينه طويلة' باللهجة الدارجة؟",
        "options": [("شخص طماع وعينه عأغراض غيره", 2), ("نظره حاد وقوي", 0), ("يحب السفر", 1)],
    },
    {
        "q": "لما يقولوا عن شب 'الوجه الطليق'، شو بيقصدوا؟",
        "options": [("بشوش، رحب الصدر، وببتسم للكل", 2), ("دائم العبوس", 0), ("دائم السفر", 1)],
    },
    {
        "q": "شو معنى كلمة 'القطة بعبك' لما حدا يكون خايف؟",
        "options": [("مرعوب وقلقان من شيء راح ينكشف", 2), ("عنده قطة بالبيت", 0), ("مبسوط كتير", 1)],
    },
    {
        "q": "إذا حدا حكى لك 'أمورنا بالسليم'، شو بيكون الوضع؟",
        "options": [("كل شيء ماشي تمام وبدون مشاكل", 2), ("الوضع سيء", 0), ("في خطر", 1)],
    },
    {
        "q": "شو معنى كلمة 'عَطشان' مجازياً بالحكي الدارج؟",
        "options": [("عنده شغف واهتمام كبير بشيء معين", 2), ("بحاجة لمياه للشرب", 0), ("تعبان من الجري", 1)],
    },
    {
        "q": "لما يقولوا 'فلان لسانه طويل'، شو بيقصدوا؟",
        "options": [("بتمساح بالحكي الجارح أو بتطاول باللسان", 2), ("صوته عالي جداً", 0), ("بحب الأكل", 1)],
    },
    {
        "q": "شو معنى 'فلتان' باللهجة الشعبية؟",
        "options": [("شخص بلا مسؤولية وبدون التزام بالأصول", 2), ("منطلق بالحرية", 0), ("رياضي سريع", 1)],
    },
    {
        "q": "لما شخص يقلك 'على راسي والله'، شو بيعبر؟",
        "options": [("عن أقصى درجات الاحترام والتقدير والخدمة", 2), ("عن وجع راسه", 0), ("عن رفضه للطلب", 1)],
    },
    {
        "q": "شو معنى 'مخضرم' بالحارة؟",
        "options": [("شخص خبرة وعاش مواقف كثيرة بالحياة", 2), ("شخص كبير بالسن فقط", 0), ("تاجر قديم", 1)],
    },
    {
        "q": "إذا واحد حكى لك 'يا زلمة طنش تعش تنتعش'، شو بنصحك؟",
        "options": [("ما تدقق على كل شغلة صغيرة وريح راسك", 2), ("سافر واطلع رحلة", 0), ("نام ولا تقم", 1)],
    },
    {
        "q": "شو معنى كلمة 'عَزوة' بالمجتمع الفلسطيني؟",
        "options": [("السند والعيلة والأصحاب اللي بينشد فيهم الظهير", 2), ("نوع طعام شعبي", 0), ("وليمة كبيرة", 1)],
    },
    {
        "q": "لما شخص يقلك 'أنا ابن هالشوارع'، شو بيقصد؟",
        "options": [("أنه خبرة وعارف تفاصيل وأصول الحارة شبر بشبر", 2), ("لا بيتي له", 0), ("ضائع بالطريق", 1)],
    },
    {
        "q": "شو معنى تعبير 'حاطط عقله برأس غيره'؟",
        "options": [("بقلد الناس بدون شخصية مستقلة", 2), ("ذكي جداً", 0), ("بستشير أهله", 1)],
    },
    {
        "q": "ختاماً.. كيف بتوصف شخصيتك الحقيقية بكلمتين؟",
        "options": [("ابن أصول، أصيل، وبدبرها بأي ضائقة", 2), ("عابر سبيل ماشي بحالي", 1), ("مش مهتم بشيء", 0)]
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
if "answered_current" not in st.session_state:
    st.session_state.answered_current = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""
if "last_is_correct" not in st.session_state:
    st.session_state.last_is_correct = True

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
            
            # سحب 10 أسئلة فريدة وخلط خيارات كل سؤال عشوائياً
            processed_pool = []
            for item in raw_question_bank:
                q_text = item["q"]
                opts = list(item["options"])
                random.shuffle(opts)
                processed_pool.append({"q": q_text, "options": opts})
            
            random.shuffle(processed_pool)
            st.session_state.selected_questions = processed_pool[:10]
            
            st.session_state.started = True
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.answered_current = False
            st.rerun()

# --- شاشة الأسئلة مع التغذية الراجعة الفورية وزر الرجوع ---
elif st.session_state.step < len(st.session_state.selected_questions):
    current_q_idx = st.session_state.step
    q_data = st.session_state.selected_questions[current_q_idx]
    
    st.markdown(f"### 📌 السؤال رقم ({current_q_idx + 1} من 10)")
    st.divider()
    
    greeting = "يا نشمي" if st.session_state.user_gender == "ذكر" else "يا صبيّة"
    
    st.markdown(f"""
        <div class="question-card">
            <h4 style="color: #007A3D; margin-bottom: 10px;">أهلاً فيك يا {st.session_state.user_name} ({greeting}):</h4>
            <p style="font-size: 18px; font-weight: bold; line-height: 1.6;">{q_data['q']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # إذا لم يتم اختيار إجابة بعد في هذا السؤال
    if not st.session_state.answered_current:
        for opt_text, points in q_data["options"]:
            if st.button(opt_text, key=f"ans_{current_q_idx}_{opt_text}"):
                st.session_state.answers[current_q_idx] = points
                st.session_state.answered_current = True
                
                # تقييم فوري حسب النقاط
                if points == 2:
                    st.session_state.last_is_correct = True
                    st.session_state.last_feedback = "🎯 وحش! إجابة ذكية ومية المية بتعبر عن أصل أصيل."
                elif points == 1:
                    st.session_state.last_is_correct = True
                    st.session_state.last_feedback = "⚡ إجابة مقبولة وبتمشي الحال، بس فيها لفتة بدها شوية تركيز."
                else:
                    st.session_state.last_is_correct = False
                    st.session_state.last_feedback = "❌ يا زلمة لا هيك خيبت ظني! هاي إجابة بعيدة كل البعد عن جو الحارة."
                st.rerun()
                
        st.write("")
        if current_q_idx > 0:
            if st.button("⬅️ رجوع للسؤال السابق وتعديل الإجابة"):
                st.session_state.step -= 1
                st.rerun()
                
    # إذا تم اختيار الإجابة، نعرض التغذية الراجعة وزر المتابعة
    else:
        if st.session_state.last_is_correct:
            st.markdown(f'<div class="feedback-box-correct">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-box-wrong">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
            
        st.write("")
        if st.button("👉 اضغط هنا للمتابعة للسؤال التالي"):
            st.session_state.answered_current = False
            st.session_state.step += 1
            st.rerun()

# --- شاشة النتيجة النهائية (خالية تماماً من زر الرجوع) ---
else:
    final_score = sum(st.session_state.answers.values())
    result_data = get_unique_title(final_score)
    
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
            <p style="font-size: 17px; line-height: 1.6; margin-top: 10px;"><b>تحليل شخصيتك يا {st.session_state.user_name}:</b> {result_data['desc']}</p>
            <hr style="border-color: #007A3D; margin: 20px 0;">
            <h4 style="color: #007A3D;">📊 مؤشرات ابن البلد الخاصة فيك:</h4>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li><b>مؤشر التدبير والتصرف في الأمور ({debray_val}%):</b> يقيس قدرتك على تسيير أمورك اليومية وحل المشاكل.</li>
                <li><b>مؤشر طول البال والصبر ({sabr_val}%):</b> يقيس قدرتك على تحمل الضغوط برواق على طريقة أهل زمان.</li>
                <li><b>مؤشر فطنة ابن البلد ({fa_hawa_val}%):</b> يقيس سرعة بديهتك وضحكتك التي تخفف هموم الشارع.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    app_link = "https://ibn-albalad-game.streamlit.app" 
    
    share_text = f"أنا لعبت تحدي 'ابن البلد' وطلع لقبي '{result_data['title']}'! 🇵🇸\nتعال جرب وشوف وخليك ابن بلد:\n🔗 {app_link}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; border-radius:12px; height:3.8em; font-weight:bold; background-color:#25D366; color:white; border:none; cursor:pointer; text-align:center; font-size:16px;">📲 شارك نتيجتك ولقبك على واتساب</button></a>', unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("🔄 عيد التحدي من أول وجديد"):
        st.session_state.started = False
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.answered_current = False
        st.rerun()
