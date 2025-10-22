



def printTree(l, **kwargs):
    def value_branch(type, value=None, indentation=True, num_spaces=0):
        branches_dict = {
            "UP": " /-",
            "BASE": "|",
            "BODY": "|--",
            "DOWN": " \\-",
            "EMPTY": ""
        }

        s = ""

        s += branches_dict[type]
        s += " " * num_spaces


        if value is not None:
            s += str(value)
        if indentation:
            s += "\n"

        return s

    #node_obj = kwargs["itself"]
    #children_outputs = kwargs["children_outputs"]


    n = len(l)
    s = ""

    if len(l) > 1:
        start_line_count = len(str(l[0]).splitlines()) // 2
        for i in range(start_line_count):
            s += value_branch("EMPTY", value=l[0].splitlines()[i], num_spaces=3)
        s += value_branch("UP", l[0].splitlines()[start_line_count])
        for i in range(1,start_line_count+1):
            s += value_branch("BASE", value=l[0].splitlines()[start_line_count+i], num_spaces=2)

        for i in range(1,n-1):
            s += value_branch("BASE")

            start_line_count = len(str(l[i]).splitlines()) // 2
            for j in range(start_line_count):
                s += value_branch("BASE", value=l[i].splitlines()[j], num_spaces=2)
            s += value_branch("BODY", l[i].splitlines()[start_line_count])
            for j in range(1, start_line_count + 1):
                s += value_branch("BASE", value=l[i].splitlines()[start_line_count + j], num_spaces=2)

        s += value_branch("BASE")

        start_line_count = len(str(l[-1]).splitlines()) // 2
        for i in range(start_line_count):
            s += value_branch("BASE", value=l[-1].splitlines()[i], num_spaces=2)
        s += value_branch("DOWN", l[-1].splitlines()[start_line_count])
        for i in range(1, start_line_count + 1):
            s += value_branch("EMPTY", value=l[-1].splitlines()[start_line_count + i], num_spaces=3)

    else:
        start_line_count = len(str(l[0]).splitlines()) // 2
        for i in range(start_line_count):
            s += value_branch("EMPTY", value=l[0].splitlines()[i], num_spaces=3)
        s += value_branch("BODY", l[0].splitlines()[start_line_count])
        for i in range(1, start_line_count + 1):
            s += value_branch("EMPTY", value=l[0].splitlines()[start_line_count + i], num_spaces=2)

    c_value = len(s.splitlines()) // 2
    print(n)
    print(c_value)

    lines = s.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        if i == c_value:
            new_line = "-#-" + line
        else:
            new_line = " "*3 + line
        new_lines.append(new_line)

    return "\n".join(new_lines)

fs = printTree([printTree([printTree(["a"])])])
fs = printTree([printTree(["1",printTree(["1","2","3","4"])]),"2",printTree(["1"]),"4"])
print(fs)


