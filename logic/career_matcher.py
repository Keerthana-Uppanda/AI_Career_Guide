import pandas as pd

def load_careers(path: str) -> pd.DataFrame:
    """Load careers CSV safely."""
    df = pd.read_csv(path)
    # Ensure required columns exist
    for col in ["Career", "Key_Skills", "Education_Level", "Work_Style", "Personality", "Subjects", "Description"]:
        if col not in df.columns:
            df[col] = ""
    return df

def match_careers(filters: dict, df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter careers by education, work_style, personality.
    Filters example: {"education": "Bachelor's", "work_style": "Team|Remote", "personality": "Analytical|Creative"}
    """
    filtered = df.copy()

    # Education filter
    edu = filters.get("education", "").strip()
    if edu:
        filtered = filtered[filtered["Education_Level"].str.contains(edu, case=False, na=False)]

    # Work style filter
    ws = filters.get("work_style", "").strip()
    if ws:
        ws_options = ws.split("|")
        mask = filtered["Work_Style"].apply(lambda x: any(opt.lower() in x.lower() for opt in ws_options if x))
        filtered = filtered[mask]

    # Personality filter
    pers = filters.get("personality", "").strip()
    if pers:
        pers_options = pers.split("|")
        mask = filtered["Personality"].apply(lambda x: any(opt.lower() in x.lower() for opt in pers_options if x))
        filtered = filtered[mask]

    return filtered.reset_index(drop=True)
