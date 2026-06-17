import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import datetime
import json
import os

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────

HEALTH_TIPS = [
    "💧 Drink at least 8 glasses of water daily to stay hydrated.",
    "🥦 Include leafy greens in at least one meal per day.",
    "🚶 Take a 10-minute walk after every meal to aid digestion.",
    "😴 Aim for 7–9 hours of quality sleep every night.",
    "🧘 Practice deep breathing for 5 minutes to reduce stress.",
    "🍎 Replace processed snacks with fruits or nuts.",
    "📵 Avoid screens at least 1 hour before bedtime.",
    "🪥 Brush and floss your teeth twice daily.",
    "🌞 Get 15–20 minutes of sunlight daily for Vitamin D.",
    "🧂 Reduce sodium intake to protect your heart.",
    "🥗 Eat a rainbow of fruits and vegetables for diverse nutrients.",
    "🏃 Aim for at least 150 minutes of moderate exercise per week.",
    "🎵 Listen to calming music to lower stress levels.",
    "🫀 Regular check-ups can detect health issues early.",
    "🍵 Replace one cup of coffee with green tea for antioxidants.",
]

EXERCISE_SUGGESTIONS = [
    "🚶 Walk briskly for 30 minutes — burns ~150 calories!",
    "🧘 Try 15 minutes of yoga — improves flexibility & calm.",
    "🤸 Do 3 sets of 10 push-ups to build upper-body strength.",
    "🦵 10 squats every hour keeps your legs and core strong.",
    "🚴 Cycling for 20 minutes is great cardio for all fitness levels.",
    "🏊 Swimming is a full-body, low-impact workout — try 20 laps!",
    "🧗 Climb stairs instead of using elevators whenever you can.",
    "🤾 Jump rope for 10 minutes — great cardio, no gym needed!",
    "🪂 Stretching for 10 minutes daily reduces injury risk.",
    "🏋️ Strength training 2–3x per week builds bone density.",
]

DIET_TIPS = [
    "🍓 Eat seasonal fruits — mangoes, bananas, papayas are great choices!",
    "🥑 Add avocado to your diet for healthy fats and potassium.",
    "🐟 Include fish like salmon or sardines for Omega-3 fatty acids.",
    "🥚 Eggs are a complete protein — great for breakfast.",
    "🌰 A handful of nuts daily provides healthy fats and minerals.",
    "🫘 Lentils and legumes are excellent plant-based protein sources.",
    "🥕 Carrots are rich in beta-carotene — great for eyes and skin.",
    "🫐 Blueberries are antioxidant-rich superfoods for brain health.",
    "🌿 Turmeric has powerful anti-inflammatory properties.",
    "🧄 Garlic boosts immunity and heart health — add it to your meals.",
]

SLEEP_TIPS = [
    "😴 Adults need 7–9 hours of sleep; teenagers need 8–10 hours.",
    "📵 Avoid phones and screens 1 hour before bed to improve sleep quality.",
    "🌡️ Keep your room cool (18–22°C) for the best sleep environment.",
    "☕ Avoid caffeine after 2 PM — it can disrupt your sleep cycle.",
    "📖 Reading a physical book before bed helps you wind down naturally.",
    "🧘 Progressive muscle relaxation can help you fall asleep faster.",
    "⏰ Maintain a consistent sleep schedule, even on weekends.",
    "🌑 Use blackout curtains — darkness signals your brain it's sleep time.",
    "🛁 A warm bath 1–2 hours before bed can improve sleep quality.",
    "🎶 White noise or soft nature sounds can mask disruptive noises.",
]

MOTIVATIONAL_QUOTES = [
    "💪 'Take care of your body. It's the only place you have to live.' – Jim Rohn",
    "🌟 'Health is not about the weight you lose, but about the life you gain.'",
    "🏆 'The groundwork of all happiness is health.' – Leigh Hunt",
    "🔥 'Your body can stand almost anything. It's your mind you have to convince.'",
    "🌈 'A healthy outside starts from the inside.' – Robert Urich",
    "⚡ 'To keep the body in good health is a duty.' – Buddha",
    "🎯 'Wellness is the complete integration of body, mind, and spirit.'",
    "✨ 'The first wealth is health.' – Ralph Waldo Emerson",
    "💡 'An apple a day keeps the doctor away — but so does daily exercise!'",
    "🚀 'Small steps every day lead to big health transformations over time.'",
]

DAILY_CHALLENGES = [
    "🎯 Walk 5,000 steps today — your heart will thank you!",
    "💧 Drink 10 glasses of water today. Track each one!",
    "🧘 Do 10 minutes of stretching or yoga this morning.",
    "🥗 Eat 5 servings of fruits and vegetables today.",
    "📵 No social media for 1 hour before bedtime tonight.",
    "😴 Be in bed by 10 PM tonight for a full 8 hours.",
    "🚶 Take a 15-minute walk during your lunch break.",
    "🍎 Replace all snacks today with fruits or nuts.",
    "🌞 Spend 20 minutes outdoors in the sunlight today.",
    "🤸 Do 20 squats every time you stand up from your chair!",
    "📖 Read for 30 minutes instead of watching TV tonight.",
    "🧂 Cook a low-sodium meal from scratch today.",
]

EMERGENCY_CONTACTS = """
🆘 EMERGENCY CONTACTS (India)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚑 Ambulance:           108
🚔 Police:              100
🚒 Fire:                101
🏥 Medical Helpline:    104
👩 Women Helpline:      1091
👧 Child Helpline:      1098
☎️  COVID Helpline:      1075
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Tiruppur District Hospital
   📞 0421-2200222

📍 KMCH (Coimbatore – nearby)
   📞 0422-4323800

📍 PSG Hospitals (Coimbatore)
   📞 0422-4345000
━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Save these numbers now!
"""

WATER_INFO = """
💧 DAILY WATER INTAKE GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━
👶 Children (4–8y):   5 glasses/day
🧒 Children (9–13y):  7–8 glasses/day
🧑 Teens (14–18y):    8–11 glasses/day
🧔 Adult Men:          10–13 glasses/day
👩 Adult Women:        8–10 glasses/day
🤰 Pregnant Women:     10 glasses/day
🍼 Breastfeeding:      13 glasses/day
🏋️ Athletes:           12–16 glasses/day
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Pro Tips:
  • Start your morning with 2 glasses
  • Drink 1 glass before every meal
  • Keep a water bottle visible always
  • Set hourly reminders on your phone
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ─────────────────────────────────────────────
#  DISEASE DATABASE
# ─────────────────────────────────────────────

DISEASE_DATA = {
    "diabetes": """
🩸 DIABETES — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Diabetes is a chronic condition where the body cannot properly
regulate blood sugar (glucose) levels.

📋 TYPES:
  • Type 1 — Body produces no insulin (autoimmune)
  • Type 2 — Body doesn't use insulin properly (most common)
  • Gestational — Occurs during pregnancy

⚠️ SYMPTOMS:
  • Frequent urination, excessive thirst
  • Unexplained weight loss or gain
  • Fatigue, blurred vision
  • Slow-healing wounds, tingling in hands/feet
  • Frequent infections, dry mouth

💊 TREATMENT & MANAGEMENT:
  • Monitor blood sugar regularly (target: 80–130 mg/dL fasting)
  • Prescribed medications: Metformin, Glipizide, or Insulin
  • Follow a low-GI diet: brown rice, vegetables, whole grains
  • Avoid: sugar, white rice, maida, fruit juices, sweets
  • Exercise 30 minutes daily — walking is excellent
  • Regular HbA1c tests every 3 months

🥗 DIET TIPS:
  • Eat small, frequent meals every 3–4 hours
  • Include: bitter gourd (karela), fenugreek, oats, barley
  • Avoid: sweets, sugary drinks, white bread, fried foods

🏥 SEE A DOCTOR IF: Blood sugar exceeds 250 mg/dL or you
   feel dizzy, confused, or unconscious.
""",

    "hypertension": """
