from threading import Thread
import time
def work(id, start, end, result):
    total = 0
    for i in range(start, end):
        total += i
    result.append(total)
    return

for i in range(1,6):
    print(i,"번째 실행")
    start = time.time()
    if __name__ == "__main__":
        START, END = 0, 100000000
        result = list()
        th1 = Thread(target=work, args=(1, START, END, result))
    
        th1.start()
        th1.join()

    print(f"Result: {sum(result)}")
    print("time :", time.time() - start)

"""
쓰레드 2개 
1 번째 실행
Result: 4999999950000000
time : 8.633133888244629
2 번째 실행
Result: 4999999950000000
time : 7.330349445343018
3 번째 실행
Result: 4999999950000000
time : 7.448468446731567
4 번째 실행
Result: 4999999950000000
time : 6.158426761627197
5 번째 실행
Result: 4999999950000000
time : 5.50690770149231
"""
"""
쓰레드 1개...?
1 번째 실행
Result: 4999999950000000
time : 9.45898723602295
2 번째 실행
Result: 4999999950000000
time : 4.212064266204834
3 번째 실행
Result: 4999999950000000
time : 3.1868174076080322
4 번째 실행
Result: 4999999950000000
time : 6.384443521499634
5 번째 실행
Result: 4999999950000000
time : 5.203074216842651
    """