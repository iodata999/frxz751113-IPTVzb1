import os
import glob


def merge_txt_files(runtime, iptv_list):
    try:
        with open(runtime, 'a') as f1:
            with open(iptv_list, 'r') as f2:
                for line in f2:
                    f1.write(line)
        print(f"已成功将 {iptv_list} 合并到 {runtime}")
    except FileNotFoundError as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    merge_txt_files('runtime.txt', 'iptv_list.txt')
