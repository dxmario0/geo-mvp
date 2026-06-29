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

def normalize_topic(topic):

    prompt = f"""
You are helping with GEO prompt discovery.

Convert the business topic into Google Trends
search topics that consumers would actually search.

Requirements:
- Preserve meaning.
- Stay in the same market.
- Use common consumer language.
- Prefer phrases people actually search.
- Avoid technical terminology.
- Return the most commonly searched phrase first.
- One topic per line.
- No bullets.
- No numbering.

Examples:

Business Topic:
rideshare services

Output:
ride sharing
ride hailing
rideshare

Business Topic:
international money transfer

Output:
money transfer
send money internationally
international transfer

Business Topic:
graphic design software

Output:
graphic design
design software
graphic design tools

Now generate topics for:

Business Topic:
{topic}
"""

    response = gemini_model.generate_content(
        prompt
    )

    topics = []

    for line in response.text.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = (
            line.replace("-", "")
                .replace("*", "")
                .strip()
        )

        if (
            line.lower().startswith("output")
            or line.lower().startswith("business topic")
        ):
            continue

        topics.append(line)

    return topics[:3]
