import re

# 1. Update EVIDENCE_INDEX.md (Fix duplicates)
with open('research/EVIDENCE_INDEX.md', 'r') as f:
    lines = f.readlines()

new_lines = []
dup_counter = 90
for line in lines:
    if line.startswith('| EVI-00') and 'TBD' in line:
        pass # Skip the original TBD ones completely to clean up
    elif line.startswith('| EVI-00') and 'FACT' in line and not 'https://cloud.google.com/run/docs' in line:
        # Keep the valid ones but renumber them if they collide. Actually let's just rewrite the index cleanly.
        pass
    else:
        new_lines.append(line)

# Let's just sed the duplicates directly using bash later for precision.
