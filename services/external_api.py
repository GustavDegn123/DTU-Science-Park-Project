import random

def fetch_external_data():
    """
    Simulerer API-kald til ESG-data, traction og andre relevante impact-metrics.
    """
    return {
        "esg_score": random.randint(60, 100),  # Simuleret ESG-score mellem 60 og 100
        "traction": random.randint(50, 90),  # Simuleret traction score
        "sdg_alignment": random.randint(50, 100)  # Simuleret SDG-alignment score
    }
