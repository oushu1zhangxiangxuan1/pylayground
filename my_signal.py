import signal
import time
import os
import sys

def main():
    def signal_handler(signum, frame):
        print('Receive signal:', signum)
        if signum == signal.SIGINT:
            print('I am going to quit safely!')
            sys.exit(0)

    print('Pid is ', os.getpid())

    signal.signal(signal.SIGHUP, signal_handler) # 1
    signal.signal(signal.SIGINT, signal_handler) # 2
    signal.signal(signal.SIGQUIT, signal_handler) # 3
    signal.signal(signal.SIGALRM, signal_handler) # 14
    signal.signal(signal.SIGTERM, signal_handler) # 15
    signal.signal(signal.SIGCONT, signal_handler) # 18


    while True:
        print('waiting...')
        time.sleep(2)
    return 



if __name__ =='__main__':
    main()