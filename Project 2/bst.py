# BST Variation 2

from __future__ import annotations
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        : int  = None,
                  value      : int  = None,
                  leftchild  : Node = None,
                  rightchild : Node = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# For the tree rooted at root:
# Return the json.dumps of the list with indent=2.
# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key"        : node.key,
            "value"      : node.value,
            "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)



# For the tree rooted at root and the key and value given:
# Insert the key/value pair.
# The key is guaranteed to not be in the tree.
# Follow the variation rules as per the PDF.
def insert(root: Node, key: int, value: int) -> Node:
    
    # Empty tree
    if root is None:
        return Node(key=key, value=value)

    curr = root
    k, v = key, value # the pair being inserted
    while True:
        #  k must be > max value of left subtree and < min value of right subtree
        can_left_ok = True
        if curr.leftchild is not None:
            # max in left subtree = go right-most
            lm = curr.leftchild
            while lm.rightchild is not None:
                lm = lm.rightchild
            can_left_ok = (k > lm.key)

        can_right_ok = True
        if curr.rightchild is not None:
            # min in right subtree = go left-most
            rm = curr.rightchild
            while rm.leftchild is not None:
                rm = rm.leftchild
            can_right_ok = (k < rm.key)

        if can_left_ok and can_right_ok:
            # place (k,v) at current node, push the old (k,v) down towards the side implied by the new key.
            old_k, old_v = curr.key, curr.value
            curr.key, curr.value = k, v

            # Continue inserting the old key in the proper direction
            if old_k < curr.key:
                # go left with old_k
                if curr.leftchild is None:
                    curr.leftchild = Node(key=old_k, value=old_v)
                    break
                else:
                    curr = curr.leftchild
                    k, v = old_k, old_v
                    continue
            else:
                # go right with old_k
                if curr.rightchild is None:
                    curr.rightchild = Node(key=old_k, value=old_v)
                    break
                else:
                    curr = curr.rightchild
                    k, v = old_k, old_v
                    continue
        else:
            # Not safe to replace
            if k < curr.key:
                if curr.leftchild is None:
                    curr.leftchild = Node(key=k, value=v)
                    break
                curr = curr.leftchild
            else:
                if curr.rightchild is None:
                    curr.rightchild = Node(key=k, value=v)
                    break
                curr = curr.rightchild

    return root

# For the tree rooted at root and the key given, delete the key.
# Follow the variation rules as per the PDF.
def delete(root: Node, key: int) -> Node:
    
    # Find the curr node to delete and its parent
    parent = None
    curr = root
    while curr is not None and curr.key != key:
        parent = curr
        if key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild

    if curr is None:
        return root

    # node has 0 or 1 child
    if curr.leftchild is None or curr.rightchild is None:
        child = curr.leftchild if curr.leftchild is not None else curr.rightchild
        if parent is None:
            # deleting the root
            return child
        if parent.leftchild is curr:
            parent.leftchild = child
        else:
            parent.rightchild = child
        return root

    # node has two children
    size_left = 0
    stack = [curr.leftchild]
    while stack:
        n = stack.pop()
        if n is None: 
            continue
        size_left += 1
        if n.leftchild is not None:
            stack.append(n.leftchild)
        if n.rightchild is not None:
            stack.append(n.rightchild)

    size_right = 0
    stack = [curr.rightchild]
    while stack:
        n = stack.pop()
        if n is None:
            continue
        size_right += 1
        if n.leftchild is not None:
            stack.append(n.leftchild)
        if n.rightchild is not None:
            stack.append(n.rightchild)

    if size_left > size_right:
        # Use inorder predecessor
        rep_parent = curr
        rep = curr.leftchild
        while rep.rightchild is not None:
            rep_parent = rep
            rep = rep.rightchild

        curr.key, curr.value = rep.key, rep.value

        # Remove the predecessor node
        if rep_parent is curr:
            rep_parent.leftchild = rep.leftchild
        else:
            rep_parent.rightchild = rep.leftchild
    else:
        # Use inorder successor
        rep_parent = curr
        rep = curr.rightchild
        while rep.leftchild is not None:
            rep_parent = rep
            rep = rep.leftchild

        curr.key, curr.value = rep.key, rep.value

        # Remove the successor node
        if rep_parent is curr:
            rep_parent.rightchild = rep.rightchild
        else:
            rep_parent.leftchild = rep.rightchild

    return root

# For the tree rooted at root and the key given:
# Calculate the list of values on the path from the root down to and including the search key node.
# The key is guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    # Remove the next line and fill in code to construct value_list.
    value_list = []
    curr = root

    while curr is not None:
        value_list.append(curr.value)
        if search_key == curr.key:
            break
        elif search_key < curr.key:
            curr = curr.leftchild
        else:
            curr = curr.rightchild
    return json.dumps(value_list, indent=2)