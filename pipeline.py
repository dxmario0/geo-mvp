from modules.prompt_discovery import run_prompt_discovery


def run_geo_pipeline(question):

    print("========== GEO Pipeline ==========")

    measurement_queries = run_prompt_discovery(question)

    return {
        "status": "Prompt Discovery completed",
        "measurement_queries": measurement_queries.to_dict("records")
    }
