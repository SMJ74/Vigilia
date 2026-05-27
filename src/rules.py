import pandas as pd

class AMLRulesEngine:
    def __init__(self):
        self.rules = []
        self.threshold = 50

    def add_rule(self, rule_func, weight=20):
        self.rules.append((rule_func, weight))

    def calculate_risk_score(self, row):
        score = 0
        reasons = []
        
        for rule_func, weight in self.rules:
            if rule_func(row):
                score += weight
                reasons.append(rule_func.__name__.replace('_', ' ').title())
        
        return {
            'risk_score': min(score, 100),
            'flagged': score >= self.threshold,
            'reasons': reasons
        }

    def apply_rules(self, df):
        results = df.apply(self.calculate_risk_score, axis=1, result_type='expand')
        return pd.concat([df, results], axis=1)


# Define Rules
def large_amount(row):
    return row['amount'] > 10000

def structuring(row):
    return 8000 < row['amount'] < 10000

def high_risk_country(row):
    return row['country'] in ['NG', 'RU', 'CN'] and row['amount'] > 3000

def rapid_movement(row):
    return row['amount'] > 5000 and row['type'] == 'withdrawal'