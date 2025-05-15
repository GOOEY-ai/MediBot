import streamlit as st
import datetime
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# File path for storing history
HISTORY_FILE = "symptom_history.json"



# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Load history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save history to file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = load_history()

# Title
st.title("🤖 MediBot - Your Personal Health Assistant")

if "name" not in st.session_state:
    st.session_state.name = ""

st.session_state.name = st.text_input("👤 Enter your name to begin:")

if not st.session_state.name:
    st.warning("Please enter your name to proceed.")
    st.stop()



# Sample Diagnosis Dictionary (deduplicated)
diagnosis_data = {
    "fever": {
        "action": "Stay hydrated and rest. If fever persists, consult a doctor.",
        "severity": "moderate",
        "category": "infectious disease",
        "possible_diseases": ["Flu", "COVID-19", "Malaria"]
    },
    "cough": {
        "action": "Try warm fluids, lozenges, and rest. Seek care if persistent.",
        "severity": "moderate",
        "category": "respiratory",
        "possible_diseases": ["Common Cold", "Bronchitis", "COVID-19", "Allergic Rhinitis"]
    },
    "leg pain": {
        "action": "Rest, elevate the leg, and take ibuprofen.",
        "severity": "moderate",
        "category": "musculoskeletal",
        "possible_diseases": ["Deep Vein Thrombosis", "Muscle Strain"]
    },
    "crash out": {
        "action": "Rest, hydrate, reduce stress. Try melatonin if needed.",
        "severity": "moderate",
        "category": "mental",
        "possible_diseases": ["Burnout", "Exhaustion", "Sleep Deprivation"]
    },
    "rash": {
        "action": "Apply hydrocortisone cream.",
        "severity": "mild",
        "category": "dermatological",
        "possible_diseases": ["Allergy", "Contact Dermatitis"]
    },
    "headache": {
        "action": "Rest, hydrate, use ibuprofen.",
        "severity": "mild",
        "category": "neurological",
        "possible_diseases": ["Tension Headache", "Migraine"]
    },
    "blurred vision": {
        "action": "Schedule an eye exam and avoid screen strain.",
        "severity": "moderate",
        "category": "neurological",
        "possible_diseases": ["Migraine Aura", "Glaucoma", "Stroke"]


   },
   "runny nose": {
       "action": "Rest, drink fluids, and use saline nasal spray.",
       "severity": "mild",
       "category": "respiratory",
       "possible_diseases": ["Common Cold", "Allergic Rhinitis", "Sinus Infection"]
   },
   "back pain": {
       "action": "Rest, apply heat or ice, and take pain relievers as needed.",
       "severity": "moderate",
       "category": "musculoskeletal",
       "possible_diseases": ["Muscle Strain", "Herniated Disc", "Sciatica"]
   },
   "harry armstrong": {
       "action": "Consult a healthcare professional for personalized treatment.",
       "severity": "varies",
       "category": "unknown",
       "possible_diseases": ["Harry Armstrong Syndrome (fictional, if it's a joke or hypothetical condition)"]
   },
 
   "leg pain": {
       "action": "Rest, elevate the leg, and take ibuprofen.",
       "severity": "moderate",
       "category": "musculoskeletal",
       "possible_diseases": ["Deep Vein Thrombosis", "Muscle Strain"]
   },
   "crash out": {
       "action": "Rest, hydrate, reduce stress. Try melatonin if needed.",
       "severity": "moderate",
       "category": "mental",
       "possible_diseases": ["Burnout", "Exhaustion", "Sleep Deprivation"]
   },
   "rash": {
       "action": "Apply hydrocortisone cream.",
       "severity": "mild",
       "category": "dermatological",
       "possible_diseases": ["Allergy", "Contact Dermatitis"]
   },
   "headache": {
       "action": "Rest, hydrate, use ibuprofen.",
       "severity": "mild",
       "category": "neurological",
       "possible_diseases": ["Tension Headache", "Migraine"]
   },
   "diarrhea": {
       "action": "Use loperamide and hydrate.",
       "severity": "moderate",
       "category": "gastrointestinal",
       "possible_diseases": ["Infection", "IBS"]
   },
   "menstrual cramps": {
       "action": "Use a hot pack, take ibuprofen, and rest.",
       "severity": "moderate",
       "category": "reproductive",
       "possible_diseases": ["Primary Dysmenorrhea", "Endometriosis"]
   },
   "cough": {
       "action": "Try warm fluids, lozenges, and rest. Seek care if persistent.",
       "severity": "moderate",
       "category": "respiratory",
       "possible_diseases": ["Common Cold", "Bronchitis", "COVID-19", "Allergic Rhinitis"]
   },
   "blurred vision": {
       "action": "Schedule an eye exam and avoid screen strain.",
       "severity": "moderate",
       "category": "neurological",
       "possible_diseases": ["Migraine Aura", "Glaucoma", "Stroke"]
   },
   "nausea": {
       "action": "Rest, avoid solid food for a few hours, sip clear fluids like ginger tea or electrolyte drinks.",
       "severity": "moderate",
       "category": "gastrointestinal",
       "possible_diseases": ["Gastroenteritis", "Pregnancy", "Food Poisoning", "Motion Sickness", "Migraine"]
   },
   "heart palpitations": {
       "action": "Reduce caffeine, hydrate, and consult a doctor.",
       "severity": "moderate",
       "category": "cardiovascular",
       "possible_diseases": ["Arrhythmia", "Anxiety Disorder", "Hyperthyroidism"]
   },
   "back pain": {
       "action": "Rest, use a heating pad, stretch gently, and take ibuprofen if needed.",
       "severity": "moderate",
       "category": "musculoskeletal",
       "possible_diseases": ["Muscle Strain", "Herniated Disc", "Sciatica", "Spinal Stenosis"]
   },
   "swollen ankle": {
       "action": "Elevate, ice, and rest. Consider compression.",
       "severity": "moderate",
       "category": "musculoskeletal",
       "possible_diseases": ["Sprain", "Fracture", "Gout"]
   },
   "yellow skin": {
       "action": "Seek medical evaluation urgently.",
       "severity": "severe",
       "category": "hepatic",
       "possible_diseases": ["Jaundice", "Hepatitis", "Liver Disease"]
   },
   "frequent urination": {
       "action": "Monitor fluid intake and schedule a checkup.",
       "severity": "moderate",
       "category": "urological",
       "possible_diseases": ["Urinary Tract Infection", "Diabetes", "Interstitial Cystitis"]
   },
   "burning urination": {
       "action": "Increase water intake and seek a urine test.",
       "severity": "moderate",
       "category": "urological",
       "possible_diseases": ["Urinary Tract Infection", "STI", "Kidney Infection"]
   },
   "loss of appetite": {
       "action": "Track meals and speak to a doctor if persistent.",
       "severity": "moderate",
       "category": "general",
       "possible_diseases": ["Depression", "Gastroenteritis", "Cancer"]
   },
   "joint pain": {
       "action": "Use anti-inflammatories and rest the joint.",
       "severity": "moderate",
       "category": "musculoskeletal",
       "possible_diseases": ["Arthritis", "Lupus", "Lyme Disease"]
   },
   "blood in stool": {
       "action": "Seek immediate medical attention.",
       "severity": "severe",
       "category": "gastrointestinal",
       "possible_diseases": ["Hemorrhoids", "Colon Cancer", "Anal Fissure"]
   },
   "night sweats": {
       "action": "Keep room cool and consult a doctor.",
       "severity": "moderate",
       "category": "general",
       "possible_diseases": ["Tuberculosis", "Menopause", "Lymphoma"]
   },
   "hand tremors": {
       "action": "Limit stimulants and seek a neurological exam.",
       "severity": "moderate",
       "category": "neurological",
       "possible_diseases": ["Parkinson’s Disease", "Essential Tremor", "Hyperthyroidism"]
   },
   "cold hands and feet": {
       "action": "Warm up with layers and check circulation.",
       "severity": "mild",
       "category": "vascular",
       "possible_diseases": ["Raynaud’s Disease", "Hypothyroidism", "Anemia"]
   },
   "excessive thirst": {
       "action": "Hydrate and test blood sugar levels.",
       "severity": "moderate",
       "category": "endocrine",
       "possible_diseases": ["Diabetes", "Dehydration", "Kidney Disease"]
   },
   "eye redness": {
       "action": "Use lubricating eye drops and avoid allergens.",
       "severity": "mild",
       "category": "ophthalmological",
       "possible_diseases": ["Conjunctivitis", "Allergic Reaction", "Dry Eye Syndrome"]
   },
   "ear pain": {
       "action": "Apply warm compress and take ibuprofen.",
       "severity": "moderate",
       "category": "ENT",
       "possible_diseases": ["Ear Infection", "Eustachian Tube Dysfunction", "Temporomandibular Joint Disorder"]
   },
   "hoarseness": {
       "action": "Rest voice and stay hydrated.",
       "severity": "mild",
       "category": "ENT",
       "possible_diseases": ["Laryngitis", "Vocal Cord Nodules", "GERD"]
   },
   "swollen lymph nodes": {
       "action": "Monitor and seek evaluation if persistent.",
       "severity": "moderate",
       "category": "immune",
       "possible_diseases": ["Infection", "Lymphoma", "Mononucleosis"]
   },
   "unexplained weight loss": {
       "action": "Consult your doctor for further testing.",
       "severity": "severe",
       "category": "general",
       "possible_diseases": ["Cancer", "Hyperthyroidism", "Diabetes"]
   },
   "painful urination": {
       "action": "Increase fluids and get tested.",
       "severity": "moderate",
       "category": "urological",
       "possible_diseases": ["Urinary Tract Infection", "STI", "Kidney Stones"]
   },
   "dry skin": {
       "action": "Apply moisturizer and avoid hot showers.",
       "severity": "mild",
       "category": "dermatological",
       "possible_diseases": ["Eczema", "Psoriasis", "Hypothyroidism"]
   },
   "dark urine": {
       "action": "Hydrate and check for liver or kidney issues.",
       "severity": "moderate",
       "category": "renal",
       "possible_diseases": ["Dehydration", "Hepatitis", "Hematuria"]
   },
   "slurred speech": {
       "action": "Call emergency services immediately.",
       "severity": "severe",
       "category": "neurological",
       "possible_diseases": ["Stroke", "Brain Injury", "Drug Overdose"]
   },
   "tingling fingers": {
       "action": "Avoid repetitive strain and consult a neurologist.",
       "severity": "moderate",
       "category": "neurological",
       "possible_diseases": ["Carpal Tunnel Syndrome", "Peripheral Neuropathy", "Cervical Disc Herniation"]
   },
   "facial drooping": {
       "action": "Seek emergency medical help immediately.",
       "severity": "severe",
       "category": "neurological",
       "possible_diseases": ["Stroke", "Bell’s Palsy", "Brain Tumor"]
   },
   "hair loss": {
       "action": "Check thyroid function and reduce stress.",
       "severity": "mild",
       "category": "dermatological",
       "possible_diseases": ["Alopecia Areata", "Hypothyroidism", "Iron Deficiency"]
   },
   "breast tenderness": {
       "action": "Monitor for cycle-related changes.",
       "severity": "mild",
       "category": "reproductive",
       "possible_diseases": ["PMS", "Hormonal Changes", "Fibrocystic Breasts"]
   },
   "excessive sweating": {
       "action": "Wear breathable fabrics and hydrate.",
       "severity": "mild",
       "category": "endocrine",
       "possible_diseases": ["Hyperhidrosis", "Hyperthyroidism", "Infection"]
   },
   "discolored nails": {
       "action": "Trim regularly and keep nails dry.",
       "severity": "mild",
       "category": "dermatological",
       "possible_diseases": ["Fungal Infection", "Psoriasis", "Iron Deficiency"]
   },
   # Overall Diagnosis based on multiple symptoms },
    "overall_diagnosis": {
        "action": "Based on the combination of your symptoms, we suggest considering a more comprehensive evaluation.",
        "severity": "moderate",
        "category": "general",
        "possible_diseases": [
            "Multiple Sclerosis",
            "Chronic Fatigue Syndrome",
            "Rheumatoid Arthritis",
            "Fibromyalgia",
            "Thyroid Disorder",
            "Systemic Infection"
        ]
    }
    # Add the rest of your cleaned diagnosis data here...
}

