import numpy as np

class Location:
    def __init__(self, location):
        self.location = location

    def copy(self):
        return Location([x for x in self.location])

    def isLocation(self):
        if len(self.location) == 0:
            return True
        else:
            return False

    def getString(self):
        return "_".join([str(x) for x in self.location])

    def getNext(self):
        if len(self.location) <= 1:
            return Location([])
        else:
            return Location([x for x in self.location[1:]])

    def currentIndex(self):
        return self.location[0]

    def addLocation(self, expand):
        extended = self.location + [expand]
        return Location([x for x in extended])

class Node:
    def __init__(self, location, framework):
        self.framework = framework.copy()
        self.value = framework.copy()
        self.children = []
        self.location = location
        self.name = "Node_"+location.getString()

    def amountChildren(self):
        return len(self.children)

    def amountActiveChildren(self):
        return len(self.getActiveChidren())

    def setValue(self, new_value, key):
        self.value[key] = new_value

    def getValue(self, key):
        return self.value[key]

    def setChildren(self, children):
        if not self.isActive():
            return None

        self.children = children

    def reset(self):
        self.setChildren([])
        self.value = self.framework

    def addChild(self, SpecificNode=None):
        if not self.isActive():
            return None

        if SpecificNode is None:
            SpecificNode = Node
        child_location = self.location.addLocation(len(self.children))
        new_child = SpecificNode(child_location, self.framework)
        self.children.append(new_child)

        return new_child

    def getChild(self, location):
        if location.isLocation():
            return self
        else:
            inspect_child = self.children[location.currentIndex()]
            return inspect_child.getChild(location.getNext())

    def isActive(self):
        return self.value["Trigger"]

    def getActiveChidren(self):
        return [x for x in self.children if x.isActive()]

    def getFilteredChildren(self, boolfunc=None, *args, **kwargs):
        #print(args)
        #print(kwargs)
        if boolfunc is None:
            return self.children

        return [x for x in self.children if boolfunc(x.value, *args, **kwargs)]

    def setOff(self):
        self.value["Trigger"] = False

    def setOn(self):
        self.value["Trigger"] = True

    def recursive_call(self, function, function_args={}, filter_function=None, filtering_args={}, count_inactive=False, current_node=None,*args, **kwargs):
        children_calls = []
        for child in self.getFilteredChildren(filter_function, **filtering_args):
            if child.isActive() is True or count_inactive:
                if current_node is not None:
                    new_child = current_node.addChild()
                else:
                    new_child=None
                children_calls.append(child.recursive_call(function, function_args, filter_function, filtering_args, count_inactive, new_child, *args, **kwargs))

        fout = function(itself=self, children_outputs=children_calls, node=current_node, **function_args)
        if isinstance(fout, tuple):
            fout, cache = fout
            if current_node is not None:
                current_node.setValue(fout, "Value")
                current_node.setValue(cache, "Cache")
        return fout

class CallableNode(Node):
    def __init__(self, location, framework):
        super().__init__(location, framework)

    def __call__(self, *args, **kwargs):
        f = self.value["Function"]
        func_return = f(parent=self,*args, **kwargs)
        self.setValue(func_return,"Value")
        return func_return

