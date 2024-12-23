import pandas as pd
import numpy as np
from pathlib import Path


def main(
    output_dir: str = "data",
    num_examples: int = 20_000,
    min_value: int = 1_000,
    max_value: int = 10_000,
    num_values: int = 2,
    operations: list[str] = ["+"],
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
    df.to_json(output_path, orient="records", lines=True)


if __name__ == "__main__":
    from strictfire import StrictFire
    StrictFire(main)