# Mood input using free text + sentiment analysis
mood_input = st.text_input("How are you feeling today? (Describe your mood)")
if mood_input:
    score = analyzer.polarity_scores(mood_input)
    compound = score["compound"]

    if compound >= 0.05:
        detected_mood = "positive"
    elif compound <= -0.05:
        detected_mood = "negative"
    else:
        detected_mood = "neutral"

    st.markdown(f"**Detected Mood:** {detected_mood.capitalize()} (Score: {compound})")

    # Proceed to symptom input
    symptoms = st.text_input("Please list your symptoms (comma-separated):")
    if symptoms:
        symptoms_list = [s.strip().lower() for s in symptoms.split(",")]
        matched_diagnoses = []

        for symptom in symptoms_list:
            for key in diagnosis_data:
                if key in symptom:
                    info = diagnosis_data[key]
                    matched_diagnoses.append({
                        "symptom": key,
                        "action": info["action"],
                        "severity": info["severity"],
                        "category": info["category"],
                        "possible_diseases": info["possible_diseases"]
                    })

        if matched_diagnoses:
            st.subheader("📋 Recommendations")
            for d in matched_diagnoses:
                st.markdown(f"**Symptom:** {d['symptom'].capitalize()}")
                st.markdown(f"- **Category:** {d['category']}")
                st.markdown(f"- **Severity:** {d['severity'].capitalize()}")
                st.markdown(f"- **Possible Diseases:** {', '.join(d['possible_diseases'])}")
                st.markdown(f"- **Suggested Action:** {d['action']}")
                st.markdown("---")
        else:
            st.info("No direct matches found. Consider consulting a healthcare professional.")

        
        
        
        
        # Save to history
        record = {
            "timestamp": str(datetime.datetime.now()),
            "name":  st.session_state.name,
            "mood_input": mood_input,
            "detected_mood": detected_mood,
            "symptoms": symptoms_list,
            "matched": matched_diagnoses
        }
        st.session_state.history.append(record)
        save_history(st.session_state.history)