❤️ HIGH BLOOD PRESSURE (HYPERTENSION) — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Blood pressure consistently above 140/90 mmHg.
Called the "silent killer" — often no obvious symptoms.

📊 BLOOD PRESSURE LEVELS:
  • Normal:      Below 120/80 mmHg  ✅
  • Elevated:    120–129 / below 80  🟡
  • Stage 1 HTN: 130–139 / 80–89    🟠
  • Stage 2 HTN: 140+ / 90+          🔴
  • Crisis:      Above 180/120       🆘 Emergency!

⚠️ SYMPTOMS (when present):
  • Severe headache (especially morning)
  • Dizziness, blurred vision
  • Chest pain, shortness of breath
  • Nosebleeds in severe cases

💊 TREATMENT & MANAGEMENT:
  • Medications: Amlodipine, Losartan, Enalapril (as prescribed)
  • Follow DASH diet: fruits, vegetables, low-fat dairy
  • Reduce salt — less than 5g/day (1 teaspoon)
  • Avoid smoking, alcohol, and excess caffeine
  • Exercise: 30 min walking, 5 days a week
  • Yoga and meditation to manage stress
  • Monitor BP daily at home

✅ FOODS TO EAT:
  Bananas, beetroot, berries, leafy greens, oats,
  garlic, flaxseeds, low-fat yogurt

❌ FOODS TO AVOID:
  Pickles, papad, chips, instant noodles, processed meats,
  excess tea/coffee, alcohol

🏥 EMERGENCY: If BP > 180/120 with symptoms — call 108!
""",

    "fever": """
🤒 FEVER, COLD & FLU — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS FEVER?
Normal temperature: 98.6°F (37°C)
Fever: Above 100.4°F (38°C) — body's immune response

📊 FEVER SEVERITY:
  • Low grade:  100.4–102°F — Rest and fluids
  • Moderate:   102–104°F   — Monitor closely
  • High:       Above 104°F — Seek medical attention

⚠️ SYMPTOMS:
  • Chills, sweating, headache, body aches
  • Runny nose, sore throat, cough (flu/cold)
  • Loss of appetite, fatigue, dehydration

💊 TREATMENT:
  • Complete bed rest
  • Fluids: water, ORS, coconut water, herbal tea
  • Paracetamol (Crocin/Dolo 650): 1 tablet every 6 hrs
  • Lukewarm sponge bath for high fever
  • Steam inhalation for nasal congestion

🌿 INDIAN HOME REMEDIES:
  • Tulsi + ginger + black pepper tea — 3x daily
  • Turmeric milk (haldi doodh) — anti-inflammatory
  • Mulethi (licorice root) tea for cough
  • Kadha (herbal decoction) — immunity booster
  • Gargle warm salt water for sore throat

🏥 SEE A DOCTOR IF:
  • Fever above 103°F lasting more than 2 days
  • Difficulty breathing, rash, severe headache
  • Infants under 3 months with any fever
  • Blood in phlegm or urine

⚠️ Do NOT give aspirin to children — risk of Reye's syndrome.
""",

    "dengue": """
🦟 DENGUE FEVER — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Mosquito-borne viral infection spread by Aedes aegypti
mosquito (bites during daytime).

⚠️ WARNING SIGNS:
  • Sudden high fever (102–104°F) lasting 2–7 days
  • Severe headache, pain behind eyes
  • Muscle and joint pain ("breakbone fever")
  • Skin rash appearing 3–4 days after fever onset
  • Nausea, vomiting, mild bleeding from nose/gums

🚨 GO TO HOSPITAL IMMEDIATELY IF:
  • Severe abdominal pain
  • Persistent vomiting (3+ times in 24 hours)
  • Bleeding gums, blood in urine/stool
  • Platelet count below 50,000
  • Cold/clammy skin, restlessness

💊 TREATMENT:
  • Complete bed rest
  • ORS, coconut water, papaya leaf juice
  • Paracetamol for fever — NO aspirin or ibuprofen!
  • Monitor platelet count daily
  • Platelet transfusion if count < 20,000

🌿 HOME SUPPORT:
  • Papaya leaf extract juice — increases platelet count
  • Giloy (Tinospora) kadha — boosts immunity
  • Pomegranate juice — rich in iron and antioxidants

🛡️ PREVENTION:
  • Mosquito repellents, full-sleeve clothing
  • Remove stagnant water around home
  • Use mosquito nets, especially for children

🏥 Tiruppur District Hospital: 0421-2200222
""",

    "asthma": """
🫁 ASTHMA — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Chronic condition where airways become inflamed and
narrowed, causing breathing difficulty.

🚫 TRIGGERS TO AVOID:
  • Dust mites, pollen, pet dander, mold
  • Smoke, pollution, strong perfumes, paint fumes
  • Cold air, stress, respiratory infections

⚠️ SYMPTOMS:
  • Shortness of breath, chest tightness
  • Wheezing (whistling sound when breathing)
  • Chronic cough — especially at night or early morning

🆘 DURING AN ATTACK:
  1. Sit upright — do NOT lie down
  2. Use rescue inhaler (Salbutamol/Ventolin): 2 puffs
  3. Stay calm — panic worsens it
  4. If no relief in 20 minutes — call 108

💊 DAILY MANAGEMENT:
  • Take controller medications as prescribed
  • Always carry your rescue inhaler
  • Know and avoid your triggers
  • Pranayama (breathing exercises) strengthens lungs

🌿 HELPFUL TIPS:
  • Keep home dust-free, use air purifiers
  • Change pillowcases weekly in hot water
  • Eat anti-inflammatory foods: ginger, turmeric, honey
  • Avoid cold drinks and ice cream

⚠️ Never ignore an asthma attack — can be life-threatening.
""",

    "thyroid": """
🦋 THYROID DISORDERS — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 HYPOTHYROIDISM (Underactive):
Symptoms: Weight gain, fatigue, feeling cold always,
dry skin, hair loss, depression, constipation,
slow heart rate, memory problems

📌 HYPERTHYROIDISM (Overactive):
Symptoms: Weight loss, rapid heartbeat, anxiety,
heat intolerance, sweating, tremors, bulging eyes

🔬 DIAGNOSIS:
  • TSH test — most important screening
  • Normal TSH range: 0.4–4.0 mIU/L
  • T3 and T4 blood tests
  • Thyroid ultrasound if nodule suspected

💊 TREATMENT:
  • Hypothyroidism: Levothyroxine (Thyronorm/Eltroxin)
    → Take on empty stomach, 30 min before breakfast
  • Hyperthyroidism: Methimazole or Carbimazole
  • Never skip thyroid medication — even 1 day matters!

🥗 DIET FOR HYPOTHYROIDISM:
  ✅ Eat: Selenium-rich foods, iodized salt, eggs, fish
  ❌ Avoid: Raw cabbage, broccoli in excess, soy
  ⚠️ Take meds 4 hours apart from calcium/iron supplements

🥗 DIET FOR HYPERTHYROIDISM:
  ✅ Eat: Cruciferous vegetables, calcium-rich foods
  ❌ Avoid: Excess iodine, seaweed, caffeine

📅 CHECK-UPS:
  • TSH test every 6 months once stable
  • Annual ultrasound if nodules detected
  • Close monitoring during pregnancy
""",

    "migraine": """
🧠 MIGRAINE & HEADACHE — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 MIGRAINE vs HEADACHE:
  • Headache: Dull, steady pain around the head
  • Migraine: Intense throbbing (usually one side) +
    nausea, light/sound sensitivity, sometimes aura

⚠️ COMMON TRIGGERS:
  • Stress, lack of sleep, skipping meals
  • Bright lights, loud sounds, strong smells
  • Hormonal changes, dehydration
  • Caffeine withdrawal, alcohol, processed foods

🆘 DURING A MIGRAINE:
  1. Go to a dark, quiet room immediately
  2. Apply cold/ice pack to forehead or back of neck
  3. Take prescribed medication early (Sumatriptan)
  4. OTC options: Saridon, Paracetamol + Domperidone
  5. Stay hydrated — sip cold water slowly

