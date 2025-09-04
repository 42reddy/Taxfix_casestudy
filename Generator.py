from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GenerationConfig
from Facts import generate_facts
from Reasoning_Tree import reasoning_tree
from questions_and_answers import generate_QA
import torch
import json
from huggingface_hub import notebook_login
notebook_login()

model_id = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)

# Load model in 4-bit or 8-bit using bitsandbytes quantization
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_4bit=True,      # use load_in_8bit=True for 8-bit
    torch_dtype=torch.float16,
    trust_remote_code=True
)


def generate_narrative(facts, reasoning, max_length=500, temperature=0.5):
    """
    Generate a short tax case narrative from facts and reasoning.
    """
    # Build the prompt with natural-language storytelling
    prompt = f"""
    Imagine you are a tax expert writing a short case report about an individual filing taxes, 
    the following are the details about the same, use them to narrate the case from the first person point of view, i.e, the individual. 
    Create a 5-7 sentence story describing a taxpayer based on these facts:

    Filing status: {facts['filing_status']}
    Year: {facts['year']}
    Age: {facts['age']}
    Filed on time: {facts['filed_on_time']}
    Employment income: {facts['employment_income']}
    Business income: {facts['business_income']}
    Capital gains: {facts['capital_gains']}
    Foreign income: {facts['foreign_income']}
    Deductions: {facts['deductions']}
    Medical expenses: {facts['medical_expenses']}
    Church tax: {facts['church_tax']}
    Penalties: {facts['penalties']}
    Audited: {facts['audited']}
    
    Include these computed values by a tax accountant:
    gross income: {reasoning['gross_income']}, 
    total deductions: {reasoning['deductions_total']}, 
    taxable income: {reasoning['taxable_income']}, 
    base tax: {reasoning['base_tax']}, 
    penalties: {reasoning['penalty_amount']}, 
    total liability: {reasoning['total_liability']}. 

    End with a generic question as if the person is asking the expert help in filing or reducing their taxes,
    Make it sound natural, like a real-world case.
    """

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    generation_config = GenerationConfig(
        max_new_tokens=max_length,
        temperature=temperature,
        do_sample=True,
        top_p=0.9
    )

    outputs = model.generate(**inputs, **generation_config.to_dict())
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Optionally remove the prompt from output
    return text[len(prompt):].strip()





# Generates a single sample data object
def generate_tax_case():
    facts = generate_facts()
    reasoning = reasoning_tree(facts)
    narrative = generate_narrative(facts, reasoning)
    questions, answers = generate_QA(facts, reasoning)
    return {
        "F": facts,
        "reasoning_tree": reasoning,
        "narrative": narrative,
        "questions": questions,
        "answers": answers
    }



# Generate a Dataset
def generate_dataset(n_cases=100, save_path="tax_cases.json"):
    dataset = []
    for _ in range(n_cases):
        case = generate_tax_case()
        dataset.append(case)

    # Save to JSON
    with open(save_path, "w") as f:
        json.dump(dataset, f, indent=4)
    print(f"{n_cases} cases saved to {save_path}")

# Example usage
if __name__ == "__main__":
    n_cases = int(input("Enter number of tax cases to generate: "))
    save_path = input("Enter filename to save the dataset: ")
    generate_dataset(n_cases, save_path)


