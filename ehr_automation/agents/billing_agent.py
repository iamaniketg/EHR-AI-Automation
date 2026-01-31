from ehr_automation.models.dtos import ClaimDTO

class BillingAgent:
    def check_claim(self, claim: ClaimDTO):
        print(f"[BillingAgent] Analyzing claim {claim.id} for anomalies...")
        
        # Simulate Anomaly Detection (e.g., Isolation Forest)
        # Here we use heuristic rules for the demo
        
        anomalies = []
        is_anomalous = False
        
        # Rule 1: High Total Amount outlier
        if claim.total > 5000:
            anomalies.append(f"Total amount ${claim.total} exceeds statistical threshold.")
            is_anomalous = True
            
        # Rule 2: Duplicate codes (Simulating sophisticated pattern detection)
        codes = [item['procedure'] for item in claim.items]
        if len(codes) != len(set(codes)):
             anomalies.append("Duplicate procedure codes detected.")
             is_anomalous = True

        if is_anomalous:
            print(f"[BillingAgent] ALERT: Anomalous claim detected! Reasons: {anomalies}")
            claim.status = "flagged_for_review"
        else:
            print("[BillingAgent] Claim passed automated review.")
            claim.status = "approved"
            
        return is_anomalous, anomalies
