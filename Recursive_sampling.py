from LLM import mistral_pipe, model, tokenizer
import re


def call_mistral(prompt, max_retries=2, retry_delay=2):
    """
    Call Mistral LLM and return raw text output.

    """
    import time

    for attempt in range(max_retries):
        try:
            # Calls LLM on the input prompt
            output = model.generate(
                **tokenizer(prompt, return_tensors="pt").to("cuda"),
                max_new_tokens=128,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
            )
            raw = tokenizer.decode(output[0], skip_special_tokens=True).strip()

            # Remove any junk before first number

            match = re.search(r'(\d+\.\s.+)', raw, re.DOTALL)
            if match:
                raw = match.group(1)

            return raw

        except Exception as e:
            print(f"[call_mistral] Error on attempt {attempt+1}: {e}")
            time.sleep(retry_delay)

    # Return empty string when failed
    return ""


def expand_node(node, facts, diversity, max_depth=3, depth=0, max_children=3):

    if depth >= max_depth:
        return node

    prompt = f"""
    You are a careful reasoning assistant.

    Question: "{node['statement']}"

    Facts (F): {facts}  
    Extra info (G): {diversity}

    Focus on reaching the conclusion by Build a reasoning trace to COMBINE multiple RELEVANT facts from (F)
    to reach higher order conclusions and answer root conclusion eventually.
    Focus on relevant facts only to answer the question.

    clearly show the reasoning, do not jump to conclusion without it

    Based on the combined facts and reasoning explain why your answer is correct

    Return ONLY the numbered reasoning steps, in order.
    """

    llm_output = call_mistral(prompt)
    if not llm_output:
        # If API fails, return the node as is
        return node

    # Extract numbered steps
    steps = re.findall(r'^\s*\d\.\s*(.+)', llm_output, re.MULTILINE)
    steps = [s.strip() for s in steps if s.strip()]

    node["children"] = []

    # Recurse for each step
    for step in steps[:max_children]:
        child_node = {"statement": step, "children": []}
        node["children"].append(
            expand_node(child_node, facts, diversity, max_depth, depth + 1, max_children)
        )

    return node