import json
import sys

with open("security-gate/config.json") as f:
    config = json.load(f)

with open("security-gate/reports/score.json") as f:
    score = json.load(f)

print(score)

if score["critical"] > config["critical_limit"]:
    print("Critical Vulnerability Found")
    sys.exit(1)

if score["score"] > config["score_limit"]:
    print("Risk Score Too High")
    sys.exit(1)

print("Security Gate Passed")
