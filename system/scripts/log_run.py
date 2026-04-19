from datetime import datetime, timezone
from pathlib import Path
import sys

if len(sys.argv) < 3:
    print('Usage: python3 system/scripts/log_run.py <skill-folder> "message"')
    sys.exit(1)

skill = sys.argv[1]
message = sys.argv[2]

log_dir = Path("skills") / skill / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

def read_skill_id(skill_name):
    current_file = Path("skills") / skill_name / "CURRENT"
    if not current_file.exists():
        return "unknown"

    skill_file = Path("skills") / skill_name / current_file.read_text().strip() / "skill.md"
    if not skill_file.exists():
        return "unknown"

    for line in skill_file.read_text().splitlines():
        if line.startswith("skill_id:"):
            return line.split(":", 1)[1].strip().strip('"')
    return "unknown"


now = datetime.now(timezone.utc)
skill_id = read_skill_id(skill)
log_file = log_dir / f"{now.date()}.log"
line = (
    f"{now.strftime('%Y-%m-%dT%H:%M:%SZ')} | run | "
    f"skill_id: {skill_id} | "
    f"trigger: \"{message}\" | "
    "in_tokens: unknown | out_tokens: unknown | total_tokens: unknown | "
    "model: unknown | status: complete"
)

with open(log_file, "a") as f:
    f.write(f"{line}\n")

print(f"Logged to {log_file}")
