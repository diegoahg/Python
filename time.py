from time import time, strftime, localtime


def test():
    for i in range(100000):
        "Hello, world!".replace("Hello", "Goodbye")

start_time = time()
test()
elapsed_time = time() - start_time
print("Tiempo Transcurrido: %.10f seconds." % elapsed_time)
print strftime("%a, %d %b %Y %H:%M:%S", localtime())