🌿 HELPFUL REMEDIES:
  • Peppermint oil on temples for tension headache
  • Ginger tea — reduces nausea and inflammation
  • Magnesium-rich foods: almonds, spinach, dark chocolate

🛡️ PREVENTION:
  • Consistent sleep schedule (same time daily)
  • Stay well-hydrated (8+ glasses/day)
  • Exercise regularly — reduces frequency by 40%
  • Track triggers in a headache diary
  • Yoga and meditation proven to reduce frequency

🏥 SEE A DOCTOR FOR:
  • First-ever sudden severe headache
  • Headache with fever and stiff neck
  • Headache after head injury
""",

    "arthritis": """
🦴 JOINT PAIN & ARTHRITIS — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 TYPES:
  • Osteoarthritis (OA): Wear-and-tear of cartilage.
    Common in knees, hips. Affects older adults.
  • Rheumatoid (RA): Autoimmune. Morning stiffness.
    Affects multiple joints symmetrically.
  • Gout: Uric acid crystals. Sudden severe pain in
    big toe or knee.

⚠️ SYMPTOMS:
  • Pain, swelling, and stiffness in joints
  • Reduced range of motion
  • Warmth and redness around the joint
  • Cracking sounds when moving

💊 OSTEOARTHRITIS TREATMENT:
  • Weight loss — every 1kg lost reduces knee load by 4kg
  • Low-impact exercise: swimming, cycling, walking
  • Paracetamol or Ibuprofen (short term)
  • Physiotherapy — critical for long-term improvement
  • Warm compress for chronic pain; cold for swollen joints

💊 GOUT MANAGEMENT:
  • Colchicine or NSAIDs for acute attack
  • Allopurinol for long-term uric acid control
  • Drink 3L water daily to flush uric acid
  • Eat cherries — proven to reduce gout attacks
  ❌ Avoid: Red meat, organ meats, shellfish, alcohol

🌿 GENERAL JOINT HEALTH:
  • Maintain healthy weight
  • Omega-3 fatty acids (fish oil) reduce inflammation
  • Calcium + Vitamin D for bone strength
  • Turmeric (curcumin) — natural anti-inflammatory

🔬 Diagnosis needs: X-ray, RA factor, uric acid blood tests
""",

    "stress": """
🧘 STRESS & ANXIETY — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 UNDERSTANDING:
Stress = normal response to challenges.
Anxiety = excessive worry interfering with daily life.

⚠️ STRESS SYMPTOMS:
  • Headaches, muscle tension, fatigue
  • Irritability, poor concentration
  • Sleep problems, appetite changes
  • Frequent illnesses (lowered immunity)

⚠️ ANXIETY SYMPTOMS:
  • Persistent worry, racing thoughts
  • Rapid heartbeat, sweating, trembling
  • Avoiding situations, panic attacks

🆘 IMMEDIATE RELIEF:
  • 4-7-8 Breathing: Inhale 4 sec, hold 7, exhale 8
  • Box Breathing: Inhale 4, hold 4, exhale 4, hold 4
  • Cold water on wrists and face — calming response
  • 5-4-3-2-1 grounding technique

💊 DAILY MANAGEMENT:
  • Exercise 30 min daily — most effective stress reducer
  • Limit caffeine and alcohol — worsen anxiety
  • Regular sleep schedule
  • Journaling — write worries down to externalize them
  • Talk to someone you trust

🧘 YOGA & MEDITATION (Proven Effective):
  • Pranayama breathing exercises
  • Shavasana for deep relaxation
  • 10 minutes meditation daily makes a real difference
  • Apps: Calm, Headspace, Insight Timer

🏥 WHEN TO SEEK HELP:
  • Anxiety interfering with work or relationships
  • Panic attacks
  • Persistent low mood or hopelessness
  ⚠️ Do NOT self-prescribe anti-anxiety medications.
""",

    "malaria": """
🦟 MALARIA — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Parasitic disease spread by female Anopheles mosquito
(bites at night). Caused by Plasmodium parasite.

⚠️ SYMPTOMS (appear 10–15 days after bite):
  • High fever with chills and sweating cycles
  • Headache, muscle aches, nausea, vomiting
  • Fatigue, anemia, jaundice (yellowing)
  • Cycles of fever every 48 or 72 hours

🔬 DIAGNOSIS:
  • Peripheral blood smear (gold standard)
  • Rapid Diagnostic Test (RDT)
  • Complete blood count (CBC)

💊 TREATMENT:
  • Chloroquine (for non-resistant strains)
  • Artemisinin-based Combination Therapy (ACT) — most effective
  • Severe malaria: IV Artesunate in hospital
  • Complete the full course — never stop early
  • Paracetamol for fever, ORS for hydration

🛡️ PREVENTION:
  • Sleep under insecticide-treated mosquito nets
  • Use DEET-based mosquito repellents
  • Wear long sleeves/pants in the evening
  • Remove stagnant water near home
  • Antimalarial tablets if traveling to high-risk areas

🏥 SEE A DOCTOR IMMEDIATELY: Malaria can become
   cerebral malaria — life-threatening without treatment.
""",

    "typhoid": """
🌡️ TYPHOID FEVER — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Bacterial infection (Salmonella typhi) spread through
contaminated food and water.

⚠️ SYMPTOMS (develop gradually over 1–3 weeks):
  • Prolonged high fever (rises each day, up to 104°F)
  • Headache, weakness, abdominal pain
  • Rash — small rose-colored spots on chest/abdomen
  • Constipation or diarrhea, loss of appetite
  • Enlarged spleen or liver

🔬 DIAGNOSIS:
  • Widal test (after 1 week of fever)
  • Blood culture (most accurate)
  • Complete blood count

💊 TREATMENT:
  • Antibiotics: Azithromycin, Ciprofloxacin, Ceftriaxone
  • Complete the FULL antibiotic course (10–14 days)
  • ORS for hydration, paracetamol for fever
  • Soft, easily digestible diet during illness

🥗 DIET DURING TYPHOID:
  ✅ Eat: Khichdi, boiled rice, bananas, boiled potatoes,
     curd, soup, porridge
  ❌ Avoid: Spicy food, raw vegetables, fried items,
     high-fiber foods, alcohol

🛡️ PREVENTION:
  • Drink boiled or filtered water only
  • Eat freshly cooked food; avoid street food
  • Wash hands before eating and after toilet
  • Typhoid vaccine (recommended every 3 years)
""",

    "tuberculosis": """
🫁 TUBERCULOSIS (TB) — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Bacterial infection (Mycobacterium tuberculosis) that
primarily affects the lungs. Spread through air when
an infected person coughs or sneezes.

⚠️ SYMPTOMS:
  • Persistent cough lasting 3+ weeks
  • Coughing up blood or mucus
  • Chest pain, difficulty breathing
  • Fatigue, weakness, weight loss
  • Night sweats, fever (usually evening)
  • Loss of appetite

🔬 DIAGNOSIS:
  • Sputum smear microscopy
  • GeneXpert test (most accurate and fast)
  • Chest X-ray
  • Tuberculin skin test (Mantoux)
  • IGRA blood test

💊 TREATMENT — DOTS Program (Free in India!):
  • First 2 months: 4 drugs (HRZE) — Intensive phase
  • Next 4 months: 2 drugs (HR) — Continuation phase
  • NEVER skip doses — leads to drug-resistant TB
  • Free treatment available at government hospitals
  • Nikshay Poshan Yojana: ₹500/month support

⚠️ IMPORTANT:
  • Wear mask to protect others
  • Ventilate your room well — open windows
  • Complete full 6-month course without fail
  • Drug-resistant TB (MDR-TB) requires 18-24 months
  • Close contacts should be tested too

🏥 Free TB treatment at all government hospitals in India
   National TB helpline: 1800-11-6666 (toll free)
""",

    "jaundice": """
💛 JAUNDICE — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Yellowing of skin and eyes due to excess bilirubin in
the blood. Usually indicates a liver, bile duct, or
blood disorder.

