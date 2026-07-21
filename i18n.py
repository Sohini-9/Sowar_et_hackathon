"""
Localization data for the Citizen Health Risk Advisory console.

Every language has a FULL set of strings (title, severity messages, school
notice, SMS body, IVR script, and UI labels) plus its own AQI-category and
pollution-source translations. This is what makes language switching
consistent — nothing falls back to English mid-message — and lets the
advisory be genuinely personalized per city, since {source}, {hotspot},
{ward}, and {municipal} are filled in with that city's own data before the
template text is shown.
"""

LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Tamil (தமிழ்)": "ta",
    "Marathi (मराठी)": "mr",
    "Bengali (বাংলা)": "bn",
    "Telugu (తెలుగు)": "te",
    "Gujarati (ગુજરાતી)": "gu",
    "Malayalam (മലയാളം)": "ml",
    "Assamese (অসমীয়া)": "as",
}

# Default regional language per city, keyed to the LANGUAGES order above.
CITY_DEFAULT_LANG = {
    "Delhi": "Hindi (हिन्दी)", "Jaipur": "Hindi (हिन्दी)", "Lucknow": "Hindi (हिन्दी)",
    "Bhopal": "Hindi (हिन्दी)", "Patna": "Hindi (हिन्दी)", "Chandigarh": "Hindi (हिन्दी)",
    "Bengaluru": "Kannada (ಕನ್ನಡ)",
    "Chennai": "Tamil (தமிழ்)",
    "Mumbai": "Marathi (मराठी)", "Pune": "Marathi (मराठी)",
    "Kolkata": "Bengali (বাংলা)",
    "Hyderabad": "Telugu (తెలుగు)",
    "Ahmedabad": "Gujarati (ગુજરાતી)",
    "Kochi": "Malayalam (മലയാളം)",
    "Guwahati": "Assamese (অসমীয়া)",
}

AQI_CATEGORY_TRANSLATIONS = {
    "en": {"Good": "Good", "Satisfactory": "Satisfactory", "Moderate": "Moderate", "Poor": "Poor", "Very Poor": "Very Poor", "Severe": "Severe"},
    "hi": {"Good": "अच्छी", "Satisfactory": "संतोषजनक", "Moderate": "मध्यम", "Poor": "खराब", "Very Poor": "बहुत खराब", "Severe": "गंभीर"},
    "kn": {"Good": "ಉತ್ತಮ", "Satisfactory": "ತೃಪ್ತಿಕರ", "Moderate": "ಮಧ್ಯಮ", "Poor": "ಕಳಪೆ", "Very Poor": "ಅತಿ ಕಳಪೆ", "Severe": "ತೀವ್ರ"},
    "ta": {"Good": "நல்லது", "Satisfactory": "திருப்திகரமானது", "Moderate": "மிதமானது", "Poor": "மோசமானது", "Very Poor": "மிக மோசமானது", "Severe": "கடுமையானது"},
    "mr": {"Good": "चांगली", "Satisfactory": "समाधानकारक", "Moderate": "मध्यम", "Poor": "वाईट", "Very Poor": "अत्यंत वाईट", "Severe": "गंभीर"},
    "bn": {"Good": "ভালো", "Satisfactory": "সন্তোষজনক", "Moderate": "মাঝারি", "Poor": "খারাপ", "Very Poor": "অত্যন্ত খারাপ", "Severe": "গুরুতর"},
    "te": {"Good": "మంచిది", "Satisfactory": "సంతృప్తికరం", "Moderate": "మధ్యస్థం", "Poor": "చెడు", "Very Poor": "చాలా చెడు", "Severe": "తీవ్రమైన"},
    "gu": {"Good": "સારી", "Satisfactory": "સંતોષકારક", "Moderate": "મધ્યમ", "Poor": "ખરાબ", "Very Poor": "ખૂબ ખરાબ", "Severe": "ગંભીર"},
    "ml": {"Good": "നല്ലത്", "Satisfactory": "തൃപ്തികരം", "Moderate": "മിതമായത്", "Poor": "മോശം", "Very Poor": "വളരെ മോശം", "Severe": "ഗുരുതരം"},
    "as": {"Good": "ভাল", "Satisfactory": "সন্তোষজনক", "Moderate": "মধ্যম", "Poor": "বেয়া", "Very Poor": "অতি বেয়া", "Severe": "গুৰুতৰ"},
}

