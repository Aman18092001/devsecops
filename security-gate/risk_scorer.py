import json

INPUT = "security-gate/reports/trivy-report.json"
OUTPUT = "security-gate/reports/score.json"

critical = high = medium = low = 0

with open(INPUT) as f:
    report = json.load(f)

for result in report.get("Results", []):

    for vuln in result.get("Vulnerabilities", []):

        sev = vuln["Severity"]

        if sev == "CRITICAL":
            critical += 1

        elif sev == "HIGH":
            high += 1

        elif sev == "MEDIUM":
            medium += 1

        elif sev == "LOW":
            low += 1

score = critical*10 + high*5 + medium*2 + low*0.5

output = {
    "critical": critical,
    "high": high,
    "medium": medium,
    "low": low,
    "score": score
}

with open(OUTPUT,"w") as f:
    json.dump(output,f,indent=4)

print(output)
