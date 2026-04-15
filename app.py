"""
AI China Travel Assistant
=========================
A Streamlit application that uses DeepSeek API to help users plan
their China travel experience — city recommendations, itineraries,
and cultural/food explanations.
"""

import streamlit as st
from openai import OpenAI

from prompts import (
    build_city_recommendation_prompt,
    build_itinerary_prompt,
    build_culture_food_prompt,
)
from config import APP_TITLE, APP_SUBTITLE, MODEL_NAME, MAX_TOKENS, API_BASE_URL


# ── Page setup ───────────────────────────────────────────────────────────────

def configure_page() -> None:
    """Set Streamlit page metadata and apply custom CSS."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🐉",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .main-title  { font-size: 2.4rem; font-weight: 700; color: #C0392B; }
        .sub-title   { font-size: 1.1rem; color: #7F8C8D; margin-top: -0.5rem; }
        .section-hdr { font-size: 1.3rem; font-weight: 600; color: #2C3E50;
                        border-left: 4px solid #C0392B; padding-left: 10px; }
        .info-box    { background: #FEF9E7; border-radius: 8px; color: #333333;
                        padding: 1rem 1.2rem; border: 1px solid #F9CA24; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── DeepSeek API helper ───────────────────────────────────────────────────────

def call_deepseek(prompt: str) -> str:
    """
    Send a prompt to DeepSeek and return the text response.
    DeepSeek is OpenAI-compatible, so we use the openai SDK.

    Args:
        prompt: The fully-formed prompt string.

    Returns:
        The assistant's reply as plain text.
    """
    import os
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["DEEPSEEK_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = "BAZI_DURUMLAR_ICIN_GECICI_KEY_VEYA_YOUR_KEY" # Uyarı için

    client = OpenAI(
        api_key=api_key,
        base_url=API_BASE_URL,
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ── Sidebar: user preferences ────────────────────────────────────────────────

def render_sidebar() -> dict:
    """
    Render the sidebar input widgets and return the collected preferences.

    Returns:
        A dict with keys: budget, interests, crowd_level, duration.
    """
    st.sidebar.image(
        "logo.png",
        width=180,
    )
    st.sidebar.title("Your Travel Profile")

    language = st.sidebar.selectbox(
        "🌐 Language",
        options=["English", "Türkçe", "中文 (Chinese)", "Polski", "Français", "Deutsch", "العربية", "Español", "Русский"],
    )

    currency_map = {
        "English": "USD", "Türkçe": "TRY", "中文 (Chinese)": "CNY",
        "Polski": "PLN", "Français": "EUR", "Deutsch": "EUR",
        "العربية": "AED", "Español": "EUR", "Русский": "RUB"
    }
    currency = currency_map.get(language, "USD")

    budget = st.sidebar.number_input(
        f"💰 Budget Limit ({currency})",
        min_value=0,
        value=50000 if currency in ["TRY", "RUB"] else (15000 if currency == "CNY" else 1500),
        step=100,
    )

    halal = st.sidebar.checkbox("☪️ Halal / Muslim-Friendly Diet")

    interests = st.sidebar.multiselect(
        "🎯 Interests",
        options=["History & Culture", "Food & Cuisine", "Nature & Scenery",
                 "Modern Cities & Nightlife", "Adventure & Hiking",
                 "Art & Architecture", "Traditional Villages"],
        default=["Food & Cuisine", "History & Culture"],
    )

    crowd_level = st.sidebar.radio(
        "👥 Crowd Preference",
        options=["Popular & iconic", "Off the beaten path", "Mix of both"],
        index=2,
    )

    duration = st.sidebar.slider(
        "📅 Trip Duration (days)",
        min_value=3,
        max_value=21,
        value=10,
        step=1,
    )

    st.sidebar.markdown("---")
    
    with st.sidebar.expander("📱 Essential China Apps", expanded=False):
        st.markdown(
            "<small><b>Note:</b> Global services like Google and WhatsApp are blocked in China. Download these before you arrive:</small>\n"
            "- 🛡️ **VPN:** Absolute necessity. Install reliable VPNs before flying.\n"
            "- 💳 **Alipay:** Cash/Cards are rarely accepted. <a href='https://www.travelchinaguide.com/essential/alipay.htm' target='_blank'>How to setup Alipay</a>.\n"
            "- 🚖 **DiDi:** The standard taxi hailing app (has an English interface).\n"
            "- 🗺️ **Amap (Gaode):** Accurate local maps (Apple Maps is also good).\n"
            "- 🗣️ **Baidu Translate:** Crucial for offline Chinese translation.\n"
            "- 🏨 **Trip.com / Agoda:** Best apps for booking hostels, hotels, and trains in China.\n"
            "- 🛵 **Meituan / Ele.me:** Ultimate apps for lightning-fast online food and grocery delivery.\n"
            "- 📶 **Airalo / Nomad (eSIM):** Buy an eSIM before you arrive. It automatically bypasses the Great Firewall!",
            unsafe_allow_html=True
        )

    with st.sidebar.expander("🏮 Public Holidays & Festivals", expanded=False):
        st.markdown(
            "<small>Avoid traveling during peak national holidays to skip massive crowds!</small>\n"
            "- **Spring Festival (Jan/Feb):** World's largest human migration. Shops may close.\n"
            "- **Labor Day (May 1-5):** Very busy domestic travel period.\n"
            "- **National Day / Golden Week (Oct 1-7):** Extremely crowded everywhere.\n"
            "- **Mid-Autumn (Sep/Oct):** Beautiful lanterns & mooncakes, bustling streets.",
            unsafe_allow_html=True
        )

    with st.sidebar.expander("🚨 Emergency Numbers & SOS", expanded=False):
        st.markdown(
            "- **Police:** 110\n"
            "- **Ambulance:** 120\n"
            "- **Fire:** 119\n"
            "- **Traffic Police:** 122\n"
            "<small><i>Tip: Operators rarely speak English. English translation apps are vital in emergencies.</i></small>",
            unsafe_allow_html=True
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<small>Powered by DeepSeek AI · Built with Streamlit</small>",
        unsafe_allow_html=True,
    )

    return {
        "budget": f"Up to {budget} {currency}",
        "currency": currency,
        "interests": interests,
        "crowd_level": crowd_level,
        "duration": duration,
        "language": language,
        "halal": halal,
    }


# ── Tab 1: City Recommendations ──────────────────────────────────────────────

def render_city_recommendations(prefs: dict) -> None:
    """Render the city recommendation tab."""
    st.markdown('<p class="section-hdr">🏙️ City Recommendations</p>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="info-box">Set your preferences in the left sidebar, '
        'then click the button below to get personalised city picks.</div>',
        unsafe_allow_html=True,
    )

    if not prefs["interests"]:
        st.warning("Please select at least one interest in the sidebar.")
        return

    if st.button("🔍 Recommend Cities", use_container_width=True, type="primary"):
        with st.spinner("Finding your perfect Chinese cities…"):
            prompt = build_city_recommendation_prompt(
                budget=prefs["budget"],
                interests=prefs["interests"],
                crowd_level=prefs["crowd_level"],
                duration=prefs["duration"],
                language=prefs["language"],
                halal=prefs["halal"],
                currency=prefs["currency"],
            )
            response = call_deepseek(prompt)

        st.success("Here are your personalised city recommendations!")
        st.markdown(response, unsafe_allow_html=True)


# ── Tab 2: Itinerary Generator ───────────────────────────────────────────────

def render_itinerary_generator(prefs: dict) -> None:
    """Render the itinerary generator tab."""
    st.markdown('<p class="section-hdr">🗺️ Itinerary Generator</p>',
                unsafe_allow_html=True)

    city = st.text_input(
        "Which city do you want an itinerary for?",
        placeholder="e.g. Chengdu, Xi'an, Shanghai…",
    )

    col1, col2 = st.columns(2)
    with col1:
        pace = st.selectbox(
            "Travel pace",
            ["Relaxed (fewer spots, more depth)",
             "Balanced",
             "Packed (maximum sightseeing)"],
            index=1,
        )
    with col2:
        focus = st.multiselect(
            "Itinerary focus",
            options=["Sightseeing", "Food & Markets", "Day trips",
                     "Local experiences", "Shopping", "Nightlife"],
            default=["Sightseeing", "Food & Markets"],
        )

    if st.button("📋 Generate Itinerary", use_container_width=True, type="primary"):
        if not city.strip():
            st.warning("Please enter a city name.")
            return

        with st.spinner(f"Building your {prefs['duration']}-day {city} itinerary…"):
            prompt = build_itinerary_prompt(
                city=city.strip(),
                duration=prefs["duration"],
                budget=prefs["budget"],
                interests=prefs["interests"],
                pace=pace,
                focus=focus,
                language=prefs["language"],
                halal=prefs["halal"],
                currency=prefs["currency"],
            )
            response = call_deepseek(prompt)

        st.success(f"Your {prefs['duration']}-day {city} itinerary is ready!")
        st.markdown(response, unsafe_allow_html=True)


# ── Tab 3: Culture & Food Explorer ───────────────────────────────────────────

def render_culture_food(prefs: dict) -> None:
    """Render the culture & food explanation tab."""
    st.markdown('<p class="section-hdr">🥢 Culture & Food Explorer</p>',
                unsafe_allow_html=True)

    topic_type = st.radio(
        "What would you like to explore?",
        options=["🍜 Food & Dish", "🏛️ Cultural Concept", "🎎 Customs & Etiquette",
                 "🀄 Language & Phrases"],
        horizontal=True,
    )

    topic = st.text_input(
        "Enter a topic to explore",
        placeholder="e.g. Dim Sum, Confucianism, chopstick etiquette, basic Mandarin phrases…",
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        depth = st.selectbox("Detail level", ["Quick overview", "Deep dive"])

    if st.button("🔎 Explain This", use_container_width=True, type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic to explore.")
            return

        with st.spinner(f"Researching '{topic}'…"):
            prompt = build_culture_food_prompt(
                topic=topic.strip(),
                topic_type=topic_type,
                depth=depth,
                interests=prefs["interests"],
                language=prefs["language"],
                halal=prefs["halal"],
            )
            response = call_deepseek(prompt)

        st.success(f"Here's everything you need to know about: **{topic}**")
        st.markdown(response, unsafe_allow_html=True)

    # Quick-access popular topics
    st.markdown("---")
    st.markdown("**Popular topics to explore:**")
    quick_topics = [
        "Peking Duck", "Dim Sum", "Face (Mianzi)", "Tea ceremony",
        "Chinese New Year", "Mahjong", "Baijiu", "Chopstick rules",
    ]
    cols = st.columns(4)
    for i, t in enumerate(quick_topics):
        if cols[i % 4].button(t, key=f"quick_{t}"):
            with st.spinner(f"Researching '{t}'…"):
                prompt = build_culture_food_prompt(
                    topic=t,
                    topic_type="🍜 Food & Dish" if i < 4 else "🏛️ Cultural Concept",
                    depth="Quick overview",
                    interests=prefs["interests"],
                    language=prefs["language"],
                    halal=prefs["halal"],
                )
                response = call_deepseek(prompt)
            st.success(f"Here's everything you need to know about: **{t}**")
            st.markdown(response, unsafe_allow_html=True)


# ── Main entry point ──────────────────────────────────────────────────────────

def main() -> None:
    configure_page()

    # Header
    st.markdown('<p class="main-title">🐉 AI China Travel Assistant</p>',
                unsafe_allow_html=True)
    st.markdown(f'<p class="sub-title">{APP_SUBTITLE}</p>',
                unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar returns the user's preferences
    prefs = render_sidebar()

    # Three feature tabs
    tab1, tab2, tab3 = st.tabs([
        "🏙️ City Recommendations",
        "🗺️ Itinerary Generator",
        "🥢 Culture & Food",
    ])

    with tab1:
        render_city_recommendations(prefs)

    with tab2:
        render_itinerary_generator(prefs)

    with tab3:
        render_culture_food(prefs)


if __name__ == "__main__":
    main()
