import random
import  numpy as np


facts_schema = {
    # Taxpayer profile
    'filing_status': ['single', 'married_joint', 'married_separate', 'business'],
    'year': ['2023', '2024', '2025'],
    'age': ['<65', '>=65'],

    # Filing behavior
    'filed_on_time': ['true', 'false'],

    # Income sources
    'employment_income': 'int',
    'business_income': 'int',
    'capital_gains': 'int',
    'foreign_income': 'int',

    # Deductions and exemptions
    'deductions': 'int',
    'medical_expenses': 'int',
    'church_tax': ['mandatory', 'opted_out'],

    # Compliance / penalties
    'penalties': ['none', 'late_fee', 'fraud_investigation'],
    'audited': ['true', 'false'],

}

def generate_facts():
    """
    Generates a random data object from a combination of filing conditions to emulate real tax scenarios
    :return: Dictionary of individual and factual information of the individual.
    """
    return {
        'filing_status': random.choice(facts_schema['filing_status']),
        'year': random.choice(facts_schema['year']),
        'age': random.choice(facts_schema['age']),
        'filed_on_time': random.choice(facts_schema['filed_on_time']),
        'employment_income': int(np.random.randint(10_000, 150_000)),
        'business_income': int(np.random.randint(0, 200_000)),
        'capital_gains': int(np.random.randint(0, 50_000)),
        'foreign_income': int(np.random.randint(0, 75_000)),
        'deductions': int(np.random.randint(1_000, 20_000)),
        'medical_expenses': int(np.random.randint(0, 15_000)),
        'church_tax': random.choice(facts_schema['church_tax']),
        'penalties': random.choice(facts_schema['penalties']),
        'audited': random.choice(facts_schema['audited'])
    }
