def generate_QA(facts, reasoning):
    """
    Generate questions and answers from facts and reasoning tree
    for MuSR-style evaluation.
    """
    questions = []
    answers = []

    # Basic income and deduction questions
    questions.append("What is the taxpayer's gross income?")
    answers.append(reasoning['gross_income'])

    questions.append("What is the total deduction amount?")
    answers.append(reasoning['deductions_total'])

    questions.append("What is the taxable income?")
    answers.append(reasoning['taxable_income'])

    questions.append("What is the base tax liability?")
    answers.append(reasoning['base_tax'])

    questions.append("What is the total tax liability including penalties?")
    answers.append(reasoning['total_liability'])

    # Filing behavior questions
    questions.append("What is the taxpayer's filing status?")
    answers.append(facts['filing_status'])

    questions.append("Was the taxpayer's return filed on time?")
    answers.append(facts['filed_on_time'])

    questions.append("Was the taxpayer audited?")
    answers.append(facts['audited'])

    questions.append("Did the taxpayer incur any penalties?")
    answers.append(facts['penalties'])

    # Optional: Church tax question
    questions.append("Did the taxpayer pay church tax?")
    answers.append(facts['church_tax'])

    # Optional: Age-related question
    questions.append("Is the taxpayer over 65 years old?")
    answers.append('Yes' if facts['age'] == '>=65' else 'No')

    return questions, answers

