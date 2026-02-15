#!/usr/bin/env python3
"""
data_generator.py
Generates 200 realistic synthetic provider profiles with intentional errors
NO API KEYS REQUIRED
"""

from faker import Faker
import pandas as pd
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
Faker.seed(42)  # For reproducibility

# Medical specialties
SPECIALTIES = [
    "Family Medicine", "Internal Medicine", "Pediatrics", "Cardiology",
    "Orthopedic Surgery", "Dermatology", "Psychiatry", "Radiology",
    "Emergency Medicine", "Anesthesiology", "Neurology", "Oncology",
    "Obstetrics & Gynecology", "Ophthalmology", "Pathology",
    "Gastroenterology", "Pulmonology", "Endocrinology", "Rheumatology"
]

# License states
STATES = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

def generate_npi():
    """Generate a realistic but fake 10-digit NPI"""
    return str(random.randint(1000000000, 9999999999))

def introduce_errors(data, error_rate=0.4):
    """Introduce realistic data quality issues (40% of records)"""
    if random.random() < error_rate:
        error_type = random.choice([
            'outdated_phone', 'wrong_address', 'old_email', 
            'moved_practice', 'specialty_change', 'inactive_license'
        ])
        
        if error_type == 'outdated_phone':
            data['phone'] = fake.phone_number()
            data['data_quality_issue'] = 'Phone may be outdated'
            
        elif error_type == 'wrong_address':
            data['address'] = fake.street_address()
            data['city'] = fake.city()
            data['data_quality_issue'] = 'Address verification needed'
            
        elif error_type == 'old_email':
            data['email'] = f"old_{fake.email()}"
            data['data_quality_issue'] = 'Email may be inactive'
            
        elif error_type == 'moved_practice':
            data['data_quality_issue'] = 'Provider may have relocated'
            
        elif error_type == 'specialty_change':
            data['data_quality_issue'] = 'Specialty verification needed'
            
        elif error_type == 'inactive_license':
            data['license_expiry'] = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            data['data_quality_issue'] = 'License may be expired'
    
    return data

