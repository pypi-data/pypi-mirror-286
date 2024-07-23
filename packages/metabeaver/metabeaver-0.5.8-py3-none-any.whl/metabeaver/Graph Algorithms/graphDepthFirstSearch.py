def graphDepthFirstSearch(root, target, visited):

    if root == None:
        return root

    if root.value == target:
        return root

    for eachNeighbour in root.neighbours:
        if eachNeighbour not in visited:
            visited.append(root)
            result = graphDepthFirstSearch(eachNeighbour, target, visited)
            if result is not None:
                return result




























