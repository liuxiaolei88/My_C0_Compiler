import sys


def test(token):  # tonken: 标识符序列

    var_global_item = ["return"]  # 全局变量表
    var_loc_item = [[]]  # 局部变量表
    table_fun = []  # 函数表
    is_global_variate = [True]  # 判断是否在全局作用域
    isVoid = [True]
    # 指令0.
    var_glo = []  # 全局变量定义指令
    fun_main = []  # 主函数指令
    # ok
    def error(type):  # 错误处理
        print("error ", type)
        if type == 1:
            print("程序发生错误")
        elif type == 2:
            print("变量查找失败")
        elif type == 3:
            print("缺失分号")
        elif type == 4:
            print("缺失逗号")
        elif type == 5:
            print("变量定义错误")
        elif type == 6:
            print("int 函数声明错误")
        elif type == 7:
            print("void 函数声明错误")
        elif type == 8:
            print("主函数")
        #     目前程序不支持处理==
        elif type == 9:
            print("缺失==")
        elif type == 10:
            print("语句声明错误")
        elif type == 11:
            print("读入语句错误")
        elif type == 12:
            print("栈空")
        elif type == 13:
            print("意外的符号")
        sys.exit(0)
    # ok
    def begin_compile():  # 入口
        print("###开始编译###")
        token_index = 0
        # 全局变量定义部分,如果是int类型 并且后面跟着标识符ID 且没有（ 函数
        if token[token_index].type == "INT" \
                and token[token_index + 1].type == "ID" \
                and token[token_index + 2].type != "(":
            token_index, vg = var_process(token_index)
            var_glo.append(vg)
        is_global_variate[0] = False
        while True:  # 自定义函数定义部分
            if token[token_index].type == "INT"\
                    and token[token_index + 1].type == "ID" \
                    and token[token_index + 2].type == "(":
                token_index = fun_int_process(token_index)
            elif token[token_index].type == "VOID" \
                    and token[token_index + 1].type == "ID":
                token_index = fun_void_process(token_index)
            else:
                break
        if token[token_index].type == "VOID" \
                and token[token_index + 1].type == "MAIN":
            token_index = fun_main_process(token_index)
        else:
            error(1)
    # ok
    def var_add(token_value):  # 创建变量
        print("创建变量", token_value)
        # 判断是否为全局变量
        if is_global_variate[0] is True:  # 是全局变量
            if token_value not in var_global_item:
                var_global_item.append(token_value)
        else:  # 局部变量
            if token_value not in var_loc_item[0]:
                var_loc_item[0].append(token_value)
    # ok
    def var_find(id):  # 查找变量 返回变量地址 0or1,a
        print("寻找变量的层差以及相对地址：", id)
        # 先查找局部变量,再查找全局变量
        # 局部 0
        if id in var_loc_item[0]:
            return 0, var_loc_item[0].index(id)
        elif id in var_global_item:
            return 1, var_global_item.index(id)
        else:
            error(2)
    # ok
    def var_process(start):  # 变量定义 返回指针位置，指令
        print("处理变量", token[start])
        t = start + 1
        var_add(token[t].value)
        t = t + 1
        # 判断语句是否结束
        is_sentence_end = True
        # 对于定义变量的语句进行处理
        while True:
            # 如果为分号，说明一句话结束
            if token[t].type == ";":
                if is_sentence_end == True:
                    break
                else:
                    # 处理没有分号的情况
                    error(3)
            #         如果是逗号，说明定义语句没有结束
            elif token[t].type == ",":
                if is_sentence_end == True:
                    is_sentence_end = False
                else:
                    error(4)
            elif token[t].type == "ID":
                if is_sentence_end == False:
                    var_add(token[t].value)
                    is_sentence_end = True
                else:
                    error(5)
            t = t + 1
        #     输出指令 ： INT 全局大小是全局变量开辟空间数+1
        order = ["INT", 0, len(var_global_item) if is_global_variate[0] is True else len(var_loc_item[0])]
        return t + 1, order
    # ok
    def fun_int_process(start):  # int函数 返回指针位置
        print("处理INT类型函数", token[start])
        isVoid[0] = False
        token_index = start
        orders = []
        # 函数名字
        fun_name = token[token_index + 1].value
        if token[token_index + 2].type == "(" \
                and token[token_index + 3].type == ")" \
                and token[token_index + 4].type == "{":
            token_index = token_index + 4
            token_index, orders = block_process(token_index)
        else:
            error(6)
        orders = order_sort(orders)
        table_fun.append([fun_name, orders, 0])
        return token_index
    # ok
    def fun_void_process(start):  # void函数 返回指针位置
        print("void 函数处理", token[start])
        isVoid[0] = True
        t = start
        orders = []
        fun_name = token[t + 1].value
        if token[t + 2].type == "(" and token[t + 3].type == ")" and token[t + 4].type == "{":
            t = t + 4
            t, orders = block_process(t)
        else:
            error(7)
        orders = order_sort(orders)
        table_fun.append([fun_name, orders, 0])
        return t
    # ok
    def fun_main_process(start):  # 主函数 返回指针位置
        print("处理main函数", token[start])
        isVoid[0] = True
        token_index = start
        if token[token_index + 2].type == "(" and token[token_index + 3].type == ")" and token[token_index + 4].type == "{":
            token_index = token_index + 4
            token_index, fun_main_order = block_process(token_index)
            fun_main_order = order_sort(fun_main_order)
            fun_main.append(fun_main_order)
        else:
            error(8)
        return token_index
    # ok
    def block_process(start):  # 分程序 返回指针位置，指令
        print("处理分程序", token[start])
        t = start + 1
        var_loc_item[0] = []  # 初始化局部变量表
        orders = []
        # 在分函数定义变量
        if token[t].type == "INT" and token[t + 1].type == "ID" and token[t + 2].type != "(":
            t, order = var_process(t)
            orders.append(order)
        while True:  # 语句处理
            if token[t].type == "}":
                break
            else:
                t, order = sentence_deal(t)
                orders.append(order)
        return t + 1, orders
    # ok
    def sentence_deal(start):  # 语句处理入口，返回语句指针以及指令
        print("语句处理", token[start])
        token_index = start
        if token[token_index].type == "IF":
            token_index, order = sen_if_deal(token_index)
            return token_index, order
        elif token[token_index].type == "WHILE":
            token_index, order = sen_while_deal(token_index)
            return token_index, order
        elif token[token_index].type == "RETURN":
            token_index, order = sen_return_deal(token_index)
            return token_index, order
        elif token[token_index].type == "SCANF":
            token_index, order = sen_scanf_deal(token_index)
            return token_index, order
        elif token[token_index].type == "PRINTF":
            token_index, order = sen_printf_deal(token_index)
            return token_index, order
        elif token[token_index].type == "ID":
            if token[token_index + 1].type == "=":
                token_index, order = sen_equal_deal(token_index)
                return token_index, order
            elif token[token_index + 1].type == "(" and token[token_index + 2].type == ")":
                token_index, order = sen_fun_call_deal(token_index)
                return token_index, order
            else:
                # ID后面出现其他符号
                error(9)
        else:
            # 语句定义错
            error(10)
    # ok
    def sen_if_deal(start):
        print('处理if语句')
        token_index = start
        orders = []
        token_index = token_index + 2
        # 处理（）中的判断，LOD
        token_index, order1 = exp_deal(token_index)
        order1 = order_sort(order1)
        order2 = []
        token_index = token_index + 1
        while True:  # 对语句处理
            if token[token_index].type == "}":
                break
            else:
                token_index, order = sentence_deal(token_index)
                order2.append(order)
        order2 = order_sort(order2)
        token_index = token_index + 1
        if token[token_index].type == "ELSE":
            order3 = []
            token_index = token_index + 2
            while True:  # 语句处理
                print(token[token_index])
                if token[token_index].type == "}":
                    break
                else:
                    token_index, order = sentence_deal(token_index)
                    order3.append(order)
            order3 = order_sort(order3)
            token_index = token_index + 1
            orders.append(order1)
            orders.append(["JPC", 0, len(order2) + 2])
            orders.append(order2)
            orders.append(["JMP", 0, len(order3) + 1])
            orders.append(order3)
            return token_index, orders
        # 只有if的情况
        orders.append(order1)
        orders.append(["JPC", 0, len(order2) + 1])
        orders.append(order2)
        return token_index, orders
    # ok
    def sen_while_deal(start):
        print("while语句处理", token[start])
        token_index = start
        orders = []
        # （ a ,len+2
        token_index = token_index + 2
        # 找（）条件内的变量，把他加载出来
        token_index, order1 = exp_deal(token_index)
        order1 = order_sort(order1)
        # 处理完条件index + 1
        token_index = token_index + 1
        order2 = []
        # 处理while里面的语句
        while True:
            if token[token_index].type == "}":
                break
            else:
                token_index, order = sentence_deal(token_index)
                order2.append(order)
        order2 = order_sort(order2)
        # 先添加while（ x） 的指令
        orders.append(order1)
        # 添加判断while（）里条件的指令
        # JPC 0 a	| 条件跳转，当栈顶值为0，则跳转至a地址，否则顺序执行
        orders.append(["JPC", 0, len(order2) + 2])
        # 如果满足条件走这里
        orders.append(order2)
        # JMP 0 a	| 无条件跳转至a地址
        # while结束以后结束到while调用的地方
        orders.append(["JMP", 0, -len(order1) - len(order2) - 1])
        return token_index + 1, orders
    # ok
    def sen_equal_deal(start):
        # 处理等于号 = 语句
        # STO t a	| 将栈顶内容送入某变量单元中，a为相对地址，t为层数
        # token[start]是等号左边的标识符，使用exp_deal进行处理，运算等号右边的表达式
        print("对代码中的等号进行处理", token[start])
        token_index = start
        orders = []
        level, offset = var_find(token[token_index].value)
        token_index = token_index + 2
        # 处理运算
        token_index, order = exp_deal(token_index)
        orders.append(order)
        orders.append(["STO", level, offset])
        return token_index, orders
    # ok
    def sen_return_deal(start):
        print("处理return", token[start])
        token_index = start
        orders = []
        # 判断函数类型
        # void 不需要返回具体值，所以不需要sto
        if isVoid[0] is True:
            orders.append(["RET", 0, 0])
            return token_index + 2, orders
        else:
            token_index = token_index + 1
            token_index, order = exp_deal(token_index)
            orders.append(order)
            # STO t a	| 将栈顶内容送入某变量单元中，a为相对地址，t为层数，存储函数返回值
            # RET 0 0	| 函数调用结束后,返回调用点并退栈
            orders.append(["STO", 1, 0])
            orders.append(["RET", 0, 0])
            return token_index, orders
    # ok
    def sen_scanf_deal(start):
        print("处理scanf语句", token[start])
        token_index = start
        if token[token_index].type == "SCANF" and token[token_index + 1].type == "(" and token[token_index + 2].type == "ID" and token[
            token_index + 3].type == ")" and token[token_index + 4].type == ";":
            scanf_value = token[token_index + 2].value
            lev, offset = var_find(scanf_value)
            order = []
            # RED 0 0	| 从命令行读入一个输入置于栈顶
            order.append(["RED", 0, 0])
            # STO t a	| 将栈顶内容送入某变量单元中，a为相对地址，t为层数
            order.append(["STO", lev, offset])
            # len(scanf (x);) = 5
            return token_index + 5, order
        else:
            error(11)
    # ok
    def sen_printf_deal(start):
        print("处理printf语句", token[start])
        token_index = start
        orders = []
        token_index = token_index + 2
        # 需LOD数据
        token_index, order = exp_deal(token_index)
        orders.append(order)
        orders.append(["WRT", 0, 0])
        return token_index + 1, orders
    # 函数调用
    # ok
    def sen_fun_call_deal(start):
        print("处理函数调用", token[start])
        token_index = start
        order = []
        # 把函数名字写入指令，最后处理
        order.append(["CAL", 0, token[token_index].value])
        token_index = token_index + 4
        return token_index, order
    # 表达式处理
    def exp_deal(start):
        print("表达式处理", token[start])
        t = start
        order = []
        stack = []

        def operation():
            if len(stack) == 0:
                error(12)
            #     判断最上面一层的符号
            elif stack[-1] == "+":
                order.append(["ADD", 0, 0])
            elif stack[-1] == "-":
                order.append(["SUB", 0, 0])
            elif stack[-1] == "*":
                order.append(["MUL", 0, 0])
            elif stack[-1] == "/":
                order.append(["DIV", 0, 0])
            else:
                error(13)
            stack.pop()

        while True:
            # 判断数字
            if token[t].type == "NUM":
                order.append(["LIT", 0, token[t].value])
                t = t + 1
            #     如果是变量：则需要lod
            elif token[t].type == "ID" and token[t + 1].type != "(":
                lev, offset  = var_find(token[t].value)
                order.append(["LOD", lev, offset ])
                t = t + 1
            #     函数
            elif token[t].type == "ID" and token[t + 1].type == "(" and token[t + 2].type == ")":
                # CAL 0 a	| 调用函数，a为函数地址
                order.append(["CAL", 0, token[t].value])
                # LOD t a	| 将变量值取到栈顶，a为相对地址，t为层数
                order.append(["LOD", 1, 0])
                # （X）需要t+3
                t = t + 3
            #     处理（ 的运算
            elif token[t].type == "(":
                stack.append("(")
                t = t + 1
            #     做运算
            elif token[t].type == ")":
                while len(stack) != 0 and stack[-1] != "(":
                    operation()
                t = t + 1
                # 处理完（）需要弹出
                if len(stack) != 0:
                    stack.pop()
                else:
                    break
            elif token[t].type == "+":
                while True:
                    # 在为空 或者 （）优先的时候
                    if len(stack) == 0 or stack[-1] == "(":
                        stack.append("+")
                        break
                    #     如果不为空则需要先进行计算，因为加减的优先级会小于乘除
                    else:
                        operation()
                t = t + 1
            elif token[t].type == "-":
                while True:
                    if len(stack) == 0 or stack[-1] == "(":
                        stack.append("-")
                        break
                    else:
                        operation()
                t = t + 1
            elif token[t].type == "*":
                stack.append("*")
                t = t + 1
            elif token[t].type == "/":
                stack.append("/")
                t = t + 1
            #     在；做运算
            elif token[t].type == ";":
                while len(stack) != 0:
                    operation()
                t = t + 1
                break
        print("exp:", order)
        return t, order

    # 将分步的指令综合在一起，找到每一小行的第一个
    def order_sort(orders):
        o = []
        def work(order):
            # 判断是否是str类型，str
            if isinstance(order[0], str):
                o.append(order)
                return
            else:
                for x in order:
                    work(x)

        work(orders)
        return o

    print("开始编译")
    begin_compile()
    print("编译完成")
    var_glo = var_glo[0]
    fun_main = fun_main[0]

    tot = []
    tot.append(["JMP", 0, 0])
    t = 1
    for i in range(len(table_fun)):
        table_fun[i][2] = t
        t = t + len(table_fun[i][1])
        tot.append(table_fun[i][1])
    m = t
    t = t + len(fun_main)
    tot.append(fun_main)
    tot.append(var_glo)
    tot.append(["CAL", 0, "main"])
    tot = order_sort(tot)
    # 写主函数入口
    tot[0][2] = t
    for i in range(len(tot)):
        if tot[i][0] == "JMP" or tot[i][0] == "JPC":
            # 因为最开始加jmp的时候是以当前指令长度大小设的，排序以后前面会加指令，所以跳转也要相加
            tot[i][2] = tot[i][2] + i
        #     处理函数
        elif tot[i][0] == "CAL":
            name = tot[i][2]
            if name == "main":
                tot[i][2] = m
            else:
                # table_fun 存放对于函数的指令
                for x in table_fun:
                    if name == x[0]:
                        # cal 入口 等于上一个函数和的结束
                        tot[i][2] = x[2]
                if isinstance(tot[i][2], str):
                    error(0)

    return tot