SOURCE_TRANSLATIONS = {
    "en": {"Traffic / Vehicular": "vehicular traffic", "Industrial Stack Emissions": "industrial stack emissions", "Construction Fugitive Dust": "construction dust", "Biomass & Waste Burning": "waste/biomass burning", "Resuspended Road Dust / Others": "road dust"},
    "hi": {"Traffic / Vehicular": "वाहन यातायात", "Industrial Stack Emissions": "औद्योगिक उत्सर्जन", "Construction Fugitive Dust": "निर्माण धूल", "Biomass & Waste Burning": "कचरा/बायोमास जलाना", "Resuspended Road Dust / Others": "सड़क की धूल"},
    "kn": {"Traffic / Vehicular": "ವಾಹನ ಸಂಚಾರ", "Industrial Stack Emissions": "ಕೈಗಾರಿಕಾ ಹೊರಸೂಸುವಿಕೆ", "Construction Fugitive Dust": "ನಿರ್ಮಾಣ ಧೂಳು", "Biomass & Waste Burning": "ತ್ಯಾಜ್ಯ ಸುಡುವಿಕೆ", "Resuspended Road Dust / Others": "ರಸ್ತೆ ಧೂಳು"},
    "ta": {"Traffic / Vehicular": "வாகன போக்குவரத்து", "Industrial Stack Emissions": "தொழிற்சாலை உமிழ்வு", "Construction Fugitive Dust": "கட்டுமான தூசி", "Biomass & Waste Burning": "கழிவு எரிப்பு", "Resuspended Road Dust / Others": "சாலை தூசி"},
    "mr": {"Traffic / Vehicular": "वाहतूक", "Industrial Stack Emissions": "औद्योगिक उत्सर्जन", "Construction Fugitive Dust": "बांधकाम धूळ", "Biomass & Waste Burning": "कचरा जाळणे", "Resuspended Road Dust / Others": "रस्त्यावरील धूळ"},
    "bn": {"Traffic / Vehicular": "যানবাহন চলাচল", "Industrial Stack Emissions": "শিল্প নির্গমন", "Construction Fugitive Dust": "নির্মাণ ধুলা", "Biomass & Waste Burning": "বর্জ্য পোড়ানো", "Resuspended Road Dust / Others": "রাস্তার ধুলা"},
    "te": {"Traffic / Vehicular": "వాహన రద్దీ", "Industrial Stack Emissions": "పారిశ్రామిక ఉద్గారాలు", "Construction Fugitive Dust": "నిర్మాణ దుమ్ము", "Biomass & Waste Burning": "వ్యర్థాల దహనం", "Resuspended Road Dust / Others": "రోడ్డు దుమ్ము"},
    "gu": {"Traffic / Vehicular": "વાહન ટ્રાફિક", "Industrial Stack Emissions": "ઔદ્યોગિક ઉત્સર્જન", "Construction Fugitive Dust": "બાંધકામ ધૂળ", "Biomass & Waste Burning": "કચરો બાળવો", "Resuspended Road Dust / Others": "રસ્તાની ધૂળ"},
    "ml": {"Traffic / Vehicular": "വാഹന ഗതാഗതം", "Industrial Stack Emissions": "വ്യാവസായിക ഉദ്‌വമനം", "Construction Fugitive Dust": "നിർമ്മാണ പൊടി", "Biomass & Waste Burning": "മാലിന്യം കത്തിക്കൽ", "Resuspended Road Dust / Others": "റോഡ് പൊടി"},
    "as": {"Traffic / Vehicular": "যান চলাচল", "Industrial Stack Emissions": "শিল্প নিৰ্গমন", "Construction Fugitive Dust": "নিৰ্মাণ ধূলি", "Biomass & Waste Burning": "আৱৰ্জনা দহন", "Resuspended Road Dust / Others": "ৰাস্তাৰ ধূলি"},
}

