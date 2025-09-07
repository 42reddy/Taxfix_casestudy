from transformers import GenerationConfig
from Recursive_sampling import expand_node
from atomic_facts import generate_narrative
from LLM import tokenizer, model


narrative = generate_narrative()
facts = narrative['F']
diversity = narrative['G']

# Sample a question and answer
qa_entry = narrative['QA'][0]
statement = f"{qa_entry['question']} Answer: {qa_entry['answer']}"

# Root node
root_node = {
    "statement": statement,
    "children": []
}



def flatten_tree(node, label="Deduced Root Conclusion", depth=0):
    """
    Converts recursive reasoning tree into the 'flattened path with labels' format.
    """
    indent = " > " * depth
    output = f"{indent}{node['statement']} | {label}"

    lines = [output]

    for child in node.get("children", []):
        # decide labels based on the content or depth
        if depth == 0:
            child_label = "Deduced Fact"
        elif "commonsense" in child.get("statement", "").lower():
            child_label = "Commonsense Knowledge"
        else:
            child_label = "Fact From Story"

        lines.extend(flatten_tree(child, label=child_label, depth=depth + 1))

    return lines




def generate_story(facts, max_length=500, temperature=0.7):
    """
    Generate a short tax case narrative from facts and reasoning.
    """
    # Convert facts dict to readable lines
    facts_text = "\n".join([f"- {k}: {v}" for k, v in facts.items()])

    # Build prompt with concrete facts + reasoning
    prompt = f"""
    Imagine you are a taxpayer writing a short personal tax narrative about yourself. 
    Use the following facts and reasoning to tell the story from a first-person point of view:

    Facts:
    {facts_text}

    Write a 5-7 sentence narrative describing your tax situation naturally and realistically, 
    including details such as your filing status, income, deductions, and any challenges. 
    End with a question asking an expert for advice on filing or maximizing deductions.
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

    # Remove the prompt from output
    return text[len(prompt):].strip()



def run_single_case(max_depth=4, max_children=2, story_length=500, temperature=0.7):
    """
    Run the full pipeline for a single narrative.
    Returns a data object with facts, reasoning tree, story, and QA.
    """

    # Generate facts, diversity, and QA
    narrative = generate_narrative()
    facts = narrative['F']
    diversity = narrative['G']
    qa_list = narrative['QA']

    # Pick one QA for reasoning tree
    qa_entry = qa_list[0]
    statement = f"{qa_entry['question']} Answer: {qa_entry['answer']}"
    root_node = {"statement": statement, "children": []}

    # Build reasoning tree
    reasoning_tree = expand_node(root_node, facts, diversity,
                                 max_depth=max_depth, depth=0, max_children=max_children)

    # Generate first person narrative
    story = generate_story(facts, story_length, temperature)

    # Return as a structured data object
    return {
        "facts": facts,
        "diversity": diversity,
        "reasoning_tree": reasoning_tree,
        "story": story,
        "qa": qa_list
    }


def run_batch_cases(n_cases=5):

    all_cases = []
    for _ in range(n_cases):
        case_data = run_single_case()
        all_cases.append(case_data)
    return all_cases


# Example usage: generate 3 cases
tax_cases = run_batch_cases(n_cases=3)