class Tree:
    def __init__(self, value_framework, SpecificNode=Node):
        self.value_framework = value_framework.copy()
        self.value_framework["Trigger"] = True
        self.value_framework["Type"] = ""
        self.main_node = SpecificNode(Location([]), self.value_framework)

    def findNode(self, location_raw):
        loc = Location(location_raw)
        return self.main_node.getChild(loc)

    def reset(self):
        self.main_node.reset()

    def recursiveCall(self, function, location_raw=[], function_args={}, filter_function=None, filtering_args={}, count_inactive=False):
        node = self.findNode(location_raw)
        cache_framework = {
            "Cache": None,
            "Value": None
        }
        tree = Tree(cache_framework)
        current_node = tree.main_node
        return node.recursive_call(function, function_args, filter_function, filtering_args, count_inactive, current_node), tree

    class Filtering:
        @staticmethod
        # EQUALITY NODE METHODS
        def valueEquality(dict_obj, key, value):
            if dict_obj[key] == value:
                return True
            else:
                return False

    class Recursion:

        @staticmethod
        def getLeafValues(keys, **kwargs):
            node_obj = kwargs["itself"]
            children_outputs = kwargs["children_outputs"]

            dict_return = {}
            for key in keys:
                if len(children_outputs) == 0:
                    dict_return[key] = [node_obj.value[key]]
                else:
                    values_list = []
                    for child_dict in children_outputs:
                        values_list = values_list + child_dict[key]

                    dict_return[key] = values_list

            return dict_return

        @staticmethod
        def getAllValues(keys, **kwargs):
            dict_return = {}
            for key in keys:
                node_obj = kwargs["itself"]
                children_outputs = kwargs["children_outputs"]
                if len(children_outputs) == 0:
                    dict_return[key] = [node_obj.value[key]]
                else:
                    values_list = []
                    for child_dict in children_outputs:
                        values_list = values_list + child_dict[key]

                    values_list.append(node_obj.value[key])

                    dict_return[key] = values_list

            return dict_return

        @staticmethod
        def getAmountChildren(**kwargs):
            node_obj = kwargs["itself"]
            children_outputs = kwargs["children_outputs"]

            if len(children_outputs) == 0:
                return 1
            else:
                value = 1
                for val in children_outputs:
                    value += val

            return value

        @staticmethod
        def getAmountChildren(**kwargs):
            children_outputs = kwargs["children_outputs"]

            if len(children_outputs) == 0:
                return 1
            else:
                value = 1
                for val in children_outputs:
                    value += val

            return value

        @staticmethod
        def getMaxDepth(**kwargs):
            node_obj = kwargs["itself"]
            children_outputs = kwargs["children_outputs"]

            if len(children_outputs) == 0:
                return 0
            else:
                value = max(children_outputs) + 1

            return value

        @staticmethod
        def printNode(value_key, **kwargs):
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

            node_obj = kwargs["itself"]
            children_outputs = kwargs["children_outputs"]

            if len(children_outputs) == 0:
                return node_obj.getValue(value_key)
            else:

                l = children_outputs[::-1]
                n = len(l)
                s = ""

                if n > 1:

                    start_line_count = len(str(l[0]).splitlines()) // 2
                    for i in range(start_line_count):
                        s += value_branch("EMPTY", value=str(l[0]).splitlines()[i], num_spaces=3)
                    s += value_branch("UP", str(l[0]).splitlines()[start_line_count])
                    for i in range(1, start_line_count + 1):
                        s += value_branch("BASE", value=str(l[0]).splitlines()[start_line_count + i], num_spaces=2)

                    for i in range(1, n - 1):
                        s += value_branch("BASE")

                        start_line_count = len(str(l[i]).splitlines()) // 2
                        for j in range(start_line_count):
                            s += value_branch("BASE", value=str(l[i]).splitlines()[j], num_spaces=2)
                        s += value_branch("BODY", str(l[i]).splitlines()[start_line_count])
                        for j in range(1, start_line_count + 1):
                            s += value_branch("BASE", value=str(l[i]).splitlines()[start_line_count + j], num_spaces=2)

                    s += value_branch("BASE")

                    start_line_count = len(str(l[-1]).splitlines()) // 2
                    for i in range(start_line_count):
                        s += value_branch("BASE", value=str(l[-1]).splitlines()[i], num_spaces=2)
                    s += value_branch("DOWN", str(l[-1]).splitlines()[start_line_count])
                    for i in range(1, start_line_count + 1):
                        s += value_branch("EMPTY", value=str(l[-1]).splitlines()[start_line_count + i], num_spaces=3)

                else:
                    start_line_count = len(str(l[0]).splitlines()) // 2
                    for i in range(start_line_count):
                        s += value_branch("EMPTY", value=str(l[0]).splitlines()[i], num_spaces=3)
                    s += value_branch("BODY", str(l[0]).splitlines()[start_line_count])
                    for i in range(1, start_line_count + 1):
                        s += value_branch("EMPTY", value=str(l[0]).splitlines()[start_line_count + i], num_spaces=2)

                c_value = len(s.splitlines()) // 2

                lines = s.splitlines()
                new_lines = []

                for i, line in enumerate(lines):
                    add_value = f"{node_obj.getValue(value_key)}--"

                    if i == c_value:
                        new_line = add_value + line
                    else:
                        new_line = " " * len(add_value) + line
                    new_lines.append(new_line)

                return "\n".join(new_lines)

