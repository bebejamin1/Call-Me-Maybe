*This project has been created as part of the 42 curriculum by bbeaurai.*

# Call Me Maybe — Introduction to Function Calling in LLMs

## Preview

<img width="800" height="459" alt="preview_cmm" src="https://github.com/user-attachments/assets/a1b312b6-4916-4195-be70-e051915ad62a" />

## Output

```
[
  {
    "prompt": "What is the product of 3 and 5?",
    "name": "fn_multiply_numbers",
    "parameters": {
      "a": 3.0,
      "b": 5.0
    }
  },
  {
    "prompt": "What is the product of 12 and 4?",
    "name": "fn_multiply_numbers",
    "parameters": {
      "a": 12.0,
      "b": 4.0
    }
  },
  {
    "prompt": "Is 4 an even number?",
    "name": "fn_is_even",
    "parameters": {
      "n": 4
    }
  },
  {
    "prompt": "Is 7 an even number?",
    "name": "fn_is_even",
    "parameters": {
      "n": 7
    }
  },
  {
    "prompt": "Calculate compound interest on 1234567.89 at 0.0375 rate for 23 years",
    "name": "fn_calculate_compound_interest",
    "parameters": {
      "principal": 1234567.89,
      "rate": 0.0375,
      "years": 23
    }
  },
  {
    "prompt": "Execute SQL query 'SELECT * FROM users' on the production database",
    "name": "fn_execute_sql_query",
    "parameters": {
      "query": "SELECT * FROM users",
      "database": "production"
    }
  },
  {
    "prompt": "Run the query 'INSERT INTO logs VALUES (1, 2, 3)' on the system database",
    "name": "fn_execute_sql_query",
    "parameters": {
      "query": "INSERT INTO logs VALUES (1, 2, 3)",
      "database": "system"
    }
  },
  {
    "prompt": "Read the file at /home/user/data.json with utf-8 encoding",
    "name": "fn_read_file",
    "parameters": {
      "path": "/home/user/data.json",
      "encoding": "utf-8"
    }
  },
  {
    "prompt": "Read C:\\Users\\john\\config.ini with latin-1 encoding",
    "name": "fn_read_file",
    "parameters": {
      "path": "C:\\Users\\john\\config.ini",
      "encoding": "latin-1"
    }
  },
  {
    "prompt": "Format template: Hello {user}'s profile!",
    "name": "no function was found",
    "parameters": {}
  },
  {
    "prompt": "Format template: Say \"hello\" to {name}",
    "name": "fn_format_template",
    "parameters": {
      "template": "Say \"hello\" to {name}"
    }
  }
]
```


## Description

**Call Me Maybe** is a function calling tool that translates natural language prompts
into structured function calls using a small language model (Qwen3-0.6B).

