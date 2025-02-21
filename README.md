# Python benchmarking task

## Test cases generation
- Given a problem statement, generate test cases and then test models on it.
- Used claude sonnet to generate deterministic functions for generating test cases on demand.
- refer to [instructions.txt](instructions.txt) for test case generation.

## Benchmarking
- Models tested: deepseek-r1, llama405b, openai-o3, gemini-2.0-flash
- Function defs expected in testing code were supplied along with the question. Check [def_analysis](def_analysis.py)
- the first three were accessed directly from together.ai: [benchmark](benchmark.py)
- google has a different api: [benchmark_google](benchmark_google.py)
- r1 ended up returning a lot of discussion around the problem, even after explicitly mentioning to return code between `<code>` and `</code>`.
- use [utils](utils.py) for sanity checking the packaged code, extracting code and running tests.

## Results
Results are compiled in this [spreadsheet](https://docs.google.com/spreadsheets/d/1juERsHvCsjG1WwbmINwIBRjMgyenjj_b2BqlzRarhIU/edit?usp=sharing).