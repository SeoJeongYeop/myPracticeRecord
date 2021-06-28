from multiprocessing import Process, Queue
import time
def work(id, start, end, result):
    total = 0
    for i in range(start, end):
        total += i
    result.put(total)
    return

for i in range(1,6):
    start = time.time()
    if __name__ == "__main__":
        print(i," 번째 실행")
        START, END = 0, 100000000
        result = Queue()
        th1 = Process(target=work, args=(1, START,  END//2, result))
        th2 = Process(target=work, args=(2, END//2, END, result))
    
        th1.start()
        th2.start()
        th1.join()
        th2.join()

        result.put('STOP')
        total = 0
        while True:
            tmp = result.get()
            if tmp == 'STOP':
               break
            else:
                total += tmp
        print(f"Result: {total}")
        print("time: ",time.time() - start)
    
""" 1  번째 실행
Result: 4999999950000000
time:  3.662855386734009
2  번째 실행
Result: 4999999950000000
time:  3.290029287338257
3  번째 실행
Result: 4999999950000000
time:  4.286776542663574
4  번째 실행
Result: 4999999950000000
time:  2.6736738681793213
5  번째 실행
Result: 4999999950000000
time:  3.8332200050354004 
"""