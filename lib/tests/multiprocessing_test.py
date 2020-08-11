#!/usr/bin/env python3

from multiprocessing import Process
import time, random
import numpy as np

def task(min_sleep,max_sleep):
    time.sleep(random.randint(min_sleep,max_sleep)+random.random())
    return None

def main():
    num_threads = 4
    threads = []
    for idx in range(0,num_threads):
        thread = Process(target=task,args=(0,2,))
        thread.start()
        threads.append(thread)

    terminate = False
    all_done = np.zeros(num_threads)
    tic = time.time()
    while not terminate:
        for count,thread in enumerate(threads):
            if not thread.is_alive():
                if not (all_done[count] == 1):
                    toc = time.time()
                    all_done[count] = 1
                    print(f'Thread {count} finished in {toc-tic} seconds!')
        
        if np.sum(all_done) == num_threads:
            terminate = True
    # for thread in threads:
    #     thread.join()
    #     thread.is_alive()

if __name__ == '__main__':
    try:
        main()
    finally:
        pass