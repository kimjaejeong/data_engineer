import ray
import datetime
import time
import numpy as np
import psutil

# Ray Task
@ray.remote
def print_current_datetime():
    time.sleep(0.3)
    current_datetime = datetime.datetime.now()
    print(current_datetime)
    return current_datetime

@ray.remote
def no_work(a):
    return


def process_run(num):
    futures = [print_current_datetime.remote() for i in range(num)]
    ray.get(futures)

if __name__ == "__main__":
    num_logical_cpus = psutil.cpu_count()
    print(num_logical_cpus)
    ray.init(num_cpus = 8)
    # ray.init(num_cpus=num_logical_cpus, ignore_reinit_error=True)

    # test1
    '''
    num 개의 프로세스에 병렬처리
    num 개의 프로세스 log가 생성됨(=num개로 나눠서 작업함)
    '''
    # process_run(16)

    # test2 - ray.put 비교
    start = time.time()
    a = np.zeros((5000,5000))
    result_ids = [no_work.remote(a) for x in range(10)]
    results = ray.get(result_ids)
    print("duration =", time.time() - start)

    start = time.time()
    a_id = ray.put(np.zeros((5000,5000)))
    result_ids = [no_work.remote(a_id) for x in range(10)]
    results = ray.get(result_ids)
    print("duration =", time.time() - start)









    print("종료")


'''
ray.put() - 큰 배열을 공유 메모리에 저장하고 복사본을 만들지 앟고 모든 작업자에 프로세스에 엑세스 할 수 있음
            

'''