⚠️ SYMPTOMS:
  • Yellow skin, eyes (sclera), and nails
  • Dark yellow/brown urine
  • Pale or clay-colored stools
  • Fatigue, abdominal pain (upper right)
  • Itchy skin, nausea, vomiting, fever

📋 TYPES & CAUSES:
  • Hepatitis A, B, C (viral liver infection)
  • Gallstones blocking bile ducts
  • Alcoholic liver disease
  • Hemolytic anemia (red blood cells breaking down)
  • Newborn jaundice (very common, usually harmless)

🔬 DIAGNOSIS:
  • Liver function tests (LFT)
  • Bilirubin levels (direct and indirect)
  • Hepatitis B and C surface antigen tests
  • Ultrasound of liver and gallbladder

💊 TREATMENT:
  • Treat the underlying cause
  • Hepatitis A: Rest, fluids, no alcohol (self-limiting)
  • Hepatitis B: Antiviral medications
  • Gallstones: Laparoscopic cholecystectomy
  • Newborn: Phototherapy (blue light)

🥗 DIET DURING JAUNDICE:
  ✅ Eat: Sugarcane juice, radish, papaya, lemon water,
     coconut water, boiled vegetables, light khichdi
  ❌ Strictly AVOID: Alcohol, fatty/fried foods,
     red meat, raw food, spicy items

⚠️ Jaundice is a symptom — always see a doctor to find
   and treat the underlying cause.
""",

    "anemia": """
🩸 ANEMIA (Low Hemoglobin) — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Condition where blood lacks enough healthy red blood
cells or hemoglobin. Very common in India, especially
in women and children.

Normal Hemoglobin:
  • Men:      13.5–17.5 g/dL
  • Women:    12.0–15.5 g/dL
  • Children: 11.0–16.0 g/dL

⚠️ SYMPTOMS:
  • Extreme fatigue and weakness
  • Pale skin, pale inner eyelids and nails
  • Shortness of breath on mild exertion
  • Dizziness, headache, cold hands and feet
  • Brittle nails, hair loss
  • Craving for ice or clay (Pica)

📋 TYPES & CAUSES:
  • Iron deficiency anemia — most common
  • Vitamin B12 deficiency anemia
  • Folate (B9) deficiency anemia
  • Sickle cell anemia (genetic)
  • Anemia of chronic disease

💊 TREATMENT:
  • Iron supplements (Ferrous Sulphate/Ferrous Fumarate)
  • Take iron with Vitamin C for better absorption
  • B12 injections or tablets for B12 deficiency
  • Folic acid tablets for folate deficiency
  • Treat underlying disease (worms, malaria, etc.)

🥗 IRON-RICH FOODS TO EAT:
  • Spinach, methi, amaranth (rajgira)
  • Dates, raisins, pomegranate, beetroot
  • Jaggery (gud) — excellent iron source
  • Lentils, kidney beans, horse gram
  • Liver, eggs, fish, red meat

⚠️ Avoid tea/coffee with meals — reduces iron absorption
""",

    "cholesterol": """
💔 HIGH CHOLESTEROL — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Fatty substance in blood. High levels increase risk of
heart disease and stroke.

📊 CHOLESTEROL LEVELS:
  • Total Cholesterol:
    Desirable: Below 200 mg/dL
    Borderline: 200–239 mg/dL
    High: 240+ mg/dL
  • LDL (Bad): Should be below 100 mg/dL
  • HDL (Good): Should be above 40 (men) / 50 (women)
  • Triglycerides: Normal below 150 mg/dL

⚠️ SYMPTOMS:
  Usually no symptoms — discovered in blood tests.
  Severe cases: Chest pain (angina), xanthomas
  (fatty deposits on skin/tendons)

💊 TREATMENT:
  • Statins: Atorvastatin, Rosuvastatin (prescribed)
  • Ezetimibe for those who can't tolerate statins
  • Lifestyle changes are ESSENTIAL alongside medication

🥗 DIET CHANGES:
  ✅ Eat: Oats, flaxseeds, almonds, walnuts, olive oil,
     fatty fish (omega-3), fruits, vegetables, legumes
  ❌ Avoid: Ghee in excess, butter, full-fat dairy,
     red meat, fried foods, packaged/processed foods,
     coconut oil in excess

🏃 LIFESTYLE:
  • Exercise 30 min daily — raises good HDL cholesterol
  • Quit smoking — raises HDL, lowers LDL
  • Limit alcohol
  • Maintain healthy body weight
  • Reduce stress (raises cholesterol)

📅 Get cholesterol tested every year after age 40.
""",

    "pcod": """
🌸 PCOD / PCOS — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 WHAT IS IT?
Polycystic Ovary Disorder/Syndrome — hormonal
imbalance in women where ovaries produce excess
androgens (male hormones). Very common — affects
1 in 5 Indian women.

⚠️ SYMPTOMS:
  • Irregular or missed periods
  • Excess facial/body hair (hirsutism)
  • Acne on face, chest, back
  • Weight gain, especially around abdomen
  • Hair thinning or scalp hair loss
  • Difficulty getting pregnant (infertility)
  • Dark patches of skin (acanthosis nigricans)
  • Mood swings, anxiety, depression

🔬 DIAGNOSIS:
  • Ultrasound (multiple cysts on ovaries)
  • Blood tests: LH, FSH, testosterone, AMH levels
  • Fasting glucose and insulin tests

💊 TREATMENT (No complete cure — managed):
  • Hormonal birth control pills (regulate periods)
  • Metformin (for insulin resistance)
  • Anti-androgens (Spironolactone) for hair/acne
  • Clomiphene/Letrozole for fertility
  • Treat symptoms individually

🥗 DIET — CRUCIAL FOR PCOD:
  ✅ Eat: Low-GI foods, whole grains, leafy greens,
     high-fiber foods, anti-inflammatory foods,
     lean protein, healthy fats
  ❌ Avoid: Sugar, refined carbs (white rice, maida),
     dairy in excess, processed foods, alcohol

🏃 LIFESTYLE IS THE BEST MEDICINE:
  • Lose just 5–10% of body weight if overweight
  • Exercise 30–45 min daily (mix cardio + strength)
  • Manage stress — yoga, meditation help enormously
  • Sleep 7–9 hours consistently

⚠️ PCOD increases risk of: Diabetes, Heart disease,
   Endometrial cancer — regular monitoring is essential.
""",

    "skin": """
🧴 SKIN HEALTH & CONDITIONS — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PIMPLES / ACNE:
  • Wash face twice daily with mild cleanser
  • Don't touch or pop pimples
  • Use non-comedogenic moisturizer
  • Salicylic acid or benzoyl peroxide products
  • Severe acne: Prescription retinoids/antibiotics
  • Avoid oily foods and stress triggers

📌 ECZEMA / DERMATITIS:
  • Moisturize frequently with fragrance-free lotion
  • Avoid harsh soaps and hot showers
  • Hydrocortisone cream for flare-ups (short term)
  • Identify triggers: stress, sweat, certain fabrics

📌 RASH / URTICARIA (HIVES):
  • Antihistamines: Cetirizine, Loratadine for itching
  • Cool compress on affected area
  • Identify and avoid the trigger
  🆘 Rash with breathing difficulty = anaphylaxis
     Call 108 immediately!

📌 FUNGAL INFECTIONS (common in Tamil Nadu heat):
  • Clotrimazole/Miconazole cream 2x daily
  • Keep skin dry — change sweaty clothes promptly
  • Dust antifungal powder in skin folds
  • Complete the full course (2–4 weeks)

✅ GENERAL SKIN TIPS:
  • Always use SPF 30+ sunscreen outdoors
  • Stay hydrated — skin reflects water intake
  • Vitamin C-rich foods for skin health
  • Aloe vera gel — natural soothing agent
  • Change bedsheets weekly

⚠️ Any rapidly changing or darkening mole —
   see a dermatologist immediately.
""",

    "stomach": """
