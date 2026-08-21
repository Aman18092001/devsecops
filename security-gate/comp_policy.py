import json
import sys

def check_policy():
    print("[*] Running Security Policy Evaluation...")
    failed = False

    # Check Gitleaks
    try:
        with open('security-gate/reports/gitleaks-report.json') as f:
            if len(json.load(f)) > 0:
                print("[-] POLICY FAIL: Secrets found in code!")
                failed = True
    except FileNotFoundError:
        pass

    # Check Trivy
    try:
        with open('security-gate/reports/trivy-report.json') as f:
            data = json.load(f)
            for res in data.get('Results', []):
                for v in res.get('Vulnerabilities', []):
                    if v.get('Severity') == 'CRITICAL':
                        print(f"[-] POLICY FAIL: Critical CVE detected ({v.get('VulnerabilityID')})")
                        failed = True
    except FileNotFoundError:
        pass

    if failed:
        sys.exit(1)
    else:
        print("[+] Policy check passed cleanly.")

if __name__ == "__main__":
    check_policy()
