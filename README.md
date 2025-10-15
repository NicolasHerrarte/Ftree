# Ftree
Tree library for visualization of trees

Location: Class which holds functions for facilitating moving around tree nodes
---
It has an array of integers in the form [l, l1, l2]

Node: Regular Node that hold an array of Nodes as children
---
You can call recursive functions on nodes to get specific outputs

Tree: Object which holds a main node
---
You can get any child node by calling its child locator function with a locator object

CallableNode: Implementation of node which can turn a recursive function into a tree
---
Call the node as if calling the option to get the output

FunctionTree: Implementation of tree which turns a recursive function into its tree form
---
Call the tree as if calling the option to get the output

More tree types can be implemented like: directory trees, hierarchical trees, searching trees, etc.

