from src.utils import generate_synthetic_transactions
from src.rules import AMLRulesEngine, large_amount, structuring, high_risk_country, rapid_movement
import pandas as pd
import os

print("🚀 Starting Vigilia - AML Transaction Monitor\n")

# Generate or load data
data_file = 'data/sample_transactions.csv'

if not os.path.exists(data_file):
    print("Generating new synthetic data...")
    df = generate_synthetic_transactions(800)
else:
    print("Loading existing data...")
    df = pd.read_csv(data_file)

# Run Rules Engine
engine = AMLRulesEngine()
engine.add_rule(large_amount, 40)
engine.add_rule(structuring, 35)
engine.add_rule(high_risk_country, 30)
engine.add_rule(rapid_movement, 25)

print("Applying AML rules...")
enriched_df = engine.apply_rules(df)

# Show Results
print("\n" + "="*60)
print("VIGILIA RESULTS")
print("="*60)
print(f"Total Transactions     : {len(enriched_df)}")
print(f"Flagged Transactions   : {len(enriched_df[enriched_df['flagged']])}")
print(f"Average Risk Score     : {enriched_df['risk_score'].mean():.1f}")

print("\nTop 10 Flagged Transactions:")
flagged = enriched_df[enriched_df['flagged']].sort_values('risk_score', ascending=False).head(10)
print(flagged[['transaction_id', 'amount', 'country', 'type', 'risk_score', 'reasons']])

print("\n✅ Done! Run again to generate fresh data.")