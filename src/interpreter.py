import os

stack = []
running = []

def C0_run(orders): #key: 下一个执行的指令序号
    running.append([0,0])
    key = 0
    print(orders)
    while key < len(orders):
        key = C0_execute(orders[key],key)

def C0_execute(order,key):
    if order[0]=="LIT":
        stack.append(int(order[2]))
        key+=1
    elif order[0]=="LOD":
        if order[1]==1:
            stack.append(int(stack[order[2]]))
        else:
            stack.append(int(stack[order[2]+running[-1][1]]))
        key+=1
    elif order[0]=="STO":
        if order[1]==1:
            stack[order[2]]=int(stack[-1])
            stack.pop()
        else:
            stack[order[2]+running[-1][1]]=int(stack[-1])
            stack.pop()
        key+=1
    elif order[0]=="CAL":
        running.append([key,len(stack)])
        key=order[2]
    elif order[0]=="INT":
        for i in range(order[2]):
            stack.append(0)
        key+=1
    elif order[0]=="JMP":
        key = order[2]
    elif order[0]=="JPC":
        if stack[-1]==0:
            key = order[2]
        else:
            key += 1
    elif order[0]=="ADD":
        num = int(stack[-2]) + int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        key+=1
    elif order[0]=="SUB":
        num = int(stack[-2]) - int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        key+=1
    elif order[0]=="MUL":
        num = int(stack[-2]) * int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        key+=1
    elif order[0]=="DIV":
        num = int(stack[-2]) / int(stack[-1])
        stack.pop()
        stack.pop()
        stack.append(num)
        key+=1
    elif order[0]=="RED":
        print(":",end=" ")
        num = input()
        num = int(num)
        stack.append(num)
        key+=1
    elif order[0]=="WRT":
        print(stack[-1])
        stack.pop()
        key+=1
    elif order[0]=="RET":
        for i in range(len(stack)-running[-1][1]):
            stack.pop()
        key=running[-1][0]+1
        running.pop()

    return key


if __name__ == "__main__":
    sentence = []
    orders = []
    print("请输入c0temp文件地址")
    filepath = '../temp.txt'
    with open(filepath,"r") as f:
        for line in f:
            if line.split():
                sentence.append(line)
    for str in sentence:
        orders.append([str[0:3],int(str[4]),int(str[6:])])
    C0_run(orders)