# Admin Section
st.sidebar.title("🔐 Admin Panel")

# Simple authentication
admin_usernames = ["RonanEdirisinghe", "ArjunRao"]
admin_passwords = {"RonanEdirisinghe": "SteamShowcase1", "ArjunRao": "SteamShowcase2"}

admin_username = st.sidebar.text_input("Username")
admin_password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login as Admin"):
    if admin_username in admin_usernames and admin_password == admin_passwords.get(admin_username):
        st.session_state["is_admin"] = True
        st.success(f"Welcome, {admin_username}!")
    else:
        st.error("Invalid admin credentials.")

if st.session_state.get("is_admin"):
    st.subheader("🛠️ Admin Tools")

    # View full history
    if st.checkbox("📜 View User History"):
        if st.session_state.history:
            for i, entry in enumerate(st.session_state.history):
                st.markdown(f"**Record {i + 1}:**")
                st.json(entry)
        else:
            st.info("No user history available.")

    # Delete all history
    if st.button("🗑️ Delete All History"):
        st.session_state.history = []
        save_history([])
        st.success("All history has been deleted.")

    # Export history
    if st.button("📤 Export History"):
        st.download_button(
            label="Download JSON",
            data=json.dumps(st.session_state.history, indent=4),
            file_name="symptom_history_export.json",
            mime="application/json"
        )

    # Symptom frequency report
    if st.checkbox("📊 Show Symptom Frequency"):
        from collections import Counter
        all_symptoms = []
        for entry in st.session_state.history:
            all_symptoms.extend(entry.get("symptoms", []))
        if all_symptoms:
            freq = Counter(all_symptoms)
            st.bar_chart(freq)
        else:
            st.info("No symptoms logged yet.")

   # Logout section
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.markdown(f"**Logged in as:** `{st.session_state.username}`")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()
        