🫃 DIGESTIVE HEALTH — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ACIDITY / GASTRIC REFLUX:
  • Avoid spicy, oily, fried foods
  • Eat small frequent meals; don't skip meals
  • Don't lie down within 2 hours of eating
  • Antacids: Gelusil, ENO for quick relief
  • PPI for persistent cases: Pantoprazole, Omeprazole
  • Drink cold milk or eat banana for quick relief

📌 CONSTIPATION:
  • Increase dietary fiber: fruits, vegetables, grains
  • Drink minimum 10 glasses of water daily
  • Exercise daily — even walking helps bowel movement
  • Isabgol (psyllium husk) in warm water at bedtime
  • Prunes, papaya, kiwi — natural laxatives

📌 DIARRHEA / LOOSE MOTION:
  • ORS (Oral Rehydration Solution) — most important
  • BRAT diet: Banana, Rice, Applesauce, Toast
  • Avoid dairy, spicy, oily food until recovered
  • Curd with rice — natural probiotic
  🏥 See doctor if blood in stool or fever accompanies it

📌 BLOATING / GAS:
  • Avoid carbonated drinks, excessive beans, raw onion
  • Eat slowly and chew food properly
  • Hing (asafoetida) in warm water relieves gas
  • Jeera (cumin) water — excellent digestive aid
  • Probiotics: curd, buttermilk daily

📌 STOMACH ULCER (Peptic Ulcer):
  • H. pylori infection — needs antibiotic treatment
  • Avoid NSAIDs (Ibuprofen, Aspirin) without food
  • Proton pump inhibitors + antibiotics (triple therapy)
  • Eat soft foods; avoid alcohol and smoking

⚠️ Persistent stomach pain over 2 days — see a doctor.
""",

    "kidney": """
🫘 KIDNEY HEALTH — Complete Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 KIDNEY STONES:
Symptoms: Severe flank/back pain, pain during urination,
blood in urine, nausea, vomiting

Treatment:
  • Small stones (<5mm): Drink 3L water daily to pass
  • Alpha-blockers (Tamsulosin) help pass stones
  • Large stones: Lithotripsy or ureteroscopy
  • Pain: Diclofenac, Ketorolac as prescribed

Prevention of stones:
  • Drink 10–12 glasses water daily (most important!)
  • Reduce salt and animal protein
  • Limit high-oxalate foods: spinach, nuts, chocolate
  • Lemon juice in water — citrate prevents stone formation

📌 CHRONIC KIDNEY DISEASE (CKD):
Symptoms: Swelling in legs/face, decreased urine,
fatigue, nausea, itching, high BP

Management:
  • Control diabetes and blood pressure (root causes)
  • Low-protein diet as advised by doctor
  • Avoid NSAIDs — they damage kidneys
  • Limit potassium-rich foods if advised
  • Dialysis if kidney function falls below 10–15%
  • Kidney transplant is the cure

📌 URINARY TRACT INFECTION (UTI):
Symptoms: Burning urination, frequent urge, cloudy urine,
pelvic pain

Treatment:
  • Antibiotics: Nitrofurantoin, Trimethoprim (3–7 days)
  • Drink plenty of water (flush out bacteria)
  • Cranberry juice — mild prevention benefit
  • Women: Urinate after intercourse, wipe front to back

⚠️ Blood in urine or high fever with UTI — see a doctor
   immediately (could be kidney infection).
