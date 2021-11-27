import os

stack = []
all_level = []  # 记录运行层级


def interpreter(order, execute_key):
    # LIT 将常数取出放到栈顶
    if order[0] == "LIT":
        stack.append(int(order[2]))
        execute_key += 1

    # 取数，lev 相对层，a相对地址
    elif order[0] == "LOD":
        # len（running）= 调用层级
        if len(all_level) == 0:
            stack.append(int(stack[order[2]]))
        else:
            # 调用层级为1
            if order[1] == 1:
                stack.append(int(stack[order[2]]))
            #  局部变量 即不在主函数内的变量的操作
            else:
                # 本层地址＋下一层全部的空间大小
                stack.append(int(stack[order[2] + all_level[-1][1]]))
        #  往下运行一行
        execute_key = execute_key + 1

    #     将栈顶内容送入某变量单元中，a为相对地址，t为层数
    elif order[0] == "STO":
        if len(all_level) == 0:
            stack[order[2]] = int(stack[-1])
            stack.pop()
        else:
            if order[1] == 1:
                stack[order[2]] = int(stack[-1])
            #  局部变量 即不在主函数内的变量的操作
            else:
                stack[order[2] + all_level[-1][1]] = int(stack[-1])
            # 弹出
            stack.pop()
        execute_key = execute_key + 1

    #     调用函数
    elif order[0] == "CAL":
        # 调用一次cal，则调用层级加1，添加在第几局
        all_level.append([execute_key, len(stack)])
        execute_key = order[2]

    # 开辟新空间，int 0 a（开辟的空间），初始是3，常数变量不初始化
    elif order[0] == "INT":
        for i in range(order[2]):
            # 赋初值为0
            stack.append(0)
        execute_key += 1

    # 无条件跳转
    elif order[0] == "JMP":
        execute_key = order[2]

    #     判断栈顶元素是否为0，符合就跳转，不符合
    elif order[0] == "JPC":
        if stack[-1] == 0:
            execute_key = order[2]
            stack.pop()
        else:
            execute_key += 1
            stack.pop()

    # 栈顶和次栈顶运算，最后退两个操作数
    # 加
    elif order[0] == "ADD":
        num = int(stack[-2]) + int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        execute_key += 1

    # 减
    elif order[0] == "SUB":
        num = int(stack[-2]) - int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        execute_key += 1

    #  乘
    elif order[0] == "MUL":
        num = int(stack[-2]) * int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        execute_key += 1

    # 除
    elif order[0] == "DIV":
        num = int(stack[-2]) / int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        execute_key += 1

    #     读入
    elif order[0] == "RED":
        print("请输入：")
        num = int(input())
        # 放到栈顶
        stack.append(num)
        execute_key += 1

    #    写
    elif order[0] == "WRT":
        print('输出： ')
        print(stack[-1])
        stack.pop()
        execute_key += 1

    #     结束一层的调用
    elif order[0] == "RET":
        # 把栈这一层的数据退栈
        for i in range(len(stack) - all_level[-1][1]):
            stack.pop()
        all_level.pop()
        # 退栈后如果0，则是在主程序内，主程序return则结束程序，将execute_key设为1e4
        if (len(all_level) == 0):
            execute_key = 1e4
        else:
            # 如果还有则从调用点的下一个程序执行
            execute_key = all_level[-1][0] + 1

    return execute_key


if __name__ == "__main__":
    temp_str = []
    orders = []
    print("请输入C0目标代码文件：")
    file_path = input()
    with open(file_path, "r") as f:
        for line in f:
            if line.split():
                temp_str.append(line)
    # 将指令划分
    for str in temp_str:
        orders.append([str[0:3], int(str[4]), int(str[6:])])
    execute_key = 0
    while execute_key < len(orders):
        execute_key = interpreter(orders[execute_key], execute_key)
    print('执行完成！')
