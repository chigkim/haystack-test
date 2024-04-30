from time import time
start = time()
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="Model name, default=llama3", default="llama3")
parser.add_argument("--host", help="Ollama Host Address, default=localhost:11434", default='http://localhost:11434')
parser.add_argument("-f", "--file", help="Text file for context, default=text.txt", default="text.txt")
parser.add_argument("-s", "--secret", help="Text file for secrets, default=secrets.txt", default="secrets.txt")
parser.add_argument("-c", "--context", help="Max Context Size, default=8192", type=int, default=8192)
parser.add_argument("-t", "--tests", help="Number of Tests, default=100", type=int, default=100)
args = parser.parse_args()

options={'temperature':0.0, 'num_ctx':args.context, 'num_predict':-1}
system = 'You are a helpful assistant.'
start_prompt = 'Somewhere in the text below, there is a secret phrase I need to locate.\n---Text begins, start searching!\n'
end_prompt = '\n---Text ends, stop searching!\nWhat is the secret phrase?'

from ollama import Client
import codecs
import random

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
	secret = random.choice(secrets)
	hide = f'\nThe secret phrase is: "{secret}"\n'
	prompt = list(words)
	random.shuffle(prompt)
	if position<length:
		prompt = prompt[:position] + [hide] + prompt[position:]
	else:
		print("Running the last bonus test with no secret inserted. It should fail, and it doesn't count toward the final score.")
	prompt = start_prompt+" ".join(prompt)+end_prompt
	if eval(prompt, secret):
		score += 1
		print(f'Passed test {i+1}/{args.tests}, Position {position}/{length}')
	else:
		print(f'Failed test {i+1}/{args.tests}, Position {position}/{length}')
	if position<length:
		print(f'Score: {score}/{i+1}, {score/(i+1)*100.0:.2f}%')

print(f'Final Score: {score}/{args.tests}, {score/args.tests*100.0:.2f}%')
print(f"Finished in {time()-start:.2f} seconds.")