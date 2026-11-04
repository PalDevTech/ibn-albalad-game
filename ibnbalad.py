import streamlit as st
import random
import urllib.parse
import re

# ==========================================
# 1. إعدادات الصفحة والتصميم المتجاوب (RTL)
# ==========================================
st.set_page_config(
    page_title="ابن/بنت البلد | التحدي الفلسطيني الأصيل",
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
    
    /* إخفاء أي نصوص توضيحية أو كتابة فاهية داخل حقول الإدخال بشكل جذري */
    input::placeholder, textarea::placeholder {
        color: transparent !important;
        opacity: 0 !important;
    }
    input::-webkit-input-placeholder {
        color: transparent !important;
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
        'تمارا', 'رغد', 'هديل', 'سجى', 'بتول', 'دعاء', 'آلاء', 'صفاء', 'اسراء', 'مي'
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
# 3. بنك الأسئلة الموسع والكامل (50 سؤالاً)
# ==========================================
raw_question_bank = [
    {
        "q": "المثل الشعبي يقول: 'اللي ما إلو خير في أهله...' كمل المثل باللهجة الفلسطينية الصحيحة؟",
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
        "q": "شو المقصود بكلمة 'الحوش' في البيوت الفلسطينية القديمة؟",
        "options": [("الساحة الداخلية المشتركة بين الدور", 2), ("المطبخ الصغير", 0), ("غرفة النوم", 1)],
    },
    {
        "q": "إذا شب بدو يخطب وبحكوا أهله 'أخذنا صهر نشمي'، شو بيقصدوا؟",
        "options": [("أنه زلمة قد الثقة وبعتمد عليه بكل شيء", 2), ("أنه غني كتير", 0), ("أنه بيعرف يطبخ", 1)],
    },
    {
        "q": "شو هي أكلة 'المنسف' بالتراث الفلسطيني والأردني بالمناسبات الكبيرة؟",
        "options": [("سيد الأكلات باللحم والجميد واللبن", 2), ("نوع من الحلوى", 0), ("أداة تنظيف", 1)],
    },
    {
        "q": "كيف بتتصرف لو واحد زعلك بس بطريقة غير مباشرة؟",
        "options": [("بواجهه بهدوء وبأخذ حقي بكلمتين وافيين", 2), ("بكتّم بقلبي وبحقد", 0), ("بشكي لكل الناس", 1)],
    },
    {
        "q": "شو معنى 'زلمة قد حاله' باللهجة الفلسطينية؟",
        "options": [("معتمد على حاله وقوي بقراراته", 2), ("شخص طويل القامة", 0), ("صاحب محل تجاري", 1)],
    },
    {
        "q": "إذا حدا حكى لك 'يا فتاح يا عليم'، شو الجواب العفوي المتداول بعدها؟",
        "options": [("يا رزاق يا كريم", 2), ("صباح الخير", 0), ("الحمد لله", 1)],
    },
    {
        "q": "شو معنى كلمة 'هِسّ' باللهجة الدارجة عنا؟",
        "options": [("طلب السكوت وعدم إصداره أي صوت", 2), ("نوع من الأكل", 0), ("اسم حي قديم", 1)],
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
        "q": "ما المقصود بتعبير 'فاتح عجهنم' بالحكي الدارج؟",
        "options": [("يفتح على نفسه باب مشاكل لا ينتهي", 2), ("يعمل في فرن مطعم", 0), ("يحب دراسة الفيزياء", 1)],
    },
    {
        "q": "ختاماً.. كيف بتوصف شخصيتك الحقيقية بكلمتين؟",
        "options": [("ابن أصول، أصيل، وبدبرها بأي ضائقة", 2), ("عابر سبيل ماشي بحالي", 1), ("مش مهتم بشيء", 0)]
    }
]

# ==========================================
# 4. الألقاب العشرة الفريدة والمفسرة (مراعية للجنس)
# ==========================================
def get_unique_title(score, gender):
    if gender == "ذكر":
        if score >= 18:
            return {"title": "عقيد البلد وسبعها العتيق 🎖️", "desc": "زلمة مواقف من طراز رفيع، بتعرف تدبر حالك بأضيق الأزمات، وكلمتك مسموعة وعقلك بوزن بلد."}
        elif score >= 14:
            return {"title": "حكيم الدار وعمودها الراسخ ☕", "desc": "عقلك متزن، حافظ الأصول والأمثال عن غيب، والكل يلجأ لك لما تحتار الأمور بوجوهها."}
        elif score >= 10:
            return {"title": "ابن البلد النشمي اللي ما بغلبوه ⚡", "desc": "واخد الحياة ببساطة وشهامة، قلبك أبيض، وبتعرف كيف تضحك على الهم بدل ما الهم يضحك عليك."}
        elif score >= 6:
            return {"title": "فيلسوف القهوة والشارع الهادئ 🫒", "desc": "تحليلك للأمور على مهله بس دقيق وصائب. بتوخذ وبتعطي بالحكي وعارف أصول اللعبة."}
        else:
            return {"title": "ملك البساطة وعفوية الشارع 🎈", "desc": "عايشها يوم بيوم وبكل بساطة وعفوية، والناس بتحب طيبة قلبك وصفاء نيتك."}
    else: # أنثى
        if score >= 18:
            return {"title": "عقيدة البلد ودرتها الأصيلة 🎖️", "desc": "بنت أصول من طراز رفيع، بتعرفي تدبري أمورك بأضيق الأزمات، وكلمتك مسموعة وعقلك بوزن بلد."}
        elif score >= 14:
            return {"title": "حكيمة الدار وعمودها الراسخ ☕", "desc": "عقلك متزن، حافظة الأصول والأمثال عن غيب، والكل يلجأ لك لما تحتار الأمور بوجوهها."}
        elif score >= 10:
            return {"title": "بنت البلد النشمية اللي ما بغلبوها ⚡", "desc": "واخدة الحياة ببساطة وشهامة، قلبك أبيض، وبتعرفي كيف تضحي وتضحكي على الهم برواق."}
        elif score >= 6:
            return {"title": "فيلسوفَة القهوة والشارع الهادئ 🫒", "desc": "تحليلك للأمور على مهله بس دقيق وصائب. بتوخذي وبتعطي بالحكي وعارفة أصول اللعبة."}
        else:
            return {"title": "ملكة البساطة وعفوية الدار 🎈", "desc": "عايشتها يوم بيوم وبكل بساطة وعفوية، والناس بتحب طيبة قلبك وصفاء نيتك."}

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
    # عنوان ديناميكي حسب الاختيار الافتراضي أو عند الدخول
    st.title("🇵🇸 ابن/بنت البلد - التحدي الفلسطيني")
    st.markdown("### اكتشف لقبك الحقيقي عشان تكون ابن أو بنت البلد الأصيل")
    st.divider()
    
    name_input = st.text_input("أدخل اسمك الكريم:", value="", placeholder="")
    age_input = st.number_input("عمرك البركة:", min_value=10, max_value=100, value=22)
    
    if st.button("🚀 بلش التحدي الآن"):
        clean_name = name_input.strip()
        if clean_name == "" or len(clean_name) < 2 or not re.search(r'[\u0600-\u06FFa-zA-Z]', clean_name):
            st.error("⚠️ يا ريت تكتب اسمك الكريم بشكل صحيح (حرفين على الأقل وبدون رموز عشوائية) لنقدر نبلش!")
        else:
            st.session_state.user_name = clean_name
            st.session_state.user_age = age_input
            st.session_state.user_gender = detect_gender(clean_name)
            
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

# --- شاشة الأسئلة ---
elif st.session_state.step < len(st.session_state.selected_questions):
    current_q_idx = st.session_state.step
    q_data = st.session_state.selected_questions[current_q_idx]
    
    st.markdown(f"### 📌 السؤال رقم ({current_q_idx + 1} من 10)")
    st.divider()
    
    if st.session_state.user_gender == "ذكر":
        greetings = ["يا نشمي", "يا غالي", "يا خيو", "يا زلمة", "يا سبع", "يا بطل البلد"]
    else:
        greetings = ["يا صبيّة", "يا نشمية", "يا غالية", "يا بنت الدار", "يا أم العز", "يا أميرة"]
    greeting = random.choice(greetings)
    
    st.markdown(f"""
        <div class="question-card">
            <h4 style="color: #007A3D; margin-bottom: 10px;">أهلاً فيك يا {st.session_state.user_name} ({greeting}):</h4>
            <p style="font-size: 18px; font-weight: bold; line-height: 1.6;">{q_data['q']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # حل مشكلة الأزرار الملونة باللون الأحمر مسبقاً: ربط الـ key برقم السؤال الحالي
    if not st.session_state.answered_current:
        for i, (opt_text, points) in enumerate(q_data["options"]):
            # مفتاح فريد لكل زر يعتمد على رقم السؤال الحالي لتجنب تداخل الذاكرة
            if st.button(opt_text, key=f"q_{current_q_idx}_opt_{i}"):
                st.session_state.answers[current_q_idx] = points
                st.session_state.answered_current = True
                
                if st.session_state.user_gender == "ذكر":
                    if points == 2:
                        st.session_state.last_is_correct = True
                        st.session_state.last_feedback = random.choice([
                            "🎯 وحش يا غالي! إجابة ذكية ومية المية بتعبر عن أصل أصيل.",
                            "🔥 كفو والله يا سبع! إجابتك بتدل إنك فاهمها عالبطيء.",
                            "⭐ عيني عليك باردة يا نشمي! جبتها على الجرح تماماً."
                        ])
                    elif points == 1:
                        st.session_state.last_is_correct = True
                        st.session_state.last_feedback = random.choice([
                            "⚡ إجابة مقبولة وبتمشي الحال يا خيو، بس فيها لفتة بدها شوية تركيز.",
                            "👍 ماشي حالك يا زلمة، قطعت نصف الطريق للصح."
                        ])
                    else:
                        st.session_state.last_is_correct = False
                        st.session_state.last_feedback = random.choice([
                            "❌ يا زلمة لا هيك خيبت ظني! هاي إجابة بعيدة كل البعد عن جو البلد.",
                            "⚠️ يا إبيييه يا غالي! وين رحت؟ هاي إجابة ما بتطلع من زلمة فاهم الأصول."
                        ])
                else:
                    if points == 2:
                        st.session_state.last_is_correct = True
                        st.session_state.last_feedback = random.choice([
                            "🎯 كفو يا صبيّة! إجابة ذكية ومية المية بتعبر عن أصل أصيل وبنت دار.",
                            "✨ يا عيني عليكِ يا غالية! أثبتّي إنك بتفهميها وهي طايرة.",
                            "👑 الله عليكِ يا نشمية! إجابة بوزن ذهب."
                        ])
                    elif points == 1:
                        st.session_state.last_is_correct = True
                        st.session_state.last_feedback = random.choice([
                            "⚡ إجابة مقبولة وبتمشي الحال يا أميرة، بس بدها لفتة ألطف شوي.",
                            "👍 ماشية أمورك تمام يا بنت الدار، قربتي كتير للصح."
                        ])
                    else:
                        st.session_state.last_is_correct = False
                        st.session_state.last_feedback = random.choice([
                            "❌ يا بنت الدار لا هيك خيبت ظني! هاي إجابة بعيدة كل البعد عن جو البلد.",
                            "⚠️ يا ستي لا هيك ما اتفقنا! هاي إجابة ما بتطلع من وحدة بتعرف أصول الدار."
                        ])

                st.rerun()
                
        st.write("")
        if current_q_idx > 0:
            if st.button("⬅️ رجوع للسؤال السابق وتعديل الإجابة", key=f"back_{current_q_idx}"):
                st.session_state.step -= 1
                st.rerun()
                
    else:
        # عرض التغذية الراجعة
        if st.session_state.last_is_correct:
            st.markdown(f'<div class="feedback-box-correct">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-box-wrong">{st.session_state.last_feedback}</div>', unsafe_allow_html=True)
            
        st.write("")
        
        # ميزة جديدة: السماح بتغيير الإجابة فوراً إذا كانت خطأ أو قبل الانتقال
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👉 المتابعة للسؤال التالي", key=f"next_{current_q_idx}"):
                st.session_state.answered_current = False
                st.session_state.step += 1
                st.rerun()
        with col2:
            if st.button("🔄 تغيير وإعادة اختيار الإجابة", key=f"change_{current_q_idx}"):
                st.session_state.answered_current = False
                st.rerun()

# --- شاشة النتيجة النهائية ---
else:
    final_score = sum(st.session_state.answers.values())
    result_data = get_unique_title(final_score, st.session_state.user_gender)
    
    if st.session_state.user_gender == "ذكر":
        success_phrases = [
            f"🎉 كفو يا {st.session_state.user_name} يا سبع البلد! ختمت التحدي بجدارة وأثبتّ أصلك.",
            f"🔥 الله عليك يا {st.session_state.user_name} يا نشمي! خلصت التحدي وطلعت بتفهمها عالبطيء.",
            f"💪 كفو ثم كفو يا {st.session_state.user_name}! ختمت التحدي وطلع عقلك بوزن بلد."
        ]
        game_title_share = "ابن البلد"
    else:
        success_phrases = [
            f"🎉 كفو يا {st.session_state.user_name} يا صبيّة يا نشمية! ختمت التحدي برواق وذكاء.",
            f"✨ يا عيني عليكِ يا {st.session_state.user_name} يا غالية! أثبتّي إنك بنت دار وبتعرفي الأصول.",
            f"👑 كفو والله يا {st.session_state.user_name}! ختمتِ التحدي وطلعتِ ملكة التدبير والدبرة."
        ]
        game_title_share = "بنت البلد"
    
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
            <h4 style="color: #007A3D;">📊 مؤشرات {game_title_share} الخاصة فيك:</h4>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li><b>مؤشر التدبير والتصرف في الأمور ({debray_val}%):</b> يقيس قدرتك على تسيير أمورك اليومية وحل المشاكل.</li>
                <li><b>مؤشر طول البال والصبر ({sabr_val}%):</b> يقيس قدرتك على تحمل الضغوط برواق على طريقة أهل زمان.</li>
                <li><b>مؤشر فطنة {game_title_share} ({fa_hawa_val}%):</b> يقيس سرعة بديهتك وضحكتك التي تخفف هموم الشارع.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    app_link = "https://ibn-albalad-game.streamlit.app" 
    
    share_text = f"أنا لعبت تحدي '{game_title_share}' وطلع لقبي '{result_data['title']}'! 🇵🇸\nتعال جرب وشوف وخليك قدها:\n🔗 {app_link}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; border-radius:12px; height:3.8em; font-weight:bold; background-color:#25D366; color:white; border:none; cursor:pointer; text-align:center; font-size:16px;">📲 شارك نتيجتك ولقبك على واتساب</button></a>', unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("🔄 عيد التحدي من أول وجديد", key="restart_game"):
        st.session_state.started = False
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.answered_current = False
        st.rerun()
