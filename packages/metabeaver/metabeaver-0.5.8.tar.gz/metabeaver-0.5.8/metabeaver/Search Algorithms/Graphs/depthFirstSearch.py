# Graph depth-first search
def graphDFS(root, visited, target):

    # Return None if graph is None: graph does not exist
    if root is None:
        return None
    # Return the node that we found the target value at, if we found a match
    if root.value == target:
        return root

    # Assume an iterable object exists in the root node - .children - which contains child nodes
    for eachChild in root.children:
        if eachChild in visited:
            continue
        visited.append(eachChild)

        # If we return something from exploring the child(ren), once it is returned to highest function, return it.
        result = graphDFS(eachChild) # We need to capture this return as the value is passed up the stack to here!
        # We've either returned None or the Node that had the matching value.
        if result:
            # If we did find a non-None value, we return the Node it was found in.
            return result

    # If the target was not found in any child node in the graph we return None
    return None # Python functions automatically return None! Included to clarify the code.

# Example showing a search through a graph, which includes a cycle, using our graphDFS



















