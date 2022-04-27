import time

start = time.time()

for i in range(1000):
	current = time.time()
	print(current - start)
	time.sleep(1)