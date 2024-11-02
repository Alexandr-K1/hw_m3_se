import time
from multiprocessing import Pool, cpu_count


def factorize(number):
    return [i for i in range(1, number + 1) if number % i ==0]

def factorize_sync(*numbers):
    result = []
    for number in numbers:
        div = factorize(number)
        result.append(div)
    return result

def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factorize, numbers)
    return result

def test_func(factorize_func, description):
    start_time = time.time()
    a, b, c, d  = factorize_func(128, 255, 99999, 10651060)
    end_time = time.time()

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f"{description} execution time: {end_time - start_time:.4f} seconds")


if __name__ == '__main__':
    test_func(factorize_sync, "Sync")
    test_func(factorize_parallel, "Parallel")
