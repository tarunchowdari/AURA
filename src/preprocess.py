import os
import json
import pandas as pd

def step_text_from_lines(step: dict):
    lines = step.get("Lines")
    if isinstance(lines, list):
        joined = " ".join([str(x).strip() for x in lines if str(x).strip()])
        if joined.strip():
            return joined.strip()
    return None

def step_text_from_text_raw(step: dict):
    text_raw = step.get("Text_raw")
    if isinstance(text_raw, str) and text_raw.strip():
        return text_raw.strip()
    return None

def preprocess_tmp_json(tmp_json_path: str, out_csv: str):
    with open(tmp_json_path, "r", encoding="utf-8") as f:
        guides = json.load(f)

    rows = []

    for guide in guides:
        if not isinstance(guide, dict):
            continue

        title = guide.get("Title")
        device = guide.get("Category")
        url = guide.get("Url")

        toolbox = guide.get("Toolbox", [])
        if isinstance(toolbox, list):
            tools_str = ", ".join([str(t) for t in toolbox if str(t).strip()])
        else:
            tools_str = str(toolbox)

        steps = guide.get("Steps")
        if not isinstance(steps, list):
            continue

        for step in steps:
            if not isinstance(step, dict):
                continue

            step_number = step.get("Order")
            step_tools = step.get("Tools", [])

            if isinstance(step_tools, list):
                step_tools_str = ", ".join([str(t) for t in step_tools if str(t).strip()])
            else:
                step_tools_str = str(step_tools)

            text = step_text_from_lines(step) or step_text_from_text_raw(step)
            if not text:
                continue

            rows.append({
                "title": title,
                "device": device,
                "url": url,
                "tools": tools_str,
                "step_tools": step_tools_str,
                "step_number": step_number,
                "text": text,
            })

    df = pd.DataFrame(rows)
    df.dropna(subset=["text"], inplace=True)

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df.to_csv(out_csv, index=False)

    print(f"✅ Saved {len(df)} steps to {out_csv}")

if __name__ == "__main__":
    tmp_json_path = r"data/raw/MyFixit-Dataset/tmp.json"
    out_csv = r"data/processed/ifixit_steps.csv"
    preprocess_tmp_json(tmp_json_path, out_csv)