ADVISORIES = {
    "en": {
        "title": "Air Quality Health Warning",
        "severe": "Severe health hazard in {city}. Limit all outdoor activity immediately, especially near {hotspot} — the city's dominant {source} zone. Wear N95 respirators outdoors and keep schools closed, particularly in {ward}.",
        "moderate": "Moderate pollution in {city}, driven mainly by {source} around {hotspot}. Sensitive individuals (children, elderly, asthmatics) should reduce outdoor exertion, particularly near {ward}.",
        "good": "Air quality in {city} is healthy today. Suitable for outdoor sports and activities, including in {ward}.",
        "school_msg": "Attention schools in {city}: halt outdoor physical activity and field programs until the local AQI drops below 100, with extra caution near {hotspot}.",
        "sms": "AeroIntel Alert: AQI in {city} is {aqi} ({cat}). Main source: {source} near {hotspot}. Residents near {ward} should avoid outdoor exposure.",
        "ivr": "Broadcast script: Hello, this is the {municipal} municipal command. The current air quality index in {city} is {aqi}, classified as {cat}, driven mainly by {source} near {hotspot}. Residents near {ward} should follow health advisory recommendations.",
        "broadcast_header": "Public Announcement Broadcast Formats",
        "sms_label": "📱 Automated SMS Alert Text",
        "ivr_label": "📞 Automated IVR / Public Loudspeaker Voice Script",
        "school_header": "🏫 School & Youth Safety Protocol",
        "vulnerable_header": "Vulnerable Populations & Wards",
        "vulnerable_desc": "Exposure risk ranking based on population density, schools, and hospitals:",
        "zone_label": "Zone Type",
    },
    "hi": {
        "title": "वायु गुणवत्ता स्वास्थ्य चेतावनी",
        "severe": "{city} में गंभीर स्वास्थ्य खतरा है। खासकर {hotspot} के पास — जो शहर का प्रमुख {source} क्षेत्र है — सभी बाहरी गतिविधियां तुरंत सीमित करें। बाहर N95 मास्क पहनें और विशेष रूप से {ward} में स्कूल बंद रखें।",
        "moderate": "{city} में मध्यम प्रदूषण है, जो मुख्य रूप से {hotspot} के आसपास {source} के कारण है। संवेदनशील लोगों (बच्चे, बुजुर्ग, अस्थमा रोगी) को {ward} के पास बाहरी शारीरिक गतिविधि कम करनी चाहिए।",
        "good": "{city} में आज हवा स्वच्छ है। {ward} सहित बाहरी खेल और गतिविधियों के लिए उपयुक्त।",
        "school_msg": "{city} के स्कूलों के लिए सूचना: स्थानीय AQI 100 से नीचे आने तक बाहरी गतिविधियां और खेल कार्यक्रम रोकें, विशेष रूप से {hotspot} के पास सतर्क रहें।",
        "sms": "एरोइंटेल अलर्ट: {city} में AQI {aqi} ({cat}) है। मुख्य स्रोत: {hotspot} के पास {source}। {ward} के निवासी बाहर जाने से बचें।",
        "ivr": "प्रसारण स्क्रिप्ट: नमस्ते, यह {municipal} नगर कमांड है। {city} में वर्तमान वायु गुणवत्ता सूचकांक {aqi} है, जिसे {cat} श्रेणी में रखा गया है, जो मुख्यतः {hotspot} के पास {source} के कारण है। {ward} के निवासी स्वास्थ्य सलाह का पालन करें।",
        "broadcast_header": "सार्वजनिक प्रसारण प्रारूप",
        "sms_label": "📱 स्वचालित एसएमएस चेतावनी पाठ",
        "ivr_label": "📞 स्वचालित आईवीआर / सार्वजनिक लाउडस्पीकर स्क्रिप्ट",
        "school_header": "🏫 स्कूल एवं युवा सुरक्षा प्रोटोकॉल",
        "vulnerable_header": "संवेदनशील जनसंख्या एवं वार्ड",
        "vulnerable_desc": "जनसंख्या घनत्व, स्कूलों और अस्पतालों के आधार पर जोखिम रैंकिंग:",
        "zone_label": "क्षेत्र प्रकार",
    },
    "kn": {
        "title": "ವಾಯು ಗುಣಮಟ್ಟ ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆ",
        "severe": "{city} ನಲ್ಲಿ ತೀವ್ರ ಆರೋಗ್ಯ ಅಪಾಯವಿದೆ. ವಿಶೇಷವಾಗಿ ನಗರದ ಪ್ರಮುಖ {source} ವಲಯವಾದ {hotspot} ಬಳಿ ಎಲ್ಲಾ ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳನ್ನು ತಕ್ಷಣ ನಿಲ್ಲಿಸಿ. ಹೊರಗೆ N95 ಮಾಸ್ಕ್ ಧರಿಸಿ ಮತ್ತು {ward} ನಲ್ಲಿ ಶಾಲೆಗಳನ್ನು ಮುಚ್ಚಿ.",
        "moderate": "{city} ನಲ್ಲಿ ಮಧ್ಯಮ ಮಾಲಿನ್ಯವಿದೆ, ಇದು ಮುಖ್ಯವಾಗಿ {hotspot} ಸುತ್ತಮುತ್ತಲಿನ {source} ನಿಂದ ಉಂಟಾಗಿದೆ. ಸೂಕ್ಷ್ಮ ವ್ಯಕ್ತಿಗಳು (ಮಕ್ಕಳು, ವೃದ್ಧರು, ಅಸ್ತಮಾ ರೋಗಿಗಳು) {ward} ಬಳಿ ಹೊರಾಂಗಣ ಶ್ರಮವನ್ನು ಕಡಿಮೆ ಮಾಡಬೇಕು.",
        "good": "{city} ನಲ್ಲಿ ಇಂದು ಗಾಳಿಯ ಗುಣಮಟ್ಟ ಆರೋಗ್ಯಕರವಾಗಿದೆ. {ward} ಸೇರಿದಂತೆ ಹೊರಾಂಗಣ ಕ್ರೀಡೆ ಮತ್ತು ಚಟುವಟಿಕೆಗಳಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.",
        "school_msg": "{city} ಯ ಶಾಲೆಗಳ ಗಮನಕ್ಕೆ: ಸ್ಥಳೀಯ AQI 100 ಕ್ಕಿಂತ ಕಡಿಮೆಯಾಗುವವರೆಗೆ ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳನ್ನು ನಿಲ್ಲಿಸಿ, {hotspot} ಬಳಿ ಹೆಚ್ಚು ಜಾಗರೂಕರಾಗಿರಿ.",
        "sms": "ಏರೋಇಂಟೆಲ್ ಅಲರ್ಟ್: {city} ನಲ್ಲಿ AQI {aqi} ({cat}) ಆಗಿದೆ. ಮುಖ್ಯ ಮೂಲ: {hotspot} ಬಳಿ {source}. {ward} ಬಳಿಯ ನಿವಾಸಿಗಳು ಹೊರಾಂಗಣ ಪ್ರವೇಶ ತಪ್ಪಿಸಿ.",
        "ivr": "ಪ್ರಸಾರ ಸ್ಕ್ರಿಪ್ಟ್: ನಮಸ್ಕಾರ, ಇದು {municipal} ಪುರಸಭೆ ಕಮಾಂಡ್. {city} ನ ಪ್ರಸ್ತುತ AQI {aqi} ಆಗಿದ್ದು, ಇದನ್ನು {cat} ಎಂದು ವರ್ಗೀಕರಿಸಲಾಗಿದೆ, ಮುಖ್ಯವಾಗಿ {hotspot} ಬಳಿಯ {source} ನಿಂದ ಉಂಟಾಗಿದೆ. {ward} ಬಳಿಯ ನಿವಾಸಿಗಳು ಆರೋಗ್ಯ ಸಲಹೆಗಳನ್ನು ಅನುಸರಿಸಿ.",
        "broadcast_header": "ಸಾರ್ವಜನಿಕ ಪ್ರಕಟಣೆ ಪ್ರಸಾರ ಸ್ವರೂಪಗಳು",
        "sms_label": "📱 ಸ್ವಯಂಚಾಲಿತ SMS ಎಚ್ಚರಿಕೆ ಪಠ್ಯ",
        "ivr_label": "📞 ಸ್ವಯಂಚಾಲಿತ IVR / ಸಾರ್ವಜನಿಕ ಧ್ವನಿವರ್ಧಕ ಸ್ಕ್ರಿಪ್ಟ್",
        "school_header": "🏫 ಶಾಲಾ ಮತ್ತು ಯುವ ಸುರಕ್ಷತಾ ಪ್ರೋಟೋಕಾಲ್",
        "vulnerable_header": "ಸೂಕ್ಷ್ಮ ಜನಸಂಖ್ಯೆ ಮತ್ತು ವಾರ್ಡ್‌ಗಳು",
        "vulnerable_desc": "ಜನಸಂಖ್ಯಾ ಸಾಂದ್ರತೆ, ಶಾಲೆಗಳು ಮತ್ತು ಆಸ್ಪತ್ರೆಗಳ ಆಧಾರದ ಮೇಲೆ ಅಪಾಯದ ಶ್ರೇಣಿ:",
        "zone_label": "ವಲಯ ಪ್ರಕಾರ",
    },
    "ta": {
        "title": "காற்று தரம் சுகாதார எச்சரிக்கை",
        "severe": "{city} இல் கடுமையான சுகாதார ஆபத்து உள்ளது. நகரின் முக்கிய {source} பகுதியான {hotspot} அருகில் அனைத்து வெளிப்புற நடவடிக்கைகளையும் உடனடியாக நிறுத்தவும். வெளியே N95 முகக்கவசம் அணியவும், {ward} இல் பள்ளிகளை மூடவும்.",
        "moderate": "{city} இல் மிதமான மாசு உள்ளது, இது முக்கியமாக {hotspot} சுற்றியுள்ள {source} காரணமாகும். முதியவர்கள், குழந்தைகள், ஆஸ்துமா நோயாளிகள் {ward} அருகில் வெளிப்புற உடல் உழைப்பைக் குறைக்க வேண்டும்.",
        "good": "{city} இல் இன்று காற்று தரம் ஆரோக்கியமாக உள்ளது. {ward} உட்பட வெளிப்புற விளையாட்டு மற்றும் நடவடிக்கைகளுக்கு ஏற்றது.",
        "school_msg": "{city} பள்ளிகளுக்கு அறிவிப்பு: உள்ளூர் AQI 100 க்கு கீழ் குறையும் வரை வெளிப்புற நடவடிக்கைகளை நிறுத்தவும், {hotspot} அருகில் கூடுதல் எச்சரிக்கையாக இருக்கவும்.",
        "sms": "ஏரோஇண்டெல் எச்சரிக்கை: {city} இல் AQI {aqi} ({cat}). முதன்மை மூலம்: {hotspot} அருகில் {source}. {ward} அருகிலுள்ள குடிமக்கள் வெளியே செல்வதைத் தவிர்க்கவும்.",
        "ivr": "ஒலிபரப்பு ஸ்கிரிப்ட்: வணக்கம், இது {municipal} நகராண்மை கட்டுப்பாட்டு அறை. {city} இன் தற்போதைய காற்று தர குறியீடு {aqi}, இது {cat} என வகைப்படுத்தப்பட்டுள்ளது, முக்கியமாக {hotspot} அருகிலுள்ள {source} காரணமாகும். {ward} அருகிலுள்ளவர்கள் சுகாதார ஆலோசனைகளைப் பின்பற்றவும்.",
        "broadcast_header": "பொது அறிவிப்பு ஒலிபரப்பு வடிவங்கள்",
        "sms_label": "📱 தானியங்கி SMS எச்சரிக்கை உரை",
        "ivr_label": "📞 தானியங்கி IVR / பொது ஒலிபெருக்கி ஸ்கிரிப்ட்",
        "school_header": "🏫 பள்ளி மற்றும் இளைஞர் பாதுகாப்பு நெறிமுறை",
        "vulnerable_header": "பாதிக்கப்படக்கூடிய மக்கள் மற்றும் வார்டுகள்",
        "vulnerable_desc": "மக்கள் தொகை அடர்த்தி, பள்ளிகள் மற்றும் மருத்துவமனைகளின் அடிப்படையில் ஆபத்து தரவரிசை:",
        "zone_label": "மண்டல வகை",
    },
    "mr": {
        "title": "हवा गुणवत्ता आरोग्य इशारा",
        "severe": "{city} मध्ये गंभीर आरोग्य धोका आहे. विशेषतः शहरातील प्रमुख {source} क्षेत्र असलेल्या {hotspot} जवळ सर्व मैदानी हालचाली त्वरित थांबवा. बाहेर N95 मास्क वापरा आणि {ward} मध्ये शाळा बंद ठेवा.",
        "moderate": "{city} मध्ये मध्यम प्रदूषण आहे, जे मुख्यतः {hotspot} भोवतालच्या {source} मुळे आहे. संवेदनशील व्यक्तींनी (मुले, वृद्ध, दम्याचे रुग्ण) {ward} जवळ शारीरिक श्रम कमी करावेत.",
        "good": "{city} मध्ये आज हवा चांगली आहे. {ward} सह मैदानी खेळ आणि क्रियाकलापांसाठी योग्य.",
        "school_msg": "{city} मधील शाळांसाठी सूचना: स्थानिक AQI 100 च्या खाली येईपर्यंत मैदानी उपक्रम थांबवा, {hotspot} जवळ जास्त सावध राहा.",
        "sms": "एरोइंटेल अलर्ट: {city} मध्ये AQI {aqi} ({cat}) आहे. मुख्य स्रोत: {hotspot} जवळील {source}. {ward} जवळील रहिवाशांनी बाहेर जाणे टाळावे.",
        "ivr": "प्रसारण स्क्रिप्ट: नमस्कार, ही {municipal} नगर आदेश यंत्रणा आहे. {city} चा सध्याचा हवा गुणवत्ता निर्देशांक {aqi} असून तो {cat} या श्रेणीत आहे, जो प्रामुख्याने {hotspot} जवळील {source} मुळे आहे. {ward} जवळील रहिवाशांनी आरोग्य सल्ल्यांचे पालन करावे.",
        "broadcast_header": "सार्वजनिक घोषणा प्रसारण स्वरूप",
        "sms_label": "📱 स्वयंचलित एसएमएस इशारा मजकूर",
        "ivr_label": "📞 स्वयंचलित आयव्हीआर / सार्वजनिक ध्वनिक्षेपक स्क्रिप्ट",
        "school_header": "🏫 शाळा व युवा सुरक्षा प्रोटोकॉल",
        "vulnerable_header": "संवेदनशील लोकसंख्या व वॉर्ड",
        "vulnerable_desc": "लोकसंख्या घनता, शाळा आणि रुग्णालयांवर आधारित जोखीम श्रेणी:",
        "zone_label": "क्षेत्र प्रकार",
    },
    "bn": {
        "title": "বায়ু গুণমান স্বাস্থ্য সতর্কতা",
        "severe": "{city}-এ গুরুতর স্বাস্থ্য ঝুঁকি রয়েছে। বিশেষত শহরের প্রধান {source} এলাকা {hotspot}-এর কাছে সমস্ত বাইরের কার্যক্রম অবিলম্বে বন্ধ করুন। বাইরে N95 মাস্ক পরুন এবং {ward}-এ স্কুল বন্ধ রাখুন।",
        "moderate": "{city}-এ মাঝারি দূষণ রয়েছে, যা প্রধানত {hotspot}-এর আশেপাশে {source}-এর কারণে। সংবেদনশীল ব্যক্তিদের (শিশু, বয়স্ক, হাঁপানি রোগী) {ward}-এর কাছে বাইরের পরিশ্রম কমাতে হবে।",
        "good": "{city}-এ আজ বাতাস স্বাস্থ্যকর। {ward} সহ বাইরের খেলাধুলা ও কার্যক্রমের জন্য উপযুক্ত।",
        "school_msg": "{city}-এর স্কুলগুলির জন্য: স্থানীয় AQI ১০০-এর নিচে না নামা পর্যন্ত বাইরের কার্যক্রম বন্ধ রাখুন, {hotspot}-এর কাছে বিশেষ সতর্কতা অবলম্বন করুন।",
        "sms": "অ্যারোইনটেল সতর্কতা: {city}-এ AQI {aqi} ({cat})। প্রধান উৎস: {hotspot}-এর কাছে {source}। {ward}-এর বাসিন্দারা বাইরে যাওয়া এড়িয়ে চলুন।",
        "ivr": "সম্প্রচার স্ক্রিপ্ট: নমস্কার, এটি {municipal} পৌর কমান্ড। {city}-এর বর্তমান বায়ু গুণমান সূচক {aqi}, যা {cat} শ্রেণীভুক্ত, প্রধানত {hotspot}-এর কাছে {source}-এর কারণে। {ward}-এর বাসিন্দারা স্বাস্থ্য পরামর্শ অনুসরণ করুন।",
        "broadcast_header": "জনসাধারণের ঘোষণা সম্প্রচার ফরম্যাট",
        "sms_label": "📱 স্বয়ংক্রিয় এসএমএস সতর্কতা পাঠ্য",
        "ivr_label": "📞 স্বয়ংক্রিয় আইভিআর / জনসাধারণের লাউডস্পিকার স্ক্রিপ্ট",
        "school_header": "🏫 স্কুল ও যুব সুরক্ষা প্রোটোকল",
        "vulnerable_header": "সংবেদনশীল জনসংখ্যা ও ওয়ার্ড",
        "vulnerable_desc": "জনঘনত্ব, স্কুল ও হাসপাতালের ভিত্তিতে ঝুঁকির ক্রম:",
        "zone_label": "অঞ্চলের ধরন",
    },
    "te": {
        "title": "వాయు నాణ్యత ఆరోగ్య హెచ్చరిక",
        "severe": "{city}లో తీవ్రమైన ఆరోగ్య ప్రమాదం ఉంది. ముఖ్యంగా నగరంలోని ప్రధాన {source} ప్రాంతమైన {hotspot} సమీపంలో అన్ని బహిరంగ కార్యకలాపాలను వెంటనే నిలిపివేయండి. బయట N95 మాస్క్‌లు ధరించండి మరియు {ward}లో పాఠశాలలను మూసివేయండి.",
        "moderate": "{city}లో మధ్యస్థ కాలుష్యం ఉంది, ఇది ప్రధానంగా {hotspot} చుట్టుపక్కల {source} వల్ల కలుగుతోంది. సున్నితమైన వ్యక్తులు (పిల్లలు, వృద్ధులు, ఆస్తమా రోగులు) {ward} సమీపంలో బహిరంగ శారీరక శ్రమను తగ్గించుకోవాలి.",
        "good": "{city}లో ఈరోజు గాలి నాణ్యత ఆరోగ్యకరంగా ఉంది. {ward}తో సహా బహిరంగ క్రీడలు మరియు కార్యకలాపాలకు అనుకూలం.",
        "school_msg": "{city}లోని పాఠశాలలకు గమనిక: స్థానిక AQI 100 కంటే తక్కువగా వచ్చే వరకు బహిరంగ కార్యకలాపాలను నిలిపివేయండి, {hotspot} సమీపంలో అదనపు జాగ్రత్త వహించండి.",
        "sms": "ఏరోఇంటెల్ హెచ్చరిక: {city}లో AQI {aqi} ({cat}). ప్రధాన మూలం: {hotspot} సమీపంలో {source}. {ward} సమీపంలోని నివాసితులు బహిరంగ ప్రదేశాలను నివారించాలి.",
        "ivr": "ప్రసార స్క్రిప్ట్: నమస్కారం, ఇది {municipal} మున్సిపల్ కమాండ్. {city} యొక్క ప్రస్తుత వాయు నాణ్యత సూచిక {aqi}, ఇది {cat}గా వర్గీకరించబడింది, ప్రధానంగా {hotspot} సమీపంలోని {source} వల్ల కలుగుతోంది. {ward} సమీపంలోని నివాసితులు ఆరోగ్య సలహాలను పాటించాలి.",
        "broadcast_header": "ప్రజా ప్రకటన ప్రసార ఫార్మాట్‌లు",
        "sms_label": "📱 స్వయంచాలక SMS హెచ్చరిక వచనం",
        "ivr_label": "📞 స్వయంచాలక IVR / పబ్లిక్ లౌడ్‌స్పీకర్ స్క్రిప్ట్",
        "school_header": "🏫 పాఠశాల మరియు యువజన భద్రతా ప్రోటోకాల్",
        "vulnerable_header": "సున్నిత జనాభా మరియు వార్డులు",
        "vulnerable_desc": "జనసాంద్రత, పాఠశాలలు మరియు ఆసుపత్రుల ఆధారంగా ప్రమాద ర్యాంకింగ్:",
        "zone_label": "జోన్ రకం",
    },
    "gu": {
        "title": "હવા ગુણવત્તા આરોગ્ય ચેતવણી",
        "severe": "{city}માં ગંભીર આરોગ્ય જોખમ છે. ખાસ કરીને શહેરના મુખ્ય {source} વિસ્તાર {hotspot} નજીક તમામ બહારની પ્રવૃત્તિઓ તાત્કાલિક મર્યાદિત કરો. બહાર N95 માસ્ક પહેરો અને {ward}માં શાળાઓ બંધ રાખો.",
        "moderate": "{city}માં મધ્યમ પ્રદૂષણ છે, જે મુખ્યત્વે {hotspot}ની આસપાસ {source}ને કારણે છે. સંવેદનશીલ વ્યક્તિઓ (બાળકો, વૃદ્ધો, અસ્થમાના દર્દીઓ) {ward} નજીક બહારની શારીરિક પ્રવૃત્તિ ઘટાડે.",
        "good": "{city}માં આજે હવા સ્વસ્થ છે. {ward} સહિત બહારની રમતો અને પ્રવૃત્તિઓ માટે યોગ્ય.",
        "school_msg": "{city}ની શાળાઓ માટે સૂચના: સ્થાનિક AQI 100થી નીચે ન આવે ત્યાં સુધી બહારની પ્રવૃત્તિઓ બંધ રાખો, {hotspot} નજીક વધારાની સાવચેતી રાખો.",
        "sms": "એરોઇન્ટેલ ચેતવણી: {city}માં AQI {aqi} ({cat}) છે. મુખ્ય સ્ત્રોત: {hotspot} નજીક {source}. {ward} નજીકના રહેવાસીઓએ બહાર જવાનું ટાળવું.",
        "ivr": "પ્રસારણ સ્ક્રિપ્ટ: નમસ્તે, આ {municipal} નગર કમાન્ડ છે. {city}નો વર્તમાન હવા ગુણવત્તા સૂચકાંક {aqi} છે, જે {cat} તરીકે વર્ગીકૃત છે, મુખ્યત્વે {hotspot} નજીકના {source}ને કારણે. {ward} નજીકના રહેવાસીઓએ આરોગ્ય સલાહનું પાલન કરવું.",
        "broadcast_header": "જાહેર જાહેરાત પ્રસારણ ફોર્મેટ",
        "sms_label": "📱 સ્વયંસંચાલિત SMS ચેતવણી ટેક્સ્ટ",
        "ivr_label": "📞 સ્વયંસંચાલિત IVR / જાહેર લાઉડસ્પીકર સ્ક્રિપ્ટ",
        "school_header": "🏫 શાળા અને યુવા સુરક્ષા પ્રોટોકોલ",
        "vulnerable_header": "સંવેદનશીલ વસ્તી અને વોર્ડ",
        "vulnerable_desc": "વસ્તી ગીચતા, શાળાઓ અને હોસ્પિટલોના આધારે જોખમ ક્રમ:",
        "zone_label": "ઝોન પ્રકાર",
    },
    "ml": {
        "title": "വായു ഗുണനിലവാര ആരോഗ്യ മുന്നറിയിപ്പ്",
        "severe": "{city}-ൽ ഗുരുതരമായ ആരോഗ്യ അപകടം ഉണ്ട്. പ്രത്യേകിച്ച് നഗരത്തിലെ പ്രധാന {source} മേഖലയായ {hotspot}-ന് സമീപം എല്ലാ പുറംപ്രവർത്തനങ്ങളും ഉടൻ നിർത്തുക. പുറത്ത് N95 മാസ്ക് ധരിക്കുക, {ward}-ൽ സ്കൂളുകൾ അടച്ചിടുക.",
        "moderate": "{city}-ൽ മിതമായ മലിനീകരണം ഉണ്ട്, ഇത് പ്രധാനമായും {hotspot} ചുറ്റുമുള്ള {source} മൂലമാണ്. സെൻസിറ്റീവ് വ്യക്തികൾ (കുട്ടികൾ, പ്രായമായവർ, ആസ്ത്മ രോഗികൾ) {ward}-ന് സമീപം പുറംജോലി കുറയ്ക്കണം.",
        "good": "{city}-ൽ ഇന്ന് വായു ഗുണനിലവാരം ആരോഗ്യകരമാണ്. {ward} ഉൾപ്പെടെ പുറംകളികൾക്കും പ്രവർത്തനങ്ങൾക്കും അനുയോജ്യം.",
        "school_msg": "{city}-ലെ സ്കൂളുകൾക്ക് അറിയിപ്പ്: പ്രാദേശിക AQI 100-ൽ താഴെയാകുന്നത് വരെ പുറംപ്രവർത്തനങ്ങൾ നിർത്തുക, {hotspot}-ന് സമീപം കൂടുതൽ ജാഗ്രത പാലിക്കുക.",
        "sms": "എയ്‌റോഇന്റൽ മുന്നറിയിപ്പ്: {city}-ൽ AQI {aqi} ({cat}). പ്രധാന ഉറവിടം: {hotspot}-ന് സമീപം {source}. {ward}-ന് സമീപമുള്ള താമസക്കാർ പുറത്തിറങ്ങുന്നത് ഒഴിവാക്കുക.",
        "ivr": "പ്രക്ഷേപണ സ്ക്രിപ്റ്റ്: നമസ്കാരം, ഇത് {municipal} മുനിസിപ്പൽ കമാൻഡ് ആണ്. {city}-ലെ നിലവിലെ വായു ഗുണനിലവാര സൂചിക {aqi} ആണ്, ഇത് {cat} ആയി തരംതിരിച്ചിരിക്കുന്നു, പ്രധാനമായും {hotspot}-ന് സമീപമുള്ള {source} മൂലമാണ്. {ward}-ന് സമീപമുള്ളവർ ആരോഗ്യ നിർദ്ദേശങ്ങൾ പാലിക്കുക.",
        "broadcast_header": "പൊതു അറിയിപ്പ് പ്രക്ഷേപണ ഫോർമാറ്റുകൾ",
        "sms_label": "📱 ഓട്ടോമേറ്റഡ് SMS മുന്നറിയിപ്പ് ടെക്സ്റ്റ്",
        "ivr_label": "📞 ഓട്ടോമേറ്റഡ് IVR / പൊതു ലൗഡ്സ്പീക്കർ സ്ക്രിപ്റ്റ്",
        "school_header": "🏫 സ്കൂൾ, യുവജന സുരക്ഷാ പ്രോട്ടോക്കോൾ",
        "vulnerable_header": "സെൻസിറ്റീവ് ജനസംഖ്യയും വാർഡുകളും",
        "vulnerable_desc": "ജനസാന്ദ്രത, സ്കൂളുകൾ, ആശുപത്രികൾ എന്നിവയെ അടിസ്ഥാനമാക്കിയുള്ള അപകട റാങ്കിംഗ്:",
        "zone_label": "സോൺ തരം",
    },
    "as": {
        "title": "বায়ু গুণগত মান স্বাস্থ্য সতৰ্কবাণী",
        "severe": "{city}ত গুৰুতৰ স্বাস্থ্য বিপদ আছে। বিশেষকৈ চহৰখনৰ প্ৰধান {source} অঞ্চল {hotspot}ৰ ওচৰত সকলো বাহিৰৰ কাৰ্যকলাপ তৎক্ষণাৎ বন্ধ কৰক। বাহিৰত N95 মাস্ক পিন্ধক আৰু {ward}ত বিদ্যালয় বন্ধ ৰাখক।",
        "moderate": "{city}ত মধ্যমীয়া প্ৰদূষণ আছে, যি মূলতঃ {hotspot}ৰ চাৰিওফালে {source}ৰ বাবে। সংবেদনশীল ব্যক্তি (শিশু, বৃদ্ধ, হাঁপানী ৰোগী) {ward}ৰ ওচৰত বাহিৰৰ শাৰীৰিক পৰিশ্ৰম হ্ৰাস কৰিব লাগে।",
        "good": "{city}ত আজি বায়ু স্বাস্থ্যসন্মত। {ward} সহ বাহিৰৰ খেল-ধেমালি আৰু কাৰ্যকলাপৰ বাবে উপযুক্ত।",
        "school_msg": "{city}ৰ বিদ্যালয়সমূহলৈ জাননী: স্থানীয় AQI 100ৰ তলত নহালৈকে বাহিৰৰ কাৰ্যকলাপ বন্ধ ৰাখক, {hotspot}ৰ ওচৰত অতিৰিক্ত সতৰ্কতা অৱলম্বন কৰক।",
        "sms": "এৰোইণ্টেল সতৰ্কবাণী: {city}ত AQI {aqi} ({cat})। মুখ্য উৎস: {hotspot}ৰ ওচৰত {source}। {ward}ৰ ওচৰৰ বাসিন্দাসকলে বাহিৰলৈ ওলোৱাৰ পৰা বিৰত থাকক।",
        "ivr": "প্ৰচাৰ স্ক্ৰিপ্ট: নমস্কাৰ, এইটো {municipal} পৌৰ কমাণ্ড। {city}ৰ বৰ্তমানৰ বায়ু গুণগত মান সূচক {aqi}, যাক {cat} বুলি শ্ৰেণীবদ্ধ কৰা হৈছে, মূলতঃ {hotspot}ৰ ওচৰৰ {source}ৰ বাবে। {ward}ৰ ওচৰৰ বাসিন্দাসকলে স্বাস্থ্য পৰামৰ্শ মানি চলক।",
        "broadcast_header": "সাধাৰণ ঘোষণা প্ৰচাৰ বিন্যাস",
        "sms_label": "📱 স্বয়ংক্ৰিয় এছএমএছ সতৰ্কবাণী পাঠ",
        "ivr_label": "📞 স্বয়ংক্ৰিয় আইভিআৰ / সাধাৰণ লাউডস্পীকাৰ স্ক্ৰিপ্ট",
        "school_header": "🏫 বিদ্যালয় আৰু যুৱ সুৰক্ষা প্ৰটোকল",
        "vulnerable_header": "সংবেদনশীল জনসংখ্যা আৰু ৱাৰ্ড",
        "vulnerable_desc": "জনঘনত্ব, বিদ্যালয় আৰু চিকিৎসালয়ৰ ভিত্তিত বিপদ শ্ৰেণীবিভাজন:",
        "zone_label": "অঞ্চল প্ৰকাৰ",
    },
}


