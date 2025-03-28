import time
import psutil
import datetime

pid_flag = True
t = 1
pid = int(input("Process pid: "))
if pid == 0:
    pid_flag = False
    t = 0.1

book = str(datetime.datetime.now()).split('.')[0].replace('-', '').replace(' ', '').replace(':', '') + '.csv'


def get_chrome_state(c_pid):
    try:
        p = psutil.Process(c_pid)
        return p
    except:
        return False


def write_performance_data(proc, book, t):
    try:
        book_list = [proc.pid,
                     str(datetime.datetime.now()),
                     round(proc.cpu_percent(interval=0.1), 1),
                     round(proc.memory_info().rss / (1024 * 1024), 1)]
        print(book_list)
        time.sleep(t)
        with open(book, 'a+', encoding='GBK') as book_file:
            book_file.write(','.join([str(b) for b in book_list]) + '\n')
    except Exception as e:
        print(e)
        raise BaseException(e)


def get_chrome_pid():
    chrome_proc_list = []

    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome'.upper() in proc.name().upper():
                chrome_proc = proc
                chrome_proc_list.append(chrome_proc)
        if not chrome_proc_list:
            return
        for c_proc in chrome_proc_list:
            if not get_chrome_state(c_proc.pid):
                chrome_proc_list.remove(c_proc)
            write_performance_data(c_proc, book, t)


def get_chrome_info_with_pid():
    while True:
        proc = get_chrome_state(pid)
        if proc:
            write_performance_data(proc, book, t)
        else:
            return


if __name__ == '__main__':
    psutil.getloadavg()
    if not pid_flag:
        get_chrome_pid()
    else:
        get_chrome_info_with_pid()