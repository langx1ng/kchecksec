#!/usr/bin/env python3
import sys
import re
import os

# ANSI 颜色
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

def colorize(text, color):
    return f"{color}{text}{RESET}"

def check_kernel_security(filepath):
    if not os.path.exists(filepath):
        print(f"{RED}[-] Cannot access '{filepath}': No such file{RESET}")
        return

    with open(filepath, 'r') as f:
        # 读取内容并处理换行符
        content = f.read().replace('\\\n', ' ')

    # 提取参数
    append_match = re.search(r'-append\s+[\'"](.*?)[\'"]', content)
    cpu_match = re.search(r'-cpu\s+([^\s\\]+)', content)

    append_str = append_match.group(1).lower() if append_match else ""
    cpu_str = cpu_match.group(1).lower() if cpu_match else ""

    # --- 1. KASLR ---
    if "nokaslr" in append_str:
        kaslr = colorize("Disabled", RED)
    elif "kaslr" in append_str:
        kaslr = colorize("Enabled", GREEN)
    else:
        kaslr = colorize("Enabled (Default)", GREEN)

    # --- 2. SMEP ---
    if "+smep" in cpu_str or ("smep" in append_str and "nosmep" not in append_str):
        smep = colorize("Enabled", GREEN)
    elif "-smep" in cpu_str or "nosmep" in append_str:
        smep = colorize("Disabled", RED)
    else:
        smep = colorize("Not Specified", YELLOW)

    # --- 3. SMAP ---
    if "+smap" in cpu_str or ("smap" in append_str and "nosmap" not in append_str):
        smap = colorize("Enabled", GREEN)
    elif "-smap" in cpu_str or "nosmap" in append_str:
        smap = colorize("Disabled", RED)
    else:
        smap = colorize("Not Specified", YELLOW)

    # --- 4. KPTI ---
    if "nopti" in append_str or "pti=off" in append_str:
        kpti = colorize("Disabled", RED)
    else:
        kpti = colorize("Enabled (Default)", GREEN)

    # --- 打印外观 (仿 checksec) ---
    filename = os.path.abspath(filepath)
    print(f"[{colorize('*', BLUE)}] '{filename}'") # 修复了这里
    print(f"    KASLR:      {kaslr}")
    print(f"    SMEP:       {smep}")
    print(f"    SMAP:       {smap}")
    print(f"    KPTI:       {kpti}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "run.sh"
    check_kernel_security(target)
