"""
prompts.py
----------
All prompt-building functions for the AI China Travel Assistant.

Each function takes structured inputs (user preferences, city names, etc.)
and returns a fully-formed string that is sent directly to Claude.

Keeping prompts here — separate from UI logic — makes them easy to
iterate on, test, and maintain without touching the Streamlit code.
"""

from typing import List


# ── City Recommendations ──────────────────────────────────────────────────────

def build_city_recommendation_prompt(
    budget: str,
    interests: List[str],
    crowd_level: str,
    duration: int,
    language: str,
    halal: bool,
    currency: str,
) -> str:
    """
    Build a prompt that asks Claude to recommend Chinese cities
    tailored to the traveller's profile.

    Args:
        budget:      e.g. "Mid-range"
        interests:   e.g. ["Food & Cuisine", "History & Culture"]
        crowd_level: e.g. "Mix of both"
        duration:    trip length in days

    Returns:
        Formatted prompt string.
    """
    interests_str = ", ".join(interests) if interests else "General sightseeing"

    return f"""
You are an expert China travel consultant with deep knowledge of every
Chinese city, region, cuisine, and cultural site.

A traveller is planning a {duration}-day trip to China with this profile:
- Budget level:       {budget}
- Main interests:     {interests_str}
- Crowd preference:   {crowd_level}

Your task:
1. Recommend exactly 4 Chinese cities or regions that best match this profile.
2. For EACH city, wrap its details in a stunning HTML block with a food background image. Use EXACTLY this structure:
<div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://loremflickr.com/800/400/food,[CITY_NAME_NO_SPACES]') center/cover; padding: 25px; border-radius: 12px; color: white; margin-bottom: 20px;">
    <h2 style="color: #F1C40F; margin-top: 0;">[City Name in English + Characters + Pinyin]</h2>
    <p><strong>Why it fits:</strong> [One-sentence explanation tied to their interests]</p>
    <p><strong>Top experiences:</strong></p>
    <ul>
        <li>[Experience 1]</li>
        <li>[Experience 2]</li>
        <li>[Experience 3]</li>
    </ul>
    <p><strong>🍲 Famous Local Food:</strong> [Name and brief description of 1 iconic dish]</p>
    <p><strong>🏪 Local Markets:</strong> [Name of a famous local market and its typical operating hours]</p>
    <p><strong>🎉 Special Event/Festival:</strong> [Name of a unique local event/festival and its exact dates or month]</p>
    <p><strong>💰 [TRANSLATE 'Average Daily Expenses']:</strong> [Estimated exact daily cost calculated strictly in {currency}] | <strong>📅 [TRANSLATE 'Best time']:</strong> [Months]</p>
    <p style="font-size: 0.9em; color: #E74C3C; background: rgba(255,255,255,0.9); padding: 5px 10px; border-radius: 4px; display: inline-block; margin-top: 10px;"><strong>⚠️ City Rule / Warning:</strong> [Specific local custom, scam, or rule to follow]</p>
</div>
(CRITICAL: Replace [CITY_NAME_NO_SPACES] with the english city name as exactly ONE continuous lowercase word with no spaces, e.g., 'beijing' or 'hongkong')

3. After the 4 cities, add a short "Suggested Route" section proposing a logical and practical travel order based on geography (e.g., Shanghai -> High Speed Train -> Beijing). Do NOT attempt to calculate exact real-time schedules or constraints.

Formatting rules:
- Use clear Markdown headers (## for city names, ### for sub-sections)
- Use bullet points for lists
- Be specific — avoid vague phrases like "beautiful scenery"
- Keep the tone enthusiastic but informative

CRITICAL REQUIREMENT: YOU MUST WRITE THE ENTIRE RESPONSE IN {language.upper()} (except for the required Markdown image URLs).
THIS INCLUDES TRANSLATING ALL THE BOLD HTML LABELS IN THE TEMPLATE (e.g. 'Why it fits:', 'Top experiences:', 'Famous Local Food:', 'Local Markets:', 'Special Event/Festival:', 'Average Daily Expenses:', 'Best time:', 'City Rule / Warning:') into {language.upper()}!
{"CRITICAL REQUIREMENT 2: The user strictly follows a MUSLIM HALAL / NO-PORK diet. ALL food recommendations must be strictly Halal, Muslim-friendly, Seafood-based, or Vegetarian." if halal else ""}
""".strip()


# ── Itinerary Generator ───────────────────────────────────────────────────────

