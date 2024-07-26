from multiprocessing import Pool
import time

def f(x):
    print(x*x)
    # return x*x


if __name__ == '__main__':
    pool = Pool(processes=4)
    # pool.map(f, range(10))
    # r = pool.map_async(f, range(10))
    # pool.apply_async(f,range(10))
    for i in range(10):
        r = pool.apply_async(f, (i,))
    #     print(r.get())
        # r.wait()
    # print(1234)
    # pool.close()
    # pool.join()