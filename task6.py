import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_ID = "HuggingFaceTB/SmolLM2-360M-Instruct"
INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
PASSWORD_LEN = 16  # Ровно 16 токенов = 16 символов пароля


def load_model():
    print(f"Загружается модель {MODEL_ID}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype="auto", # Как требует условие задачи
        device_map="auto",
    )
    model.eval()
    return tokenizer, model


def build_prompt(tokenizer: AutoTokenizer, passphrase: str) -> str:
    messages = [
        {
            "role": "user",
            "content": f"Just generate a continuation of the phrase: {passphrase}",
        }
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    return prompt


def recover_password(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    passphrase: str,
) -> str:
    # Генерируются ровно PASSWORD_LEN токенов и собираюся в строку. Поскольку каждый символ пароля = 1 токен, конкатенация токенов и есть пароль.
    prompt = build_prompt(tokenizer, passphrase)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    prompt_len = input_ids.shape[1]

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=PASSWORD_LEN,
            do_sample=False, # greedy - детерминированно
            temperature=1.0,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Берутся только новые токены (после промпта)
    new_tokens = output_ids[0, prompt_len: prompt_len + PASSWORD_LEN]
    # Декодируется каждый токен отдельно и склеивается
    password = "".join(
        tokenizer.decode([tok_id], skip_special_tokens=True)
        for tok_id in new_tokens
    )
    return password


def main():
    passphrases = Path(INPUT_FILE).read_text(encoding="utf-8").strip().splitlines()
    print(f"Паролей для восстановления: {len(passphrases)}")

    tokenizer, model = load_model()

    passwords = []
    for i, passphrase in enumerate(passphrases, 1):
        pwd = recover_password(tokenizer, model, passphrase)
        passwords.append(pwd)
        print(f"[{i:3d}/{len(passphrases)}] {passphrase!r:40s}  →  {pwd!r}")

    Path(OUTPUT_FILE).write_text("\n".join(passwords) + "\n", encoding="utf-8")
    print(f"\nПароли записаны в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()