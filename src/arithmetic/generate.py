import pandas as pd
import numpy as np
from pathlib import Path


# PROMPT_TEMPLATE.format(expression=)
PROMPT_TEMPLATE = "<BOS_TOKEN><|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|># System Preamble\nYou are in contextual safety mode. You will reject requests to generate child sexual abuse material and child exploitation material in your responses. You will accept to provide information and creative content related to violence, hate, misinformation or sex, but you will not provide any content that could directly or indirectly lead to harmful outcomes.\n\nYour information cutoff date is June 2024.\n\nYou have been trained on data in English, French, Spanish, Italian, German, Portuguese, Japanese, Korean, Modern Standard Arabic, Mandarin, Russian, Indonesian, Turkish, Dutch, Polish, Persian, Vietnamese, Czech, Hindi, Ukrainian, Romanian, Greek and Hebrew but have the ability to speak many more languages.\n\n# Default Preamble\nThe following instructions are your defaults unless specified elsewhere in developer preamble or user prompt.\n- Your name is Command.\n- You are a large language model built by Cohere.\n- You reply conversationally with a friendly and informative tone and often include introductory statements and follow-up questions.\n- If the input is ambiguous, ask clarifying follow-up questions.\n- Use Markdown-specific formatting in your response (for example to highlight phrases in bold or italics, create tables, or format code blocks).\n- Use LaTeX to generate mathematical notation for complex equations.\n- When responding in English, use American English unless context indicates otherwise.\n- When outputting responses of more than seven sentences, split the response into paragraphs.\n- Prefer the active voice.\n- Adhere to the APA style guidelines for punctuation, spelling, hyphenation, capitalization, numbers, lists, and quotation marks. Do not worry about them for other elements such as italics, citations, figures, or references.\n- Use gender-neutral pronouns for unspecified persons.\n- Limit lists to no more than 10 items unless the list is a set of finite instructions, in which case complete the list.\n- Use the third person when asked to write a summary.\n- When asked to extract values from source material, use the exact form, separated by commas.\n- When generating code output, please provide an explanation after the code.\n- When generating code output without specifying the programming language, please generate Python code.\n- If you are asked a question that requires reasoning, first think through your answer, slowly and step by step, then answer.<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|USER_TOKEN|>{expression}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"

# COMPLETION3_TEMPLATE.format(value1=, value2=, value3=, sum=)
COMPLETION3_TEMPLATE = "The sum of {value1}, {value2}, and {value3} is {sum}.<|END_OF_TURN_TOKEN|>"


def generate_data(
    num_examples: int = 20_000,
    min_value: int = 1_000,
    max_value: int = 10_000,
    num_values: int = 2,
    operations: list[str] = ["+"],
):
    problems = []
    solutions = []
    
    for _ in range(num_examples):
        # Generate random numbers
        values = np.random.randint(min_value, max_value, size=num_values)
        
        # Choose random operation for each pair
        ops = np.random.choice(operations, size=num_values-1)
        
        # Build the problem string and compute solution
        problem = str(values[0])
        result = values[0]
        
        for i, (op, val) in enumerate(zip(ops, values[1:])):
            problem += f" {op} {val}"
            if op == "+":
                result += val
            elif op == "-":
                result -= val
            elif op == "*":
                result *= val
            elif op == "/":
                result /= val
                
        problems.append(problem)
        solutions.append(str(result))
    
    df = pd.DataFrame({
        "prompt": problems,
        "completion": solutions
    })

    return df


def promptify(df):
    # Inner function to update each row based on the templates
    def update_row(row):
        # Extract the numbers from the expression in the 'prompt'
        numbers = [int(num) for num in row['prompt'].split(' + ')]
        
        # Format the prompt using the template
        row['prompt'] = PROMPT_TEMPLATE.format(expression=row['prompt'])
        
        # Format the completion using the template
        row['completion'] = COMPLETION3_TEMPLATE.format(value1=numbers[0], value2=numbers[1], value3=numbers[2], sum=row["completion"])
        
        return row

    # Apply the update_row function to each row of the DataFrame
    df = df.apply(update_row, axis=1)
    return df


def main(
    output_dir: str = "data",
    num_examples: int = 20_000,
    min_value: int = 1_000,
    max_value: int = 10_000,
    num_values: int = 2,
    operations: list[str] = ["+"],
    do_generate: bool = True,
    do_promptify: bool = True,
) -> pd.DataFrame:
    """Generate arithmetic problems with their solutions.
    
    Args:
        num_examples: Number of problems to generate
        min_value: Minimum value for random numbers
        max_value: Maximum value for random numbers
        num_values: Number of values in each problem
        operations: List of operations to use (+, -, *, /)
        
    Returns:
        DataFrame with problems and solutions
    """
    
    # Ensure output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Construct filename from parameters
    op_names = {
        "+": "plus",
        "-": "minus",
        "*": "times",
        "/": "divide"
    }
    ops_str = '_'.join(op_names[op] for op in sorted(operations))
    filename = f"arithmetic_{num_examples}ex_{min_value}-{max_value}_{num_values}vals_{ops_str}.jsonl"
    # Construct full output path
    output_path = output_dir / filename

    if do_generate:
        df = generate_data(num_examples=num_examples, min_value=min_value, max_value=max_value, num_values=num_values, operations=operations)
        df.to_json(output_path, orient="records", lines=True)
        print("Saved data to {output_path}")

    if do_promptify:
        df = pd.read_json(output_path, orient="records", lines=True)
        prompt_df = promptify(df)

        promptname = f"arithmetic_{num_examples}ex_{min_value}-{max_value}_{num_values}vals_{ops_str}.prompt.jsonl"
        prompt_path = output_dir / promptname

        prompt_df.to_json(prompt_path, orient="records", lines=True)
        print("Saved prompt data to {prompt_path}")


if __name__ == "__main__":
    from strictfire import StrictFire
    StrictFire(main)
