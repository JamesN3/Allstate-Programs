import threading
import time
import concurrent.futures

start = time.perf_counter()


def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    print("Done Sleeping")
    return f"Done Sleeping...{seconds}"


# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

threads = []

# _ throwaway variable
for _ in range(10):
    t = threading.Thread(target=do_something, args=[1.5])
    t.start()
    threads.append(t)
# Stops program from moving on

for thread in threads:
    thread.join()
finish = time.perf_counter()

print(f"Finished in {round(finish-start, 2)} second(s)")

with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    # Returns in order they were started
    results = executor.map(do_something, secs)

    for result in results:
        print(result)
    # f1 = executor.submit(do_something, 1)
    # f2 = executor.submit(do_something, 1)

    # # A for loop but in list comprehension
    # results = [executor.submit(do_something, sec) for sec in secs]

    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())