Given a prompt like *"What is the sum of 2 and 3?"*, the system does not answer
the question directly. Instead, it identifies the correct function to call and extracts
its typed arguments:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {"a": 2.0, "b": 3.0}
}
```

The key challenge is reliability: small models fail to produce valid JSON roughly 70%
of the time when prompted naively. This project solves that using **constrained
decoding** — a technique that restricts the model's token choices at each generation
step to guarantee 100% structurally valid output.

---

## Instructions

### Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- The `llm_sdk/` directory must be present at the project root (provided separately)

### Installation

```bash
uv sync
```

This installs all dependencies including `numpy`, `pydantic`, and `llm_sdk`.

### Running

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

All arguments are optional. Defaults:
- `--functions_definition` → `data/input/functions_definition.json`
- `--input` → `data/input/function_calling_tests.json`
- `--output` → `data/output/function_calling_results.json`

### Makefile targets

| Target | Description |
|--------|-------------|
| `make` / `make run` | Install dependencies and run the program |
| `make install` | Install dependencies only |
| `make debug` | Run with Python's `pdb` debugger |
| `make lint` | Run `flake8` and `mypy` |
| `make lint-strict` | Run `mypy --strict` |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |

---

## Algorithm Explanation

### Constrained Decoding

The generation loop works as follows at each step:

1. The current token sequence (prompt + generated tokens so far) is fed to the LLM.
2. The model returns **logits** — a score for every token in the vocabulary (~150k tokens).
3. The constrained decoder determines which tokens are **valid continuations** given:
   - The current JSON structure state (e.g., inside a string value, expecting a number…)
   - The schema of the function being generated (argument types from `functions_definition.json`)
4. All **invalid tokens** have their logits set to `-inf`.
5. The token with the highest remaining logit is selected (greedy decoding).
6. The selected token is appended and the loop repeats until the JSON object is complete.

### Two-Phase Generation

The generation is split into two phases:

**Phase 1 — Function selection:** The LLM is prompted to pick the function name from
the available list. The vocabulary file maps token IDs to their string representations,
allowing the decoder to restrict valid tokens to exactly those that spell out one of the
known function names.

**Phase 2 — Argument generation:** For each parameter defined in the function's schema,
the decoder enforces the declared type:
- `"number"` / `"integer"` → only tokens that form valid numeric literals are allowed
- `"string"` → tokens forming valid JSON string content
- `"boolean"` → restricted to `true` or `false`

The vocabulary JSON file (obtained via `get_path_to_vocab_file()`) is loaded once at
startup and used throughout to map token IDs to their string values.

---

## Design Decisions

- **No external constrained-decoding libraries** (`outlines`, `lm-format-enforcer`, etc.)
  are used — the constraint logic is implemented from scratch using only `numpy` and
  the `llm_sdk` API, as required by the subject.
- **Pydantic** is used for all data classes (`FunctionDef`) to validate function
  definitions at load time and catch malformed inputs early.
- **Greedy decoding** is used rather than sampling: given the structural constraints
  already guarantee validity, taking the argmax at each step maximises semantic
  accuracy without introducing randomness.
- **Graceful error handling** throughout: invalid JSON input files, missing files, and
  malformed function definitions all produce clear error messages and a clean exit
  rather than tracebacks.

---

## Performance Analysis

| Metric | Result |
|--------|--------|
| JSON validity | 100% — every output is parseable |
| Function selection accuracy | ~90%+ on provided test set |
| Argument extraction accuracy | ~90%+ on provided test set |
| Speed | < 5 minutes for the full test set on standard hardware |

The constrained decoder is the primary reason the 0.6B model achieves results
comparable to much larger models: structural correctness is no longer a matter of
the model's probability distribution but a hard guarantee.

---

## Challenges Faced

**Vocabulary mapping:** The Qwen3 tokenizer uses a BPE vocabulary where tokens can
span multiple characters, include leading spaces, or represent partial words. Building
a correct prefix-based token filter required careful handling of token boundaries to
avoid rejecting valid continuations prematurely.

**Type enforcement for numbers:** Numeric tokens in BPE vocabularies are fragmented
(e.g., `"12"`, `"3"`, `".4"` are separate tokens). The constraint logic must allow
any prefix of a valid number (integers and floats) while still rejecting non-numeric
tokens.

**String argument extraction:** User prompts sometimes contain special characters,
quotes, or Unicode. The JSON string constraint must allow all valid JSON string
content while still rejecting unescaped control characters and premature closing quotes.

**Python 3.10 compatibility:** f-strings with same-quote characters inside expressions
(`f"{d["key"]}"`) are valid only in Python 3.12+. All such occurrences have been
rewritten using alternate quote styles to ensure compatibility with Python 3.10.

---

## Testing Strategy

- **Manual runs** against the provided `function_calling_tests.json` with visual
  inspection of the output file.
- **Edge cases tested:** empty strings, very large numbers, special characters in
  string arguments, prompts that match no function, prompts that are ambiguous.
- **JSON validity** verified by parsing the output file with `json.load()` after
  each run.
- **Schema compliance** verified by cross-referencing output parameter types against
  the function definitions.
- **Error handling** tested by providing: missing input files, empty JSON arrays,
  malformed JSON, function definitions with missing fields.

---

## Example Usage

### Basic run (default paths)

```bash
uv run python -m src
```

### Custom paths

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Example output (`data/output/function_calling_results.json`)

```json
[
  {
    "prompt": "What is the product of 3 and 5?",
    "name": "fn_multiply_numbers",
    "parameters": {"a": 3.0, "b": 5.0}
  },
  {
    "prompt": "Is 4 an even number?",
    "name": "fn_is_even",
    "parameters": {"n": 4}
  },
  {
    "prompt": "Read the file at /home/user/data.json with utf-8 encoding",
    "name": "fn_read_file",
    "parameters": {"path": "/home/user/data.json", "encoding": "utf-8"}
  }
]
```

---

## Resources

### References

- [Attention Is All You Need — Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762)
- [Outlines: Efficient Guided Generation (Brandon T. Willard, Rémi Louf)](https://arxiv.org/abs/2307.09702)
- [Byte Pair Encoding — Sennrich et al. (2016)](https://arxiv.org/abs/1508.07909)
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)
- [JSON specification — ECMA-404](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [Pydantic documentation](https://docs.pydantic.dev/)

### AI Usage

AI (Claude) was used in this project for the following tasks:

- **Debugging:** identifying Python 3.10 compatibility issues with f-string syntax
  and suggesting fixes.
- **Code review:** checking that the project structure matched the subject's
  requirements (CLI arguments, output format, error handling).
- **README drafting:** the initial structure and phrasing of this document was
  produced with AI assistance and then reviewed and corrected.

All code was written and understood by the author. AI-generated suggestions were
critically reviewed before being integrated.
