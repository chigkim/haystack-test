from time import time
start = time()
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="Model name, default=llama3", default="llama3")
parser.add_argument("--host", help="Ollama Host Address, default=localhost:11434", default='http://localhost:11434')
parser.add_argument("-f", "--file", help="Text file for context, default=text.txt", default="text.txt")
parser.add_argument("-s", "--secret", help="Text file for secrets, default=secrets.txt", default="secrets.txt")
parser.add_argument("-c", "--context", help="Max Context Size, default=8192", type=int, default=8192)
parser.add_argument("-p", "--predict", help="Max number of tokens to predict, default=300", type=int, default=300)
parser.add_argument("-t", "--tests", help="Number of Tests, default=100", type=int, default=100)
parser.add_argument("-n", "--needles", help="Number of needles, default=3", type=int, default=3)
args = parser.parse_args()

options={'temperature':0.0, 'num_ctx':args.context, 'num_predict':args.predict}
system = 'You are a helpful assistant.'
start_prompt = 'Identify and assemble the secret sentence from the numbered fragments hidden in the text below.\n---Text begins here, start your search now!\n'
end_prompt = '\n---Text ends here, stop your search.\nPlease arrange the secret fragments you located in numerical order to construct the full secret sentence. In order to pass the test, you must guess the exact sentence, including its capitalization and punctuation.\nWhat is the complete secret sentence?'

from ollama import Client
import codecs
import random
import re

def eval(prompt, secret):
	messages = [{'role': 'system', 'content': system}]
	messages.append({'role': 'user', 'content': prompt})
	response = client.chat(model=args.model, messages=messages, options=options)
	div = 1000000000
	total = response['total_duration']/div
	load = response['load_duration']/div
	prompt_count = response['prompt_eval_count'] if 'prompt_eval_count' in response else 0
	prompt_duration = response['prompt_eval_duration']/div
	gen_count = response['eval_count']
	gen_duration = response['eval_duration']/div
	stat = f"Total: {total:.2f} secs, Load: {load:.2f} secs, Prompt Processing: {prompt_count} tokens, {prompt_count/prompt_duration:.2f} tk/s, Text Generation: {gen_count} tokens, {gen_count/gen_duration:.2f} tk/s"
	print(stat)
	print(response['message']['content'].strip())
	return secret in response['message']['content']

def fragment(secret, n):
	# Split the phrase into n fragments.
	print("Secret:", secret)
	secrets = secret.split(" ")
	length = len(secrets)
	if n>length:
		n = length
	fragments = []
	step = int(length/n)
	steps = range(0,length, step)
	steps = steps[:n]
	for i, pos in enumerate(steps):
		fragment = ""
		if i+1 == n:
			fragment = " ".join(secrets[pos:])
		else:
			fragment = " ".join(secrets[pos:pos+step])
		fragment = f'\nSecret fragment {i+1}: "{fragment}"\n'
		fragments.append(fragment)
	return fragments

def shuffle(prompt, secret):
	# Make sure the fragments never appear in order.
	r = r'Secret fragment \d+: \"(.*?)\"'
	while True:
		random.shuffle(prompt)
		fragments = [re.search(r, f)[1] for f in prompt if re.search(r, f)]
		if " ".join(fragments) != secret: break

	positions = [f"{w.strip()[16:]} at {p}" for p, w in enumerate(prompt) if "Secret fragment " in w]
	positions = ", ".join(positions)
	print("Inserted", positions)
	return prompt

secrets = codecs.open(args.secret, 'r', 'utf-8').readlines()
secrets = [phrase.strip() for phrase in secrets]
client = Client(host=args.host)
text = codecs.open(args.file, 'r', 'utf-8').read()
words = text.split(" ")
score = 0
length = len(words)
step = int(length/args.tests)
steps = list(range(0, length, step))
steps = steps[:args.tests]
steps.append(length)
print("Testing "+args.model)
for i, position in enumerate(steps):
	prompt = list(words)
	if position<length:
		secret = random.choice(secrets)
		hide = fragment(secret, args.needles)
		prompt = prompt[:position] + hide + prompt[position:]
		prompt = shuffle(prompt, secret)
	else:
		print("Running the last bonus test with no secret inserted. It should fail, and it doesn't count toward the final score.")
	prompt = start_prompt+" ".join(prompt)+end_prompt
	if eval(prompt, secret):
		score += 1
		print(f'Passed test {i+1}/{args.tests}')
	else:
		print(f'Failed test {i+1}/{args.tests}')
	if position<length:
		print(f'Score: {score}/{i+1}, {score/(i+1)*100.0:.2f}%')

print(f'Final Score: {score}/{args.tests}, {score/args.tests*100.0:.2f}%')
print(f"Finished in {time()-start:.2f} seconds.")