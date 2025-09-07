# Tax Case Generator

Generates synthetic tax cases with reasoning traces for LLM evaluation, based on MuSR paper methodology.

Creates realistic but fake tax scenarios with step-by-step reasoning, narratives, and Q&A pairs for training AI models.

## Quick Start

```bash
# Install dependencies
pip install torch transformers accelerate huggingface_hub numpy bitsandbytes

```

The script will prompt for:
- Number of cases to generate
- Output file location

## Output Format

Each case includes:
- **Facts**: atomic facts about income tax payer, age, marital status etc.
- **Reasoning Trace**: Recursive combination of atomic facts to arrive at higher order conclusions
- **Narrative**: Story from taxpayer perspective  
- **Q&A**: Common questions and answers

## Customization
- Modify the rules in atomic fact generation to be in accordance with real laws
- Add new seed files with domain specific rules and atomic facts to generate the narratives


