def treeBFS(root, target):

    # Return nothing in the tree does not exist, is null
    if root is None:
        return None

    # If the tree has at least one root node, add it to the queue to process
    queue = []
    queue.append(root)

    # Check the root node, then add its children to check, and continue to add child elements of other nodes to check.
    while len(queue) > 0:
        currentElement = queue[0]

        # if the current node we're considering has a value equal to the target, return that node
        if currentElement.value == target:
            return currentElement

        # Add child nodes to the list to process
        for eachChild in currentElement.children:
            queue.append(eachChild)

        # Remove the least recently discovered element so we go the list in FIFO order (First In, First Out).
        queue.pop(0)