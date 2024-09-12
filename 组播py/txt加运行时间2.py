import os
import glob


def merge_txt_files(iptv_list, runtime):
    try:
        with open(iptv_list, 'a') as f1:
            with open(runtime, 'r') as f2:
                for line in f2:
                    f1.write(line)
        print(f"已成功将 {runtime} 合并到 {iptv_list}")
    except FileNotFoundError as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    merge_txt_files('iptv_list.txt', 'runtime.txt')
    