""",
}

STATS_FILE = "health_bot_stats.json"


# ─────────────────────────────────────────────
#  STATS MANAGER
# ─────────────────────────────────────────────

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {
        "user_name": "",
        "total_interactions": 0,
        "health_score": 0,
        "feature_counts": {},
        "sessions": 0,
    }

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


# ─────────────────────────────────────────────
#  BMI CALCULATOR
# ─────────────────────────────────────────────

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)
    if bmi < 18.5:
        category = "Underweight 🟡"
        advice = "Consider increasing calorie intake with nutritious foods."
    elif bmi < 25.0:
        category = "Normal weight 🟢"
        advice = "Great job! Maintain your healthy lifestyle."
    elif bmi < 30.0:
        category = "Overweight 🟠"
        advice = "Regular exercise and a balanced diet can help."
    else:
        category = "Obese 🔴"
        advice = "Please consult a doctor for a personalised health plan."
    return bmi, category, advice


# ─────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────

class LoginScreen:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.root.title("HealthBot — Login")
        self.root.geometry("480x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f1923")

        self._build()

    def _build(self):
        # Center frame
        outer = tk.Frame(self.root, bg="#0f1923")
        outer.pack(expand=True, fill="both")

        card = tk.Frame(outer, bg="#16222e", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=400)

        # Logo
        tk.Label(card, text="🌿", font=("Segoe UI", 40),
                 bg="#16222e", fg="#3ddc84").pack(pady=(36, 4))

        tk.Label(card, text="HealthBot",
                 font=("Segoe UI", 22, "bold"),
                 bg="#16222e", fg="#3ddc84").pack()

        tk.Label(card, text="Your Personal Wellness Companion",
                 font=("Segoe UI", 10),
                 bg="#16222e", fg="#78909c").pack(pady=(2, 24))

        tk.Label(card, text="Enter your name to get started:",
                 font=("Segoe UI", 10),
                 bg="#16222e", fg="#a0bcc8").pack(anchor="w", padx=36)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            card, textvariable=self.name_var,
            font=("Segoe UI", 13),
            bg="#1e2d3d", fg="#e8f5e9",
            insertbackground="#3ddc84",
            relief="flat", bd=0,
        )
        self.name_entry.pack(fill="x", padx=36, ipady=10, pady=(6, 4))
        self.name_entry.bind("<Return>", lambda e: self._login())
        self.name_entry.focus()

        self.err_var = tk.StringVar()
        tk.Label(card, textvariable=self.err_var,
                 font=("Segoe UI", 9),
                 bg="#16222e", fg="#ef9a9a").pack(pady=(2, 10))

        btn = tk.Button(
            card, text="Enter HealthBot →",
            font=("Segoe UI", 12, "bold"),
            bg="#3ddc84", fg="#0f1923",
            activebackground="#5dec9a",
            relief="flat", cursor="hand2",
            command=self._login
        )
        btn.pack(fill="x", padx=36, ipady=10)

        tk.Label(card,
                 text="Type your name and press Enter or click the button",
                 font=("Segoe UI", 8),
                 bg="#16222e", fg="#4a6070").pack(pady=(10, 0))

    def _login(self):
        name = self.name_var.get().strip()
        if not name:
            self.err_var.set("⚠️ Please enter your name to continue.")
            return
        if len(name) < 2:
            self.err_var.set("⚠️ Name must be at least 2 characters.")
            return
        name = name[0].upper() + name[1:]
        # Clear login and launch main app
        for widget in self.root.winfo_children():
            widget.destroy()
        self.on_login(name)


# ─────────────────────────────────────────────
#  MAIN BOT GUI
# ─────────────────────────────────────────────

class HealthBotApp:
    def __init__(self, root, user_name):
        self.root = root
        self.root.title("🌿 HealthBot — Your Personal Wellness Companion")
        self.root.geometry("920x700")
        self.root.minsize(760, 580)
        self.root.configure(bg="#0f1923")

        self.stats = load_stats()
        self.stats["user_name"] = user_name
        self.stats["sessions"] += 1
        save_stats(self.stats)

        self.bmi_step = 0
        self.bmi_weight = 0

        self._build_ui()
        self._greet()

    # ── UI BUILD ──────────────────────────────

    def _build_ui(self):
        self.C_BG       = "#0f1923"
        self.C_PANEL    = "#16222e"
        self.C_SIDEBAR  = "#111d28"
        self.C_ACCENT   = "#3ddc84"
        self.C_ACCENT2  = "#29b6f6"
        self.C_TEXT     = "#e8f5e9"
        self.C_MUTED    = "#78909c"
        self.C_ENTRY_BG = "#1e2d3d"

        # ── Header ────────────────────────────
        hdr = tk.Frame(self.root, bg="#0d2137", height=62)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🌿", font=("Segoe UI", 22),
                 bg="#0d2137", fg=self.C_ACCENT).pack(side="left", padx=(18, 4), pady=10)
        tk.Label(hdr, text="HealthBot",
                 font=("Segoe UI", 18, "bold"),
                 bg="#0d2137", fg=self.C_ACCENT).pack(side="left")
        tk.Label(hdr, text="Your Personal Wellness Companion",
                 font=("Segoe UI", 10),
                 bg="#0d2137", fg=self.C_MUTED).pack(side="left", padx=(8, 0))

        self.score_var = tk.StringVar()
        self._refresh_score_label()
        tk.Label(hdr, textvariable=self.score_var,
                 font=("Segoe UI", 10, "bold"),
                 bg="#0d2137", fg="#ffd54f").pack(side="right", padx=18)

        tk.Label(hdr,
                 text=f"👤 {self.stats['user_name']}",
                 font=("Segoe UI", 10),
                 bg="#0d2137", fg=self.C_ACCENT2).pack(side="right", padx=4)

        # ── Main area ─────────────────────────
        main = tk.Frame(self.root, bg=self.C_BG)
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg=self.C_SIDEBAR, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        def sb_section(text):
            tk.Label(sidebar, text=text,
                     font=("Segoe UI", 7, "bold"),
                     bg=self.C_SIDEBAR, fg=self.C_MUTED).pack(pady=(10, 2))

        def sb_btn(label, cmd):
            btn = tk.Button(
                sidebar, text=label, anchor="w",
                font=("Segoe UI", 9),
                bg=self.C_SIDEBAR, fg=self.C_TEXT,
                activebackground="#1e3040",
                activeforeground=self.C_ACCENT,
                relief="flat", cursor="hand2",
                padx=12, pady=4,
                command=lambda c=cmd: self._quick_send(c)
            )
            btn.pack(fill="x", padx=5, pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1e3040", fg=self.C_ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.C_SIDEBAR, fg=self.C_TEXT))

        sb_section("── WELLNESS ──")
        sb_btn("💡 Health Tip",        "health tip")
        sb_btn("💧 Water Intake",       "water")
        sb_btn("🏃 Exercise",           "exercise")
        sb_btn("😴 Sleep Advice",       "sleep")
        sb_btn("🥗 Diet Tips",          "diet")
        sb_btn("⚖️  BMI Calculator",    "bmi")
        sb_btn("🎯 Daily Challenge",    "challenge")
        sb_btn("💬 Motivation",         "motivation")

        sb_section("── DISEASES ──")
        sb_btn("🩸 Diabetes",           "diabetes")
        sb_btn("❤️  Hypertension",      "hypertension")
        sb_btn("🤒 Fever / Flu",        "fever")
        sb_btn("🦟 Dengue",             "dengue")
        sb_btn("🫁 Asthma",             "asthma")
        sb_btn("🦋 Thyroid",            "thyroid")
        sb_btn("🧠 Migraine",           "migraine")
        sb_btn("🦴 Joint / Arthritis",  "arthritis")
        sb_btn("🧘 Stress / Anxiety",   "stress")
        sb_btn("🦟 Malaria",            "malaria")
        sb_btn("🌡️  Typhoid",           "typhoid")
        sb_btn("🫁 Tuberculosis (TB)",  "tuberculosis")
        sb_btn("💛 Jaundice",           "jaundice")
        sb_btn("🩸 Anemia",             "anemia")
        sb_btn("💔 Cholesterol",        "cholesterol")
        sb_btn("🌸 PCOD / PCOS",        "pcod")
        sb_btn("🧴 Skin Problems",      "skin")
        sb_btn("🫃 Stomach / Gastric",  "stomach")
        sb_btn("🫘 Kidney Issues",      "kidney")

        sb_section("── OTHER ──")
        sb_btn("🆘 Emergency Contacts", "emergency")
        sb_btn("📊 My Stats",           "stats")

        tk.Frame(sidebar, bg="#1e3040", height=1).pack(fill="x", padx=8, pady=6)

        tk.Button(
            sidebar, text="💾 Save Chat",
            font=("Segoe UI", 9), anchor="w",
            bg="#1a3a2a", fg=self.C_ACCENT,
            activebackground="#1e4a30",
            relief="flat", cursor="hand2",
            padx=12, pady=3,
            command=self._save_history
        ).pack(fill="x", padx=5, pady=1)

        tk.Button(
            sidebar, text="🗑️  Clear Chat",
            font=("Segoe UI", 9), anchor="w",
            bg="#3a1a1a", fg="#ef9a9a",
            activebackground="#4a2020",
            relief="flat", cursor="hand2",
            padx=12, pady=3,
            command=self._clear_chat
        ).pack(fill="x", padx=5, pady=1)

        tk.Label(sidebar,
                 text=f"Session #{self.stats['sessions']}",
                 font=("Segoe UI", 8),
                 bg=self.C_SIDEBAR, fg=self.C_MUTED).pack(side="bottom", pady=6)

        # ── Chat area ─────────────────────────
        chat_frame = tk.Frame(main, bg=self.C_BG)
        chat_frame.pack(side="left", fill="both", expand=True)

        self.chat = scrolledtext.ScrolledText(
            chat_frame, wrap="word",
            font=("Segoe UI", 10),
            bg=self.C_PANEL, fg=self.C_TEXT,
            insertbackground=self.C_ACCENT,
            relief="flat", padx=14, pady=14,
            state="disabled",
            selectbackground="#1e3d5c"
        )
        self.chat.pack(fill="both", expand=True, padx=6, pady=(6, 0))

        self.chat.tag_config("bot",        foreground="#a5d6a7", font=("Segoe UI", 10))
        self.chat.tag_config("user",       foreground="#81d4fa", font=("Segoe UI", 10))
        self.chat.tag_config("label_bot",  foreground=self.C_ACCENT,  font=("Segoe UI", 8, "bold"))
        self.chat.tag_config("label_user", foreground=self.C_ACCENT2, font=("Segoe UI", 8, "bold"))
        self.chat.tag_config("divider",    foreground="#1e3040")

        # Input bar
        input_bar = tk.Frame(chat_frame, bg="#0d2137", pady=10)
        input_bar.pack(fill="x", padx=6, pady=6)

        self.entry = tk.Entry(
            input_bar,
            font=("Segoe UI", 12),
            bg=self.C_ENTRY_BG, fg=self.C_TEXT,
            insertbackground=self.C_ACCENT,
            relief="flat", bd=0
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(10, 6))
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.focus()

        tk.Button(
            input_bar, text="Send ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.C_ACCENT, fg="#0f1923",
            activebackground="#5dec9a",
            relief="flat", cursor="hand2",
            padx=16, pady=6,
            command=self._send
        ).pack(side="right", padx=(0, 10))

        tk.Label(chat_frame,
                 text='Type naturally: "I have fever", "about diabetes", "bmi"  •  or click sidebar',
                 font=("Segoe UI", 8),
                 bg=self.C_BG, fg=self.C_MUTED).pack(pady=(0, 4))

    # ── HELPERS ──────────────────────────────

    def _refresh_score_label(self):
        self.score_var.set(f"⭐ Health Score: {self.stats['health_score']}")

    def _append(self, text, tag="bot", sender="HealthBot"):
        self.chat.config(state="normal")
        ts = datetime.datetime.now().strftime("%H:%M")
        label_tag = "label_bot" if sender == "HealthBot" else "label_user"
        self.chat.insert("end", f"\n{sender}  [{ts}]\n", label_tag)
        self.chat.insert("end", text + "\n", tag)
        self.chat.insert("end", "─" * 58 + "\n", "divider")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _quick_send(self, text):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)
        self._send()

    def _send(self):
        raw = self.entry.get().strip()
        if not raw:
            return
        self.entry.delete(0, "end")
        self._append(raw, tag="user", sender=f"You ({self.stats['user_name']})")
        self.stats["total_interactions"] += 1
        response = self._process(raw.lower())
        self._append(response)
        save_stats(self.stats)
        self._refresh_score_label()

    # ── PROCESS ───────────────────────────────

    def _process(self, msg):
        name = self.stats["user_name"]
        fc   = self.stats["feature_counts"]

        def track(feat, pts=5):
            fc[feat] = fc.get(feat, 0) + 1
            self.stats["health_score"] += pts

        def has(*words):
            return any(w in msg for w in words)

        # ── BMI multi-step ────────────────────
        if self.bmi_step == 1:
            try:
                w = float(msg.replace("kg", "").strip())
                if w < 20 or w > 300:
                    raise ValueError
                self.bmi_weight = w
                self.bmi_step = 2
                return "Got it! Now enter your height in centimetres (e.g. 165):"
            except ValueError:
                self.bmi_step = 0
                return "⚠️ Please enter a valid weight in kg (e.g. 65)."

        if self.bmi_step == 2:
            try:
                h = float(msg.replace("cm", "").strip())
                if h < 100 or h > 250:
                    raise ValueError
                bmi, cat, advice = calculate_bmi(self.bmi_weight, h)
                self.bmi_step = 0
                track("bmi", 10)
                return (
                    f"📊 BMI RESULT for {name}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Weight : {self.bmi_weight} kg\n"
                    f"  Height : {h} cm\n"
                    f"  BMI    : {bmi}\n"
                    f"  Status : {cat}\n\n"
                    f"💡 {advice}"
                )
            except ValueError:
                self.bmi_step = 0
                return "⚠️ Please enter a valid height in cm (e.g. 165)."

        # ── Greetings ─────────────────────────
        if has("hello", "hi", "hey", "namaste", "vanakkam"):
            track("greeting", 2)
            hour = datetime.datetime.now().hour
            tod = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
            return (
                f"{tod}, {name}! 🌿\n"
                f"I'm HealthBot — your personal wellness companion.\n\n"
                f"I can help you with:\n"
                f"  • Disease info: diabetes, fever, dengue, hypertension...\n"
                f"  • Daily wellness: tips, diet, exercise, sleep\n"
                f"  • BMI calculator, daily challenges\n"
                f"  • Emergency contacts\n\n"
                f"Type naturally or click the sidebar menu!\n"
                f"💧 Did you drink enough water today?"
            )

        if has("how are you", "how r u", "sup"):
            track("greeting", 2)
            return (
                f"Running at 100% wellness, {name}! 💪\n"
                f"More importantly — how are YOU feeling today?\n"
                f"Tell me your symptoms or type 'help' for the full menu!"
            )

        if has("bye", "goodbye", "exit", "quit", "see you"):
            track("bye", 2)
            return (
                f"Take care, {name}! 🌿\n"
                f"Remember:\n"
                f"  • Drink enough water 💧\n"
                f"  • Move your body 🏃\n"
                f"  • Sleep well 😴\n\n"
                f"See you next time! Your health score: ⭐{self.stats['health_score']}"
            )

        if has("thank", "thanks", "thx", "ty"):
            track("thanks", 2)
            return f"You're welcome, {name}! 😊 Stay healthy and feel free to ask anything anytime!"

        # ── Wellness Features ─────────────────
        if has("health tip", "tip", "tips", "wellness"):
            track("health_tip")
            return f"💡 HEALTH TIP\n━━━━━━━━━━━━\n{random.choice(HEALTH_TIPS)}"

        if has("water", "hydration", "drink"):
            track("water")
            return WATER_INFO

        if has("exercise", "workout", "fitness", "gym", "walk", "physical"):
            track("exercise")
            return (
                f"🏃 EXERCISE SUGGESTION\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"{random.choice(EXERCISE_SUGGESTIONS)}\n\n"
                f"Consistency is key — even 15 minutes daily makes a difference!"
            )

        if has("sleep", "rest", "insomnia", "can't sleep", "sleeping"):
            track("sleep")
            return f"😴 SLEEP GUIDANCE\n━━━━━━━━━━━━━━━━\n{random.choice(SLEEP_TIPS)}"

        if has("diet", "food", "eat", "nutrition", "meal"):
            track("diet")
            return f"🥗 DIET SUGGESTION\n━━━━━━━━━━━━━━━━━\n{random.choice(DIET_TIPS)}"

        if has("bmi", "body mass", "calculate weight"):
            self.bmi_step = 1
            track("bmi", 0)
            return (
                f"⚖️ BMI CALCULATOR\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Let's calculate your BMI, {name}!\n\n"
                f"First, enter your weight in kilograms (e.g. 65):"
            )

        if has("challenge", "today", "goal"):
            track("challenge", 10)
            ch = random.choice(DAILY_CHALLENGES)
            return (
                f"🎯 TODAY'S HEALTH CHALLENGE\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{ch}\n\n"
                f"+10 health points for accepting the challenge! 🌟"
            )

        if has("motivation", "motivat", "inspire", "quote"):
            track("motivation", 3)
            return f"💬 MOTIVATIONAL MESSAGE\n━━━━━━━━━━━━━━━━━━━━━━━\n{random.choice(MOTIVATIONAL_QUOTES)}"

        if has("emergency", "contact", "hospital", "ambulance", "sos"):
            track("emergency", 0)
            return EMERGENCY_CONTACTS

        if has("stat", "score", "progress", "points"):
            track("stats", 0)
            top = sorted(fc.items(), key=lambda x: x[1], reverse=True)
            top_str = "\n".join([f"  • {k}: {v}x" for k, v in top[:5]]) or "  None yet!"
            return (
                f"📊 YOUR HEALTH STATS, {name}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"  ⭐ Health Score    : {self.stats['health_score']}\n"
                f"  💬 Total Interactions: {self.stats['total_interactions']}\n"
                f"  📅 Sessions        : {self.stats['sessions']}\n\n"
                f"🏆 TOP FEATURES USED:\n{top_str}"
            )

        if has("help", "menu", "options", "what can"):
            return (
                f"🌿 HEALTHBOT MENU\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"WELLNESS:\n"
                f"  💡 health tip  → Random wellness tip\n"
                f"  💧 water       → Daily water intake guide\n"
                f"  🏃 exercise    → Workout suggestions\n"
                f"  😴 sleep       → Sleep improvement tips\n"
                f"  🥗 diet        → Healthy food suggestions\n"
                f"  ⚖️  bmi         → Calculate your BMI\n"
                f"  🎯 challenge   → Today's health challenge\n"
                f"  💬 motivation  → Inspirational quotes\n\n"
                f"DISEASES (type any name):\n"
                f"  diabetes, hypertension, fever, dengue, asthma,\n"
                f"  thyroid, migraine, arthritis, stress, malaria,\n"
                f"  typhoid, tuberculosis, jaundice, anemia,\n"
                f"  cholesterol, pcod, skin, stomach, kidney\n\n"
                f"OTHER:\n"
                f"  🆘 emergency   → Emergency contacts\n"
                f"  📊 stats       → Your usage & score\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"Or just describe symptoms naturally — I understand! 😊"
            )

        # ── Disease Matching ──────────────────
        disease_map = {
            "diabetes":      ["diabetes", "diabetic", "blood sugar", "insulin", "sugar level", "type 2", "type 1"],
            "hypertension":  ["hypertension", "high blood pressure", "blood pressure", "bp", "systolic", "diastolic"],
            "fever":         ["fever", "cold", "flu", "cough", "runny nose", "sore throat", "temperature",
                              "body pain", "viral", "paracetamol", "crocin", "dolo"],
            "dengue":        ["dengue", "mosquito", "platelet", "breakbone", "aedes"],
            "asthma":        ["asthma", "inhaler", "wheez", "bronchial", "breathing problem"],
            "thyroid":       ["thyroid", "tsh", "hypothyroid", "hyperthyroid", "thyronorm", "metabolism"],
            "migraine":      ["migraine", "headache", "head pain", "head ache"],
            "arthritis":     ["arthritis", "joint pain", "knee pain", "gout", "uric acid",
                              "rheumatoid", "bone pain", "back pain"],
            "stress":        ["stress", "anxiety", "worried", "mental health", "depression",
                              "panic", "tension", "tense", "anxious"],
            "malaria":       ["malaria", "plasmodium", "anopheles", "cyclic fever"],
            "typhoid":       ["typhoid", "salmonella", "widal", "enteric"],
            "tuberculosis":  ["tuberculosis", "tb ", " tb", "dots", "sputum", "mycobacterium", "tubercul"],
            "jaundice":      ["jaundice", "yellow skin", "yellow eyes", "bilirubin", "hepatitis",
                              "liver disease", "liver problem"],
            "anemia":        ["anemia", "anaemia", "low hemoglobin", "low haemoglobin",
                              "low hb", "pale skin", "iron deficiency"],
            "cholesterol":   ["cholesterol", "ldl", "hdl", "triglyceride", "lipid profile", "statin"],
            "pcod":          ["pcod", "pcos", "polycystic", "irregular period", "hormonal imbalance",
                              "missed period"],
            "skin":          ["skin", "rash", "itch", "allergy", "pimple", "acne", "eczema",
                              "psoriasis", "hives", "fungal", "ringworm"],
            "stomach":       ["stomach", "gastric", "acidity", "gas", "bloating", "indigestion",
                              "constipation", "diarrhea", "loose motion", "ulcer", "abdominal"],
            "kidney":        ["kidney", "renal", "kidney stone", "uti", "urinary", "burning urination",
                              "dialysis", "nephro"],
        }

        for disease, keywords in disease_map.items():
            if any(k in msg for k in keywords):
                track(disease, 5)
                return DISEASE_DATA[disease]

        # ── Symptom guessing ──────────────────
        if has("chest pain", "chest"):
            return (
                f"⚠️ CHEST PAIN — Important\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Chest pain can have several causes:\n\n"
                f"🚨 CALL 108 IMMEDIATELY if you have:\n"
                f"  • Crushing/squeezing chest pain spreading to left arm\n"
                f"  • Chest pain with shortness of breath and sweating\n"
                f"  • These are signs of a HEART ATTACK\n\n"
                f"Less urgent causes:\n"
                f"  • Gastric/acidity — burning sensation after eating\n"
                f"  • Muscle strain — pain on pressing the chest wall\n"
                f"  • Anxiety/panic attack — with racing heartbeat\n"
                f"  • Asthma — with wheezing (type 'asthma' for guide)\n\n"
                f"🏥 Any new chest pain should be evaluated by a doctor.\n"
                f"   Emergency: 108"
            )

        if has("vomit", "nausea", "throw up"):
            return (
                f"🤢 NAUSEA & VOMITING — Guide\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Common causes:\n"
                f"  • Food poisoning, gastroenteritis\n"
                f"  • Motion sickness, migraine\n"
                f"  • Dengue fever, typhoid\n"
                f"  • Medication side effects\n\n"
                f"Immediate care:\n"
                f"  • Sip small amounts of water or ORS frequently\n"
                f"  • Avoid solid food for 2–4 hours\n"
                f"  • Domperidone or Ondansetron for vomiting\n"
                f"  • Ginger tea — natural anti-nausea remedy\n"
                f"  • Rest in a well-ventilated area\n\n"
                f"See a doctor if:\n"
                f"  • Vomiting persists more than 24 hours\n"
                f"  • Blood in vomit\n"
                f"  • Signs of dehydration: dry mouth, dark urine\n"
                f"  • Accompanied by high fever"
            )

        if has("dizzy", "dizziness", "giddy", "vertigo", "spinning"):
            return (
                f"😵 DIZZINESS / VERTIGO — Guide\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Common causes:\n"
                f"  • Low blood pressure (sit/lie down immediately)\n"
                f"  • Low blood sugar — eat something immediately\n"
                f"  • Dehydration — drink water\n"
                f"  • Inner ear problem (BPPV / Vertigo)\n"
                f"  • Anemia (type 'anemia' for guide)\n\n"
                f"Immediate action:\n"
                f"  • Sit or lie down immediately to prevent falls\n"
                f"  • Drink water and eat a small snack\n"
                f"  • Avoid sudden movements\n"
                f"  • Betahistine tablets help with vertigo\n\n"
                f"See a doctor if dizziness is:\n"
                f"  • Severe or recurring\n"
                f"  • With hearing loss or ringing ears\n"
                f"  • With double vision or slurred speech (stroke sign)\n"
                f"  🆘 Stroke: Call 108 immediately"
            )

        if has("weight loss", "losing weight", "weight gain", "gaining weight"):
            return (
                f"⚖️ UNEXPLAINED WEIGHT CHANGES\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Unexplained weight LOSS could indicate:\n"
                f"  • Hyperthyroidism (type 'thyroid' for guide)\n"
                f"  • Diabetes (type 'diabetes' for guide)\n"
                f"  • Tuberculosis — if with cough\n"
                f"  • Depression, stress, or eating disorders\n\n"
                f"Unexplained weight GAIN could indicate:\n"
                f"  • Hypothyroidism (type 'thyroid' for guide)\n"
                f"  • PCOD (type 'pcod' for guide)\n"
                f"  • Cushing's syndrome (excess cortisol)\n"
                f"  • Fluid retention from kidney/heart disease\n\n"
                f"Recommended tests:\n"
                f"  • TSH, blood sugar, CBC, LFT, KFT\n\n"
                f"Please consult a doctor for proper evaluation.\n"
                f"Use 'bmi' to check your current BMI."
            )

        # ── Fallback ──────────────────────────
        return (
            f"🤔 I'm not sure about that, {name}.\n\n"
            f"Try asking about specific diseases:\n"
            f"  'diabetes', 'fever', 'dengue', 'hypertension', 'asthma',\n"
            f"  'thyroid', 'migraine', 'arthritis', 'malaria', 'typhoid',\n"
            f"  'tuberculosis', 'jaundice', 'anemia', 'cholesterol',\n"
            f"  'pcod', 'skin', 'stomach', 'kidney', 'stress'\n\n"
            f"Or wellness topics:\n"
            f"  'health tip', 'water', 'exercise', 'sleep', 'diet', 'bmi'\n\n"
            f"Type 'help' for the full menu!"
        )

    # ── GREET ON START ───────────────────────

    def _greet(self):
        name = self.stats["user_name"]
        hour = datetime.datetime.now().hour
        tod = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        self._append(
            f"{tod}, {name}! 🌿 Welcome to HealthBot!\n\n"
            f"I'm your personal wellness companion.\n"
            f"⭐ Your health score: {self.stats['health_score']} points\n\n"
            f"I can help you with:\n"
            f"  🩺 19 diseases: diabetes, dengue, fever, hypertension...\n"
            f"  💡 Daily health tips, diet, exercise & sleep advice\n"
            f"  ⚖️  BMI calculator\n"
            f"  🆘 Emergency contacts (Tiruppur & Coimbatore)\n\n"
            f"Type naturally or use the sidebar menu on the left!\n"
            f"Try: 'I have a fever' or 'tell me about diabetes' 😊"
        )

    # ── HISTORY & UTILS ──────────────────────

    def _save_history(self):
        self.chat.config(state="normal")
        content = self.chat.get("1.0", "end")
        self.chat.config(state="disabled")
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"health_chat_{self.stats['user_name']}_{ts}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"HealthBot Chat — {self.stats['user_name']}\n")
            f.write(f"Saved on: {datetime.datetime.now()}\n")
            f.write("=" * 58 + "\n\n")
            f.write(content)
        messagebox.showinfo("Saved!", f"✅ Chat saved to:\n{fname}")

    def _clear_chat(self):
        if messagebox.askyesno("Clear Chat", "Clear the chat window?"):
            self.chat.config(state="normal")
            self.chat.delete("1.0", "end")
            self.chat.config(state="disabled")
            self._greet()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("")
    except Exception:
        pass

    def on_login(name):
        root.geometry("920x700")
        root.resizable(True, True)
        HealthBotApp(root, name)

    LoginScreen(root, on_login)
    root.mainloop()
