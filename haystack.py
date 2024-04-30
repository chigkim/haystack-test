# Host address where Ollama is listening
host='http://localhost:11434'
# model name to test
model = "llama3:8b-instruct-q8_0"
# File name to read text to use for hiding secrets
file = "text.txt"
# Number of tests to run
tests = 100
# Generation parameters for Ollama. Change the num_ctx according to the model.
options={'temperature':0.0, 'num_ctx':8192, 'num_predict':-1}
system = 'You are a helpful assistant.'
start_prompt = 'Somewhere in the text below, there is a secret phrase I need to locate.\n---Text begins, start searching!\n'
end_prompt = '\n---Text ends, stop searching!\nWhat is the secret phrase?'

from time import time
start = time()
from ollama import Client
import codecs
import random

def eval(prompt, secret):
	messages = [{'role': 'system', 'content': system}]
	messages.append({'role': 'user', 'content': prompt})
	response = client.chat(model=model, messages=messages, options=options)
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

secrets = codecs.open('secrets.txt', 'r', 'utf-8').readlines()
secrets = [phrase.strip() for phrase in secrets]
client = Client(host=host)
text = codecs.open(file, 'r', 'utf-8').read()
words = text.split(" ")
score = 0
length = len(words)
step = int(length/tests)
steps = list(range(0, length, step))
steps = steps[:tests]
steps.append(length)
print("Testing "+model)
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
		print(f'Passed test {i+1}/{tests}, Position {position}/{length}')
	else:
		print(f'Failed test {i+1}/{tests}, Position {position}/{length}')
	if position<length:
		print(f'Score: {score}/{i+1}, {score/(i+1)*100.0:.2f}%')

print(f'Score: {score}/{tests}, {score/tests*100.0:.2f}%')
print(f"Finished in {time()-start:.2f} seconds.")