def generate_provider_profile(provider_id):
    """Generate a single provider profile"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    provider = {
        'provider_id': provider_id,
        'npi': generate_npi(),
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"Dr. {first_name} {last_name}",
        'specialty': random.choice(SPECIALTIES),
        'phone': fake.phone_number(),
        'email': f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
        'address': fake.street_address(),
        'city': fake.city(),
        'state': random.choice(STATES),
        'zip_code': fake.zipcode(),
        'license_number': f"{random.choice(STATES)}{random.randint(100000, 999999)}",
        'license_state': random.choice(STATES),
        'license_expiry': (datetime.now() + timedelta(days=random.randint(30, 1095))).strftime('%Y-%m-%d'),
        'board_certified': random.choice([True, False]),
        'accepting_new_patients': random.choice([True, False]),
        'years_in_practice': random.randint(1, 40),
        'medical_school': fake.company() + " Medical School",
        'graduation_year': random.randint(1980, 2020),
        'hospital_affiliations': ', '.join([fake.company() + " Hospital" for _ in range(random.randint(1, 3))]),
        'languages': ', '.join(random.sample(['English', 'Spanish', 'Chinese', 'French', 'Hindi', 'Arabic'], k=random.randint(1, 3))),
        'data_quality_issue': None,
        'last_updated': (datetime.now() - timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d'),
        'record_status': 'active',
        'has_pdf_documents': random.choice([True, False])
    }
    
    # Introduce errors in ~40% of records
    provider = introduce_errors(provider, error_rate=0.4)
    
    return provider

def generate_synthetic_dataset(num_providers=200):
    """Generate complete synthetic provider dataset"""
    print(f"\n{'='*70}")
    print(f"GENERATING SYNTHETIC PROVIDER DATASET")
    print(f"{'='*70}\n")
    print(f"Generating {num_providers} synthetic provider profiles...")
    
    providers = []
    for i in range(1, num_providers + 1):
        provider = generate_provider_profile(i)
        providers.append(provider)
        
        if i % 50 == 0:
            print(f"  Generated {i} providers...")
    
    # Convert to DataFrame
    df = pd.DataFrame(providers)
    
    # Calculate error statistics
    error_count = df['data_quality_issue'].notna().sum()
    error_rate = (error_count / len(df)) * 100
    
    print(f"\n{'='*70}")
    print(f"DATASET GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"\n📊 Statistics:")
    print(f"  • Total Providers: {len(df)}")
    print(f"  • Records with Quality Issues: {error_count} ({error_rate:.1f}%)")
    print(f"  • Clean Records: {len(df) - error_count} ({100-error_rate:.1f}%)")
    print(f"  • Providers with PDFs: {df['has_pdf_documents'].sum()}")
    
    return df

def save_dataset(df, output_path='data/synthetic_providers.csv'):
    """Save dataset to CSV"""
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset saved to: {output_path}")
    
def create_sample_pdfs_metadata(num_pdfs=20):
    """Generate metadata for sample PDF documents"""
    pdf_samples = []
    
    for i in range(1, num_pdfs + 1):
        pdf_info = {
            'pdf_id': i,
            'filename': f"provider_license_{i}.pdf",
            'document_type': random.choice(['License Certificate', 'Board Certification', 'Credential Letter']),
            'provider_name': fake.name(),
            'license_number': f"{random.choice(STATES)}{random.randint(100000, 999999)}",
            'state': random.choice(STATES),
            'issue_date': fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d'),
            'expiry_date': fake.date_between(start_date='today', end_date='+3y').strftime('%Y-%m-%d'),
            'document_quality': random.choice(['High', 'Medium', 'Low', 'Scanned']),
            'requires_ocr': random.choice([True, False])
        }
        pdf_samples.append(pdf_info)
    
    return pd.DataFrame(pdf_samples)

def main():
    """Main execution"""
    print("\n🏥 PROVIDER DIRECTORY DATA GENERATOR")
    print("   No API keys required - Fully synthetic data\n")
    
    # Generate main provider dataset
    providers_df = generate_synthetic_dataset(200)
    save_dataset(providers_df)
    
    # Generate PDF metadata
    pdf_df = create_sample_pdfs_metadata(20)
    pdf_df.to_csv('data/sample_pdfs_metadata.csv', index=False)
    print(f"✅ PDF metadata saved to: data/sample_pdfs_metadata.csv")
    
    # Display sample records
    print(f"\n{'='*70}")
    print("SAMPLE PROVIDER RECORDS (First 10)")
    print(f"{'='*70}\n")
    print(providers_df[['provider_id', 'full_name', 'specialty', 'state', 'data_quality_issue']].head(10).to_string(index=False))
    
    # Data quality breakdown
    print(f"\n{'='*70}")
    print("DATA QUALITY ISSUE BREAKDOWN")
    print(f"{'='*70}\n")
    issue_counts = providers_df['data_quality_issue'].value_counts(dropna=False)
    for issue, count in issue_counts.items():
        if pd.isna(issue):
            print(f"  • No Issues: {count}")
        else:
            print(f"  • {issue}: {count}")
    
    # Specialty distribution
    print(f"\n{'='*70}")
    print("SPECIALTY DISTRIBUTION (Top 10)")
    print(f"{'='*70}\n")
    specialty_counts = providers_df['specialty'].value_counts().head(10)
    for specialty, count in specialty_counts.items():
        print(f"  • {specialty}: {count}")
    
    print(f"\n{'='*70}")
    print("✅ DATA GENERATION COMPLETE!")
    print(f"{'='*70}")
    print("\nYou can now:")
    print("  1. Run validation: python demo_runner.py")
    print("  2. Start API: python main_no_api.py")
    print("  3. Start dashboard: streamlit run streamlit-app.py\n")

if __name__ == "__main__":
    main()
