# haystack-test

Fun, Pseudo needle in a haystack test for Ollama.

## Instruction

* Make sure you have Ollama installed, and downloaded a model to test.
* Install ollama python library: pip install ollama
* Run python haystack.py

```bash
python haystack.py -h

usage: haystack.py [-h] [-m MODEL] [--host HOST] [-f FILE] [-s SECRET] [-c CONTEXT] [-t TESTS]

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Model name, default=llama3
  --host HOST           Ollama Host Address, default=localhost:11434
  -f FILE, --file FILE  Text file for context, default=text.txt
  -s SECRET, --secret SECRET
                        Text file for secrets, default=secrets.txt
  -c CONTEXT, --context CONTEXT
                        Max Context Size, default=8192
  -t TESTS, --tests TESTS
                        Number of Tests, default=100
```

## Process

* Read `secrets.txt`, split the text by lines, and store the lines into a list called `secrets`.
* Read `text.txt`, split the text by words, and store the words into a list called `words`.
* Before each test, shuffle the `words` list.
* Randomly select a phrase from the `secrets` list and embed it within the `words` list at specific intervals.
* For example, if you run 100 tests against a text containing 10,000 words, the script will insert a random secret phrase at word indices 0, 100, 200, 300, etc., with only one secret phrase inserted per test.
* Join the `words` list into a single document along with a predefined prompt and feed it to the model.

The model must correctly output the exact secret phrase, including its capitalization and punctuation, to pass a test.

## Prompt

```
System: You are a helpful assistant.
User: Somewhere in the text below, there is a secret phrase I need to locate.
---Text begins, start searching!
...text...
The secret phrase is: "The little red hen laid the golden eggs"
...text...
---Text ends, stop searching!
What is the secret phrase?
```