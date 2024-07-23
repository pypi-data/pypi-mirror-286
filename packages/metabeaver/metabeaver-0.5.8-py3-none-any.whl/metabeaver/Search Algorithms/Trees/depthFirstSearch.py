# Do depth-first search on a tree
def treeDFS(root, target):

    # Returns None right away if passed an empty tree - non creato ex nihilo. Returns None we when hit empty children.
    if root is None:
        return None

    # Return the root if first node contains it, or pass first child matching back to parent recursive call.
    if root.value == target:
        return root

    # Go left and return None or a Node matching the target value to this function.
    left = treeDFS(root.left, target)
    if left is not None:
        return left

    # If the left hand recursion and parent did not contain the target, search to the right.
    return treeDFS(root.right, target)


























