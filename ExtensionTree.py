from Tree import *

#Temporal
import sys
sys.path.insert(0, "../RSA")

from Discrete import *

class EulerTree(FunctionTree):
    def __init__(self):
        super().__init__(self.gcd_r)
        self.gcd = None
        self.gcd_tree = None
        self.bezoet_coefs = None
        self.bezoet_tree = None
        self.inverted = False

    def gcd_r(self, num, **kwargs):
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

    def calc_bezout_coefs(self):
        if self.called:
            fout, cache_tree = self.recursiveCall(EulerTree.bezout_coefs_r,
                                                     filter_function=Tree.Filtering.valueEquality,
                                                     filtering_args={
                                                         "key": "Type",
                                                         "value": "Principal"
                                                     })
            self.bezoet_tree = cache_tree
            invert = cache_tree.findNode([]).getValue("Cache")
            if invert:
                final_coefs = (-fout[1], fout[0])
            else:
                final_coefs = (fout[0], -fout[1])

            self.bezoet_coefs = final_coefs
            return final_coefs

    def calc_gcd(self, num1, num2):
        self((num1, num2))
        dict_gcd, _ = self.recursiveCall(Tree.Recursion.getLeafValues,
                                         function_args={
                                             "keys": ["Value"]
                                         },
                                         count_inactive=True)
        self.gcd = dict_gcd["Value"][0]
        return self.gcd

    @staticmethod
    def bezout_coefs_r(**kwargs):
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
        if node_obj.amountActiveChildren() > 0:
            if recursive_depth == 1:
                direction = False
                return current_bezout, direction
            else:
                previous_bezout = kwargs["children_outputs"][0]
                direction = not recursive_node.children[0].getValue("Cache")

                new_bezout = bezout_next(previous_bezout, current_bezout, direction)
                #print("---")
                #print(previous_bezout)
                #print(current_bezout)
                #print(new_bezout)
                return new_bezout, direction

class ModularNumber():
    def __init__(self, n, modulo):
        etree = EulerTree()
        self.gcd = etree.calc_gcd(n, modulo)
        self.coefs = etree.calc_bezout_coefs()
        self.invertible = (self.gcd == 1)
        self.m_inverse = None
        if self.invertible:
            self.m_inverse = self.coefs[0]

mod101_4620 = ModularNumber(101,4620)
print(mod101_4620.m_inverse)

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
"""
fout, cache_tree = gcdtree.recursiveCall(bezout_coefs,
                            filter_function=Tree.Filtering.valueEquality,
                            filtering_args={
                                "key": "Type",
                                "value": "Principal"
                            })
print(fout, cache_tree.findNode([]).getValue("Cache"))
"""
