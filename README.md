# haystack-test

Fun, Pseudo needle in a haystack test for Ollama.

## Instruction

After installing [Ollama](https://ollama.com/download) and [downloading a model](https://ollama.com/library) to test, you can execute the following commands to install Ollama python and run 100 tests for 8192 context size.

```bash
pip install ollama
python3 haystack-multi.py -m llama3 -f text.txt -s secrets.txt -c 8192 -t 100
```

Make sure to leave about 500 tokens as a buffer in order to fit the prompt, secrets, and response from model. For example, if your context size is 8192, your text should be 7692 tokens or less.

```bash
python haystack-single.py -h

usage: haystack-single.py [-h] [-m MODEL] [--host HOST] [-f FILE] [-s SECRET] [-c CONTEXT] [-t TESTS]

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

This is what the script does when you run the test.

* Read `secrets.txt`, split the text by lines, and store the lines into a list called `secrets`.
* Read `text.txt`, split the text by words, and store the words into a list called `words`.
* Before each test, shuffle the `words` list.
* Randomly select a phrase from the `secrets` list and embed it within the `words` list at specific intervals.
* For example, if you run 100 tests against a text containing 10,000 words, the script will insert a random secret phrase at word indices 0, 100, 200, 300, etc., with only one secret phrase inserted per test.
* Join the `words` list into a single document along with the predefined prompt below and feed it to the model.

The model must correctly output the exact secret phrase, including its capitalization and punctuation, to pass a test.

## Prompt for Single Needle

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

## Prompt for Multie Needle

```
Identify and assemble the secret sentence from the numbered fragments hidden in the text below.
---Text begins here, start your search now!
...text...
Secret fragment 3: "on my shoulder."
...text...
Secret fragment 1: "The soft, fluffy"
...text...
Secret fragment 2: "kitten purred loudly"
...text...
---Text ends here, stop your search.
Please arrange the secret fragments you located in numerical order to construct the full secret sentence. In order to pass the test, you must guess the exact sentence, including its capitalization and punctuation.
What is the complete secret sentence?
```

## Result

Here are the results after running 100 tests for each model below:

| Model | Input Context Length | Single Needle | Multi Needle |
| --- | --- | --- | --- |
| llama3:8b-instruct-q8_0 | 8K | 94% | 44% |
| llama3:70b-instruct-q8_0 | 8K | No Test | 100% |
| llama3-gradient:8b-instruct-1048k-q8_0 | 32K | 100% | 33% |
| dolphin-llama3:8b-256k-v2.9-q8_0 | 8K | 75% | 2% |

Here's the [log](https://gist.github.com/chigkim/e047b83755df46548f69454973f1b81f) for the full output.