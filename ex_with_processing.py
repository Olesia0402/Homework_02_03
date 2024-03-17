import multiprocessing
import time


def factorize(*number) -> list:
    factorized_numbers = []
    for num in number:
        factors = [i for i in range(1, num + 1) if num % i == 0]
        factorized_numbers.append(factors)
    return factorized_numbers

def callback(result):
    print(f"Result in callback: {result}")

if __name__ == "__main__":
    # print(time.time())
    # for num in [128, 255, 99999, 10651060]:
    #     pr = multiprocessing.Process(target=factorize, args=(num, ))
    #     pr.start()
    #     pr.join()
    #     print(pr)
    # print(time.time())
    
    print(f"Count CPU: {multiprocessing.cpu_count()}")
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        print(time.time())
        p.map_async(
            factorize,
            (128, 255, 99999, 10651060),
            callback=callback,
        )
        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
        print(time.time())

    print(f'End {multiprocessing.current_process().name}')
