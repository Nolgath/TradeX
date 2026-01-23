import os

# Define absolute path for logs.txt - shared across all modules
LOGS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs.txt")

# Ensure logs.txt exists
if not os.path.exists(LOGS_FILE):
    with open(LOGS_FILE, "w", encoding='utf-8') as f:
        f.write("")
