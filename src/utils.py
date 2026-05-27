import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_synthetic_transactions(n=500):
    """Generate fake transaction data"""
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(n):
        data.append({
            'transaction_id': fake.uuid4()[:12],
            'account_id': fake.uuid4()[:8],
            'amount': round(random.uniform(50, 25000), 2),
            'timestamp': start_date + timedelta(minutes=random.randint(0, 43200)),
            'counterparty': fake.company(),
            'country': random.choice(['US', 'GB', 'NG', 'RU', 'CN', 'BR']),
            'type': random.choice(['transfer', 'deposit', 'withdrawal']),
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/sample_transactions.csv', index=False)
    print(f"✅ Generated {n} synthetic transactions")
    return df