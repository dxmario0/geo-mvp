from config.settings import gemini_model


def extract_business_topic(question):

    prompt = f"""
You are a GEO Analyst.

A company is asking about its visibility in AI search.

Your task is to identify the consumer market
or industry that the company operates in.

Do NOT identify:
- SEO
- Search
- Marketing
- Advertising
- AI

Instead identify the market being searched.

Examples:

Uber -> rideshare services

Airbnb -> vacation rentals

Wise -> international money transfer

Canva -> graphic design software

Return only the market topic.
No explanation.

Question:
{question}
"""

    response = gemini_model.generate_content(
        prompt
    )

    return response.text.strip()
