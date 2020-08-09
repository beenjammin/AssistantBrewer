from multiprocessing import Process
import time

def fun():
    print('starting fun')
    time.sleep(2)
    print('finishing fun')

def main():
    fun()
    p = Process(target=fun)
    p.start()
    p.join()


if __name__ == '__main__':

    print('starting main')
    main()
    print('finishing main')