"""
class Sequence(Tree):
    def __init__(self, value_framework, SpecificNode=Node):
        super().__init__(value_framework, SpecificNode)

class SequenceNode(Node):
    def __init__(self, location, framework):
        super().__init__(location, framework)
"""

class FunctionTree(Tree):
    def __init__(self, function):
        fw = {
            "Function": function,
            "Value": None
        }
        super().__init__(fw, CallableNode)
        self.called = False

    def __call__(self, *args, **kwargs):
        self.called = True
        return self.main_node(*args, **kwargs)

    class Recursion:
        @staticmethod
        def generatePermutations(element_list, k, removed_element=None, count=0, **kwargs):
            if k == count:
                return np.array([[removed_element]])

            else:
                parent = kwargs["parent"]
                children_in_sequence = None
                for e in element_list:
                    new_child = parent.addChild(CallableNode)
                    new_list = [x for x in element_list if x != e]
                    child_call = new_child(new_list, k, e, count + 1)
                    if children_in_sequence is None:
                        children_in_sequence = child_call
                    else:
                        children_in_sequence = np.concatenate([children_in_sequence, child_call], axis=1)

                if removed_element is None:
                    return children_in_sequence
                else:
                    removed_array = np.full((1, children_in_sequence.shape[1]), removed_element)
                    concat_array = np.concatenate([removed_array, children_in_sequence], axis=0)
                return concat_array


def exp(num, **kwargs):
    if num == 0:
        return 1
    else:
        parent = kwargs["parent"]
        new_child = parent.addChild(CallableNode)
        return num*new_child(num-1)

def exp_summation(num, **kwargs):
    if num <= 1:
        return num

    else:
        parent = kwargs["parent"]
        new_child1 = parent.addChild(CallableNode)
        new_child2 = parent.addChild(CallableNode)
        return new_child2(num - 2) + new_child1(num - 1)


"""
f = FunctionTree(exp)
print(f(6))
i = [0,0,0,0,0]
print(f.findNode(i).name)
print(f.findNode(i).value["Value"])
print(f.findNode(i).recursive_call(getLeafValues, ["Value"]))

fwC = {
    "Function": exp,
    "Value": None
}

n = CallableNode(Location([0]), fwC)
print(n(5))

fw = {
    "Value": None,
    "Power": None
}
tree = Tree(fw)
main_node = tree.main_node
main_node.setValue(0, "Value")
ch1 = main_node.addChild()
ch2 = main_node.addChild()
ch1.setValue(1, "Value")
ch2.setValue(2, "Value")
ch1_1 = ch1.addChild()
ch1_2 = ch1.addChild()
ch1_3 = ch1.addChild()
ch1_1.setValue(11, "Value")
ch1_2.setValue(12, "Value")
ch1_3.setValue(13, "Value")
ch2_1 = ch2.addChild()
ch2_2 = ch2.addChild()
ch2_3 = ch2.addChild()
ch2_1.setValue(21, "Value")
ch2_2.setValue(22, "Value")
ch2_3.setValue(23, "Value")
ch1_1_1 = ch1_1.addChild()
ch1_1_2 = ch1_1.addChild()
ch1_1_1.setValue(111, "Value")
ch1_1_2.setValue(112, "Value")

l = Location([0,0,1])
search = main_node.getChild(l)
print(search.value)
print(search.name)
print(l.getString())
"""