def build_itinerary_prompt(
    city: str,
    duration: int,
    budget: str,
    interests: List[str],
    pace: str,
    focus: List[str],
    language: str,
    halal: bool,
    currency: str,
) -> str:
    """
    Build a prompt that asks Claude to generate a day-by-day itinerary.

    Args:
        city:      Target city name.
        duration:  Number of days.
        budget:    Budget tier.
        interests: Traveller interests.
        pace:      e.g. "Balanced"
        focus:     e.g. ["Sightseeing", "Food & Markets"]

    Returns:
        Formatted prompt string.
    """
    interests_str = ", ".join(interests) if interests else "General travel"
    focus_str     = ", ".join(focus)     if focus     else "Sightseeing"

    return f"""
You are a seasoned China travel guide creating a detailed, practical itinerary.

Destination: {city}
Duration:    {duration} days
Budget tier: {budget}
Traveller interests: {interests_str}
Travel pace: {pace}
Itinerary focus: {focus_str}

Create a complete day-by-day itinerary following these rules:

At the very beginning of your response, display a delicious real food photo from {city} using this EXACT markdown format: `![{city} Food](https://loremflickr.com/800/400/food,[CITY_NAME_NO_SPACES])` replacing [CITY_NAME_NO_SPACES] with the English name of the city as exactly ONE continuous word with no spaces.

Structure for EACH day:
### Day N — [Catchy day theme]
**Morning** (start time – time):
- Activity with location name, why it's worth visiting, and 1 practical tip

**Afternoon** (time – time):
- Activity details

**Evening** (time – onwards):
- Dinner recommendation: specific restaurant name or food district, dish to order, price range
- Optional evening activity

**Daily budget estimate:** [Estimated value in {currency}] {currency} (excluding accommodation)
**Getting around today:** [transport tip]

After all days, add these sections:
## Accommodation Recommendations
List 3 options (budget / mid-range / splurge) with neighbourhood and why

## Essential Tips for {city}
5 practical tips (transport card, scams to avoid, apps to install, etc.)

## Must-Try Foods in {city}
List 6 local dishes with a one-line description each

Formatting: Use Markdown. Be specific with names and prices.
Avoid generic advice. This should feel like it's written by someone who
actually lives in {city}.

CRITICAL REQUIREMENT: YOU MUST WRITE THE ENTIRE RESPONSE IN {language.upper()} (except for the required image URLs and Markdown syntax).
THIS INCLUDES TRANSLATING ALL BOLD LABELS (like 'Morning', 'Afternoon', 'Evening', 'Daily budget estimate', 'Getting around today', 'Accommodation Recommendations', 'Essential Tips') into {language.upper()}!
{"CRITICAL REQUIREMENT 2: The user strictly follows a MUSLIM HALAL / NO-PORK diet. ALL food recommendations and restaurant suggestions must be strictly Halal, Muslim-friendly, Seafood-based, or Vegetarian." if halal else ""}
""".strip()


# ── Culture & Food Explorer ───────────────────────────────────────────────────

def build_culture_food_prompt(
    topic: str,
    topic_type: str,
    depth: str,
    interests: List[str],
    language: str,
    halal: bool,
) -> str:
    """
    Build a prompt that asks Claude to explain a Chinese cultural
    concept or dish clearly and engagingly.

    Args:
        topic:      The concept or dish to explain.
        topic_type: Category label from the UI radio button.
        depth:      "Quick overview" or "Deep dive"
        interests:  Traveller interests (used to tailor examples).

    Returns:
        Formatted prompt string.
    """
    interests_str = ", ".join(interests) if interests else "travel"

    # Map UI labels to natural language for the prompt
    type_context = {
        "🍜 Food & Dish":          "food dish or culinary tradition",
        "🏛️ Cultural Concept":     "cultural or philosophical concept",
        "🎎 Customs & Etiquette":  "social custom or etiquette rule",
        "🀄 Language & Phrases":   "language feature or set of phrases",
    }.get(topic_type, "topic")

    detail_instruction = (
        "Keep it concise: 3–4 short sections, bullet points where helpful."
        if depth == "Quick overview"
        else
        "Go deep: history, regional variations, modern context, and practical tips."
    )

    return f"""
You are a knowledgeable and engaging Chinese culture and food expert
writing for a curious Western traveller.

Topic to explain: "{topic}"
Type of topic: {type_context}
Detail level: {depth}
Traveller background: interested in {interests_str}

{detail_instruction}

Structure your response with these sections (use ## headers):

## What is {topic}?
[Start this section by IMMEDIATELY displaying a real photo describing it using this EXACT markdown format: `![{topic}](https://loremflickr.com/800/400/food,[TOPIC_NO_SPACES])` replacing [TOPIC_NO_SPACES] with the english name of the dish or concept as exactly ONE continuous word with NO spaces (e.g. 'pekingduck', 'dimsum', 'architecture').]

Clear, jargon-free explanation in 2–4 sentences.

## The Story Behind It
Origin, history, or cultural significance — make it interesting.

## What to Expect as a Traveller
Practical, first-person framing: what you'll see, taste, or experience.
Include where to find it / when to encounter it.

## Insider Knowledge
1–3 facts or tips that most guidebooks skip.

{"## Regional Variations" if depth == "Deep dive" else ""}
{"Describe how this differs across Chinese regions." if depth == "Deep dive" else ""}

## One Thing NOT to Do
A common tourist mistake related to this topic and how to avoid it.

Tone: warm, enthusiastic, and educational — like a knowledgeable friend,
not a textbook. Use specific examples. No filler phrases.

CRITICAL REQUIREMENT: YOU MUST WRITE THE ENTIRE RESPONSE IN {language.upper()} (except for the required image URLs and Markdown syntax).
THIS INCLUDES TRANSLATING ALL HEADERS (like 'What is', 'The Story Behind It', 'What to Expect', 'Insider Knowledge', 'One Thing NOT to Do') into {language.upper()}!
{"CRITICAL REQUIREMENT 2: The user strictly follows a MUSLIM HALAL / NO-PORK diet. ALL explanations of dishes must consider the Halal constraints, avoiding pork entirely or explicitly pointing out Muslim-friendly alternatives." if halal else ""}
""".strip()
