from Tree import *
def fibonacci(n, **kwargs):
    parent = kwargs["parent"]
    n = int(n)
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        new_child1 = parent.addChild(CallableNode)
        new_child2 = parent.addChild(CallableNode)
        return new_child1(n-1) + new_child2(n-2)

ftree = FunctionTree(fibonacci)
#print(ftree(10))
str_ftree, _ = ftree.recursiveCall(Tree.Recursion.printNode,
                                            location_raw=[],
                                            function_args={
                                                "value_key": "Value"
                                            })
##print(str_ftree)


binary = BinarySearchTree(BinarySearchTree.Comparison.greaterThan)
binary.addElements(["banana", "peach", "apple", "pear", "coconut", "mango", "papaya"])

#print(binary.getElements(["chemistry", "Flikker op"]))
str_ftree, _ = binary.recursiveCall(Tree.Recursion.printNode,
                                            location_raw=[],
                                            function_args={
                                                "value_key": "Value"
                                            })

_all, _ = binary.recursiveCall(Tree.Recursion.getAllValues,
                                            location_raw=[],
                                            function_args={
                                                "keys": ["Value"]
                                            })
print(_all)
print(str_ftree)




