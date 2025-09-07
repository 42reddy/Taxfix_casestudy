# domain_logic.py
import random
import numpy as np
from income_tax import names, countries, marital_statuses, hobbies, pets, question_bank

def generate_atomic_facts():
    # Base demographic facts
    name = random.choice(names)
    age = np.random.randint(25, 70)
    country = random.choice(countries)
    marital_status = random.choice(marital_statuses)

    # Financial facts
    income = int(np.random.randint(20_000, 120_000) // 1000 * 1000)
    deductions = int(np.random.randint(0, 10_000) // 1000 * 1000)
    medical_expenses = int(np.random.randint(0, 15_000) // 1000 * 1000)

    # Family composition facts
    if marital_status == "married":
        spouse_income = int(np.random.randint(0, 50_000) // 1000 * 1000)
        children_count = np.random.randint(0, 4)
    else:
        spouse_income = 0
        children_count = np.random.randint(0, 2)

    # Derived atomic boolean facts
    is_married = marital_status == "married"
    spouse_has_zero_income = spouse_income == 0
    has_children = children_count > 0

    # Country specific rules as atomic facts
    country_allows_joint_filing = country in ["USA", "Germany"]

    # Medical expense threshold calculation
    medical_threshold = int(0.075 * income)
    medical_expenses_exceed_threshold = medical_expenses > medical_threshold

    facts = {
        # Personal information
        "name": name,
        "age": age,
        "country": country,
        "marital_status": marital_status,

        # Financial information
        "income": income,
        "deductions": deductions,
        "medical_expenses": medical_expenses,
        "spouse_income": spouse_income,
        "children_count": children_count,

        # Derived boolean facts
        "is_married": is_married,
        "spouse_has_zero_income": spouse_has_zero_income,
        "has_children": has_children,
        "country_allows_joint_filing": country_allows_joint_filing,
        "medical_expenses_exceed_threshold": medical_expenses_exceed_threshold,

        # Threshold values for transparency
        "medical_expense_threshold": medical_threshold,
        "medical_threshold_percentage": 7.5,

        # Explicit rule statements
        "rule_joint_filing_countries": "Joint filing is allowed in USA and Germany only",
        "rule_joint_filing_spouse_requirement": "Joint filing requires spouse to have zero income",
        "rule_joint_filing_marital_requirement": "Joint filing requires married status",
        "rule_child_benefits_requirement": "Child benefits require having at least one child",
        "rule_medical_expense_threshold": "Medical expenses are high if they exceed 7.5% of income",

        # Step by step calculation facts
        "income_times_threshold_percent": int(income * 0.075),
        "medical_vs_threshold_comparison": f"{medical_expenses} vs {medical_threshold}",
        "joint_filing_conditions_met": is_married and spouse_has_zero_income and country_allows_joint_filing
    }

    return facts

def generate_diversity_facts():
    return {
        "hobby": random.choice(hobbies),
        "pet": random.choice(pets),
        "favorite_season": random.choice(["spring", "summer", "fall", "winter"]),
        "preferred_transport": random.choice(["car", "bike", "public_transport", "walking"])
    }

def sample_QA(facts):
    num_q = random.choice([2, 3])
    sampled = random.sample(question_bank, num_q)
    qa_list = []
    for q_template in sampled:
        q = q_template["question"].format(**facts)
        a = q_template["answer_fn"](facts)
        qa_list.append({"question": q, "answer": a})
    return qa_list

def generate_narrative():
    F = generate_atomic_facts()
    G = generate_diversity_facts()
    QA = sample_QA(F)

    return {
        "F": F,
        "G": G,
        "QA": QA
    }