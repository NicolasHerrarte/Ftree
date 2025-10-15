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

    def setValue(self, new_value, key):
        self.value[key] = new_value

    def setChildren(self, children):
        self.children = children

    def addChild(self, SpecificNode=None):
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

    def recursive_call(self, function, *args, **kwargs):
        children_calls = []
        for child in self.children:
            children_calls.append(child.recursive_call(function, *args, **kwargs))

        return function(itself=self, children_outputs=children_calls, *args, **kwargs)

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
        self.main_node = SpecificNode(Location([]), value_framework)

    def findNode(self, location_raw):
        loc = Location(location_raw)
        return self.main_node.getChild(loc)

class FunctionTree(Tree):
    def __init__(self, function):
        fw = {
            "Function": function,
            "Value": None
        }
        super().__init__(fw, CallableNode)

    def __call__(self, *args, **kwargs):
        return self.main_node(*args, **kwargs)


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


def getLeafValues(keys, **kwargs):
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

            dict_return[key] = values_list

    return dict_return

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


