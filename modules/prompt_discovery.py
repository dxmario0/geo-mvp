import os
import time

import pandas as pd

from config.settings import (
    PROJECT_DIR,
    gemini_model,
    pytrends
)


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

    response = gemini_model.generate_content(prompt)

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

    response = gemini_model.generate_content(prompt)

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


def get_google_trends_queries(topic):

    try:

        pytrends.build_payload(
            [topic],
            timeframe="today 12-m"
        )

        related_queries = pytrends.related_queries()

        if (
            topic in related_queries
            and related_queries[topic] is not None
        ):

            top_df = related_queries[topic]["top"]

            if (
                top_df is not None
                and not top_df.empty
            ):

                print(f"Google Trends topic found: {topic}")

                return top_df, topic

    except Exception as e:

        if "429" in str(e):

            raise RuntimeError(
                "Google Trends rate limit hit (HTTP 429)."
            )

    print(f"No Trends data for: {topic}")

    candidate_topics = normalize_topic(topic)

    print(f"Candidate topics: {candidate_topics}")

    for candidate_topic in candidate_topics:

        try:

            print(f"Trying normalized topic: {candidate_topic}")

            time.sleep(2)

            pytrends.build_payload(
                [candidate_topic],
                timeframe="today 12-m"
            )

            related_queries = pytrends.related_queries()

            if (
                candidate_topic in related_queries
                and related_queries[candidate_topic] is not None
            ):

                top_df = related_queries[candidate_topic]["top"]

                if (
                    top_df is not None
                    and not top_df.empty
                ):

                    print(
                        f"Using normalized topic: {candidate_topic}"
                    )

                    return top_df, candidate_topic

        except Exception as e:

            if "429" in str(e):

                raise RuntimeError(
                    "Google Trends rate limit hit (HTTP 429)."
                )

            print(f"Failed for {candidate_topic}: {e}")

    raise ValueError(
        f"No Google Trends data found for '{topic}'."
    )


def run_prompt_discovery(question):

    print("Step 1 - Extracting business topic...")

    business_topic = extract_business_topic(question)

    print(f"Business Topic: {business_topic}")

    print("Step 2 - Retrieving Google Trends queries...")

    top_df, trends_topic = get_google_trends_queries(
        business_topic
    )

    print(f"Google Trends Topic: {trends_topic}")

    queries = top_df["query"].head(5).tolist()

    prompt = f"""
You are helping with GEO prompt discovery.

For each query below, determine whether it should be
used for GEO visibility measurement.

REMOVE if:
- contains a company, brand, or product name
- is primarily a definition or educational query

KEEP if:
- category query
- commercial intent query
- market research query

Return ONLY the queries to KEEP.

One query per line.

Queries:

{chr(10).join(queries)}
"""

    response = gemini_model.generate_content(prompt)

    kept_queries = [

        line.strip()

        for line in response.text.split("\n")

        if line.strip()

    ]

    measurement_queries = top_df[
        top_df["query"].isin(
            kept_queries
        )
    ].head(3)

    output_file = os.path.join(
        PROJECT_DIR,
        "measurement_queries.csv"
    )

    measurement_queries.to_csv(
        output_file,
        index=False
    )

    print(f"Saved: {output_file}")

    return measurement_queries
