# Tax Case Data Generator

This project creates fake but realistic tax cases for training AI models. I built it to solve the challenge of getting enough diverse tax scenarios to train language models on tax reasoning.

## What it does

Takes random taxpayer info → runs it through tax calculations → creates a story about it → generates Q&A pairs

The idea is that AI models need lots of examples to learn from, but real tax data is private. So this generates synthetic cases that look real but aren't tied to actual people.

## How to use it

```bash
python main.py
```

It'll ask how many cases you want and where to save them. Each case gets saved as JSON with all the details.

## What's in each case

- **Facts**: Random but realistic taxpayer info (income, filing status, etc.)
- **Calculations**: Step-by-step tax math following real rules
- **Story**: A short narrative written from the taxpayer's perspective  
- **Q&A**: Questions the person might ask and appropriate answers

## Files breakdown

- `Facts.py` - Defines what kind of taxpayer info we generate
- `Reasoning_Tree.py` - The tax calculation logic
- `main.py` - Puts it all together and saves the data
- `questions_and_answers.py` - Makes Q&A pairs (not shown in code sample)

## Key design choices

**Why a reasoning tree?** Tax calculations have clear steps - gross income, deductions, tax brackets, penalties. I coded these as separate steps so it's easy to see the logic and modify individual parts.

**Why synthetic data?** Real tax data is sensitive. This generates unlimited examples without privacy issues.

**Why include narratives?** Raw numbers are boring. The stories make it feel like real cases, which helps when training conversational AI.

## Making changes

To include different tax scenarios,  Edit the schema in `Facts.py`:

```python
facts_schema = {
    'filing_status': ['single', 'married_joint', 'business'],
    'new_thing': ['option1', 'option2']
}
```

To include more realstic tax calculations, Update the calculations in `Reasoning_Tree.py`. Each step is separate so you can modify just what you need.

## Technical stuff

Uses Mistral-7B for generating the narratives. Runs in 4-bit mode to save memory.

The tax calculations are simplified but follow real principles - progressive brackets, standard deductions, common penalties.

## Installation

```
pip install torch transformers accelerate huggingface_hub numpy -U bitsandbytes
```

You'll need to login to HuggingFace and agree to the model library rules when you first run it.

## Example output

```json
{
  "facts": {
    "filing_status": "single",
    "employment_income": 75000,
    "deductions": 8500
  },
  "reasoning_tree": {
    "gross_income": 75000,
    "taxable_income": 66500,
    "total_liability": 9800
  },
  "narrative": "I'm filing as single for 2024. Made $75k from my job...",
  "questions": ["How much do I owe?", "Any way to reduce this?"]
}
```
