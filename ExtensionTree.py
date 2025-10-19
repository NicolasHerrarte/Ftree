from Tree import *

#Temporal
import sys
sys.path.insert(0, "../RSA")

from Discrete import *

class EulerTree(FunctionTree):
    def __init__(self):
        super().__init__(self.GCD_R)

    def GCD_R(self, num, **kwargs):
        parent = kwargs["parent"]
        if not parent.isActive():
            return num

        n1, n2 = num
        parent = kwargs["parent"]
        quotient, rem = remainderDivision(n1, n2)

        child1 = parent.addChild(CallableNode)
        child1.setValue("Principal", "Type")
        if rem != 0:
            child1((n2, rem))
        else:
            child1.setOff()
            child1(n2)
        child2 = parent.addChild(CallableNode)
        child2.setValue("Coef", "Type")
        child2.setOff()
        child2(quotient)
        child3 = parent.addChild(CallableNode)
        child3.setValue("Remainder", "Type")
        child3.setOff()
        child3(rem)

        return n1

def bezout_coefs(**kwargs):
    def bezout_next(previous, current, direction):
        multiplier = previous[direction]
        swap_coefs = [x * multiplier for x in current]
        coefs = [0, 0]
        coefs[not direction] = swap_coefs[1] + previous[not direction]
        coefs[direction] = swap_coefs[0]
        return tuple(coefs)

    node_obj = kwargs["itself"]
    recursive_node = kwargs["node"]
    recursive_depth = recursive_node.recursive_call(Tree.Recursion.getMaxDepth)


    coef_node = node_obj.getFilteredChildren(Tree.Filtering.valueEquality, key="Type", value="Coef")[0]
    coef = coef_node.getValue("Value")
    current_bezout = (1, coef)
    #print(node_obj.amountActiveChildren())
    #print(recursive_depth)
    if node_obj.amountActiveChildren() > 0:
        if recursive_depth == 1:
            direction = False
            return current_bezout, direction
        else:
            previous_bezout = kwargs["children_outputs"][0]
            direction = not recursive_node.children[0].getValue("Cache")

            new_bezout = bezout_next(previous_bezout, current_bezout, direction)
            print("---")
            print(previous_bezout)
            print(current_bezout)
            print(new_bezout)
            return new_bezout, direction


gcdtree = EulerTree()
gcdtree((9834, 387))
"""
_all = gcdtree.main_node.recursive_call(Tree.Recursion.getAllValues,
                                        function_args={
                                            "keys": ["Value"]
                                        },
                                        count_inactive=True)
_all2 = gcdtree.recursiveCall(Tree.Recursion.getAllValues,
                                        location_raw=[0],
                                        function_args={
                                            "keys": ["Value"]
                                        },
                                        count_inactive=True)
"""
#print(gcdtree.findNode([]).recursive_call(Tree.Recursion.getAmountChildren, count_inactive=True))
#ans, cache_tree = gcdtree.recursiveCall(Tree.Recursion.getMaxDepth)
#print(ans, cache_tree.findNode([0,0,0]).value["Cache"])
#l = []
#print(gcdtree.findNode(l).isActive())
#print(gcdtree.findNode(l).value["Value"])
#print(gcdtree.findNode(l).amountActiveChildren())
#print("---")
fout, cache_tree = gcdtree.recursiveCall(bezout_coefs,
                            filter_function=Tree.Filtering.valueEquality,
                            filtering_args={
                                "key": "Type",
                                "value": "Principal"
                            })
print(fout, cache_tree.findNode([]).getValue("Cache"))
