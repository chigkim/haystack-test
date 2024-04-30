# haystack-test

Fun, Pseudo needle in a haystack test for Ollama.

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

In order to pass a test, the model has to output the exact phrase including capitalization and punctuation.