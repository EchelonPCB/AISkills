from datetime import datetime
from pathlib import Path
import sys

if len(sys.argv) < 3:
    print('Usage: python3 system/scripts/log_run.py <skill-folder> "message"')
    sys.exit(1)

skill = sys.argv[1]
message = sys.argv[2]

log_dir = Path("skills") / skill / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / f"{datetime.now().date()}.log"
with open(log_file, "a") as f:
    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

print(f"Logged to {log_file}")