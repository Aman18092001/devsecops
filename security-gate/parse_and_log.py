import json
import os
import sys
import mysql.connector

build_no = sys.argv[1] if len(sys.argv) > 1 else "1"

# Resolve absolute path to report directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def safe_load_json(file_name):
    path = os.path.join(REPORTS_DIR, file_name)
    if os.path.exists(path) and os.path.getsize(path) > 3:
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error loading {file_name}: {e}")
    return None

def parse_reports():
    violations = []

    # 1. Gitleaks Parsing
    gitleaks_data = safe_load_json("gitleaks-report.json")
    if isinstance(gitleaks_data, list):
        for s in gitleaks_data:
            violations.append((
                build_no, s.get('RuleID', 'SECRET_LEAK'), 'SECRET',
                'NIST-IA-5', 'CIS-16.4', 'OWASP-A07:2021', 'CRITICAL', 'VIOLATION'
            ))

    # 2. Semgrep SAST Parsing
    semgrep_data = safe_load_json("semgrep-report.json")
    if isinstance(semgrep_data, dict):
        for res in semgrep_data.get('results', []):
            check_id = res.get('check_id', '').lower()
            owasp_cat = 'OWASP-A03:2021' if any(k in check_id for k in ['sqli', 'injection', 'command']) else 'OWASP-A01:2021'
            violations.append((
                build_no, res.get('check_id', 'SAST_FINDING'), 'SAST',
                'NIST-SA-11', 'CIS-16.1', owasp_cat, res.get('extra', {}).get('severity', 'HIGH'), 'VIOLATION'
            ))

    # 3. Trivy Container Parsing
    trivy_data = safe_load_json("trivy-report.json")
    if isinstance(trivy_data, dict):
        for res in trivy_data.get('Results', []):
            for v in res.get('Vulnerabilities', []):
                sev = v.get('Severity')
                if sev in ['CRITICAL', 'HIGH']:
                    violations.append((
                        build_no, v.get('VulnerabilityID'), 'CONTAINER',
                        'NIST-SI-2', 'CIS-7.5', 'OWASP-A06:2021', sev, 'VIOLATION'
                    ))

    return violations

def log_to_mysql(violations):
    try:
        conn = mysql.connector.connect(
            host="172.31.13.180",
            port=3306,
            user="aman",
            password="aman",
            database="devsecops_audit"
        )
        cursor = conn.cursor()

        # Update Summary
        status = "FAILED" if len(violations) > 0 else "PASSED"
        cursor.execute(
            """INSERT INTO build_compliance_summary 
               (build_number, repository_url, branch, environment, total_cves, policy_status) 
               VALUES (%s, %s, %s, %s, %s, %s) 
               ON DUPLICATE KEY UPDATE total_cves=%s, policy_status=%s""",
            (build_no, "https://github.com/Aman18092001/devsecops.git", "main", "dev", len(violations), status, len(violations), status)
        )

        # Batch Insert Detailed Framework Logs
        if violations:
            query = """INSERT INTO framework_compliance_logs 
                       (build_number, cve_or_rule_id, finding_type, nist_control, cis_control, owasp_category, severity, status) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(query, violations)

        conn.commit()
        print(f"[+] Successfully inserted {len(violations)} compliance records into MySQL for Build #{build_no}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[-] MySQL Logging Failed: {e}")

if __name__ == "__main__":
    records = parse_reports()
    log_to_mysql(records)