def build_advisory(lang_code, city, aqi, cpcb_category, dominant_source_en, hotspot, ward, municipal):
    """
    Fills the language template with this city's own live data — dominant
    pollution source, top hotspot, most vulnerable ward, local municipal body —
    so the resulting advisory is specific to the selected city rather than a
    generic message with only the city name swapped in.
    """
    ad_t = ADVISORIES.get(lang_code, ADVISORIES["en"])
    cat_translated = AQI_CATEGORY_TRANSLATIONS.get(lang_code, AQI_CATEGORY_TRANSLATIONS["en"]).get(cpcb_category, cpcb_category)
    source_translated = SOURCE_TRANSLATIONS.get(lang_code, SOURCE_TRANSLATIONS["en"]).get(dominant_source_en, dominant_source_en)

    fmt_kwargs = dict(city=city, aqi=aqi, cat=cat_translated, source=source_translated, hotspot=hotspot, ward=ward, municipal=municipal)

    return {
        "title": ad_t["title"],
        "severe": ad_t["severe"].format(**fmt_kwargs),
        "moderate": ad_t["moderate"].format(**fmt_kwargs),
        "good": ad_t["good"].format(**fmt_kwargs),
        "school_msg": ad_t["school_msg"].format(**fmt_kwargs),
        "sms": ad_t["sms"].format(**fmt_kwargs),
        "ivr": ad_t["ivr"].format(**fmt_kwargs),
        "broadcast_header": ad_t["broadcast_header"],
        "sms_label": ad_t["sms_label"],
        "ivr_label": ad_t["ivr_label"],
        "school_header": ad_t["school_header"],
        "vulnerable_header": ad_t["vulnerable_header"],
        "vulnerable_desc": ad_t["vulnerable_desc"],
        "zone_label": ad_t["zone_label"],
        "cat_translated": cat_translated,
    }
