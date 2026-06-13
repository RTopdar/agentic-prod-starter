import os

metrics = []
PROMPTS_DIR = os.path.dirname(__file__)

# Dynamic Metric Loading
# Automatically discovers any new markdown files added to the prompts folder
for file in os.listdir(PROMPTS_DIR):
    if file.endswith(".md"):
        metrics.append(
            {
                "name": file.replace(".md", ""),
                "prompt": open(os.path.join(PROMPTS_DIR, file), "r").read(),
            }
        )
