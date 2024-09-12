import datetime


def write_runtime_to_file():
    now = datetime.datetime.now()
    runtime = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('runtime.txt', 'a') as f:
        f.write(f"程序运行时间: {runtime}\n")


if __name__ == '__main__':
    write_runtime_to_file()
