def fibonacci(n):

    """
    Fn ≈ 1/√5 * ϕ^n
    The nth number in the Fibonacci series is approximately equal to (1 divided by sqrt(5)) * (golden ratio ^ n)
    """

    if n == 0:
        return 0
    if n == 1:
        return 1

    if n > 1:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacciSeries(n):

    # Initalise the first two numbers in the fib sequence
    a, b = 0, 1

    # Move value of b to the left, to a. Update value of b to itself plus whatever a is now. 0,1 -> 1,1 -> 1,2, -> 2,3..
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacciSeries(5):
    print(num)

"""
def treeDepthFirstSearch(root, target):

    # If the start tree was EMPTY can not creato ex nihilo, so return None. Return None when children do not exist.
    if root is None or root.value == target:
        return root

    # Go left. Will return a node IF AND ONLY IF we found a node whose .value property is equal to the target
    left = treeDepthFirstSearch(root.left, target)
    if left is not None:
        return left

    # Go right and either return a node that matched the value or some series of None.
    return treeDepthFirstSearch(root.right, target)
"""





















