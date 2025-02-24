import asyncio
import os
import openai
import pandas as pd

client = openai.AsyncOpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
)


semaphore = asyncio.Semaphore(32)


async def make_request(prompt: str) -> str:
    async with semaphore:
        try:
            return await client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                n=10,
                temperature=1.0,
            )
        except Exception as e:
            print(f"Error with prompt {prompt}: {e}")
            return None


async def send_requests(prompts: list[str]) -> list[str]:
    results = [make_request(x) for x in prompts]
    return await asyncio.gather(*results)


def get_answers(x: str) -> int:
    return x

def process_responses(responses: list[openai.types.chat.chat_completion.ChatCompletion]) -> tuple[list[list[str]], list[list[str]]]:
    completions = [
        [choice.message.content for choice in response.choices]
        for response in responses
    ]
    answers = [
        [get_answers(choice.message.content) for choice in response.choices]
        for response in responses
    ]
    return completions, answers


async def main():
    df = pd.read_json(
        "data/arithmetic_20000ex_10000-1000000_5vals_plus.jsonl", lines=True
    )
    prompts = df["prompt"][:10]
    raw_responses = await send_requests(prompts)

    completions, answers = process_responses(raw_responses)
    import pdb; pdb.set_trace()
    for i, choice in enumerate(response.choices):
        print("=" * 8 + str(i) + "=" * 8)
        print(choice.message.content)
    print(row["completion"])


if __name__ == "__main__":
    asyncio.run(main())
