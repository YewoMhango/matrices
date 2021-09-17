class Matrix:
    def __init__(self, width: int, height: int, elements: list = []):
        self.width = int(width)
        self.height = int(height)

        if self.width < 1:
            raise ValueError("Invalid negative width: " + str(width))
        if self.height < 1:
            raise ValueError("Invalid negative height: " + str(height))

        self.__elements = [0 for _ in range(width * height)]

        for i in range(len(elements)):
            self.__elements[i] = elements[i]

    def get(self, x: int, y: int):
        """
        Returns a value at the given (x,y) index where x is the column 
        and y is the row, counting from left to right and top to bottom, respectively
        """
        if type(x) != int or x >= self.width or x < 0:
            raise ValueError("Invalid index: " + str(x))
        if type(y) != int or y >= self.height or y < 0:
            raise ValueError("Invalid index: " + y)

        return self.__elements[self.width * y + x]

    def set(self, x: int, y: int, value):
        """
        Sets the value at the given (x,y) index to the given value, where x 
        is the column and y is the row, counting from left to right and top to bottom, 
        respectively
        """
        if type(x) != int or x >= self.width or x < 0:
            raise ValueError("Invalid index: " + x)
        if type(y) != int or y >= self.height or y < 0:
            raise ValueError("Invalid index: " + y)

        if value % 1 == 0:
            value = int(value)

        self.__elements[self.width * y + x] = value

    def __add__(self, other):
        """
        Returns the sum of `self` and `other` 
        """
        if self.width != other.width or self.height != other.height:
            raise ValueError(
                "Both matrices need to have the same dimensions")

        newMatrix = Matrix(self.width, self.height)

        for i in range(self.width):
            for j in range(self.height):
                newMatrix.set(i, j,  self.get(i, j) + other.get(i, j))

        return newMatrix

    def __sub__(self, other):
        """
        Returns the difference of `self` and `other` 
        """
        if self.width != other.width or self.height != other.height:
            raise ValueError(
                "Both matrices need to have the same dimensions")

        newMatrix = Matrix(self.width, self.height)

        for i in range(self.width):
            for j in range(self.height):
                newMatrix.set(i, j,  self.get(i, j) - other.get(i, j))

        return newMatrix

    def __mul__(self, other):
        """
        Returns the multiple of `self` and `other`
        """
        if self.width != other.height:
            raise ValueError(
                "Number of columns of A needs to be equal to number of rows of B")

        resultingWidth = other.width
        resultingHeight = self.height

        result = Matrix(resultingWidth, resultingHeight)

        numbers = self.width

        for i in range(resultingWidth):
            for j in range(resultingHeight):
                sum = 0
                for n in range(numbers):
                    sum += self.get(n, j) * other.get(i, n)
                result.set(i, j, sum)

        return result

    def __str__(self) -> str:
        """
        Returns a string representation of the matrix
        """
        columnWidths = [0 for x in range(self.width)]

        for i in range(self.width):
            for j in range(self.height):
                columnWidths[i] = max(columnWidths[i], len(
                    str(self.get(i, j))))

        totalWidth = 1

        for x in columnWidths:
            totalWidth += x + 1

        string = "\n┌" + (" " * totalWidth) + "┐\n"

        for j in range(self.height):
            string += "│"
            for i in range(self.width):
                string += leftpad(self.get(i, j), columnWidths[i] + 1)
            string += " │\n"

        string += "└" + (" " * totalWidth) + "┘\n"

        return string

    def transpose(self):
        """
        Returns the transpose of `self`
        """
        newMatrix = Matrix(self.height, self.width)

        for i in range(self.width):
            for j in range(self.height):
                newMatrix.set(j, i, self.get(i, j))

        return newMatrix

    def clone(self):
        """
        Returns a clone of `self`, with the same values as `self`
        """
        newMatrix = Matrix(self.width, self.height)

        for x in range(self.width):
            for y in range(self.height):
                newMatrix.set(x, y, self.get(x, y))

        return newMatrix

    def swapRows(self, first: int, second: int):
        """
        Returns a new matrix, with the rows indicated by 
        `first` and `second` swapped
        """
        newMatrix = self.clone()

        for x in range(self.width):
            newMatrix.set(x, first, self.get(x, second))
            newMatrix.set(x, second, self.get(x, first))

        return newMatrix


def leftpad(value, length: int, padding: str = " ") -> str:
    """
    Returns a string of length `length` or more, padded with 
    the value of `padding` at its beginning
    """
    if len(str(value)) >= length:
        return str(value)

    return padding * (length - len(str(value))) + str(value)


# A = Matrix(2, 2,
#            [1, 2,
#             3, 4])
# B = Matrix(3, 2,
#            [5, 6, 7,
#             8, 9, 10])

# print("A:", A)
# print("B:", B)
# print("A × B:", A * B)

# C = Matrix(2, 2,
#            [3, 1,
#             2, 1])
# CInverse = Matrix(2, 2,
#                   [1, -1,
#                    -2, 3])

# print("C:", C)
# print("C⁻¹:", CInverse)
# print("C × C⁻¹:", C * CInverse)


def gaussJordanElimination(left: Matrix, right: Matrix) -> Matrix:
    """
    Augments the `left` and `right` matrices and performs row operations 
    on it until the `left` matrix becomes an identity matrix.

    This serves multiple purposes as it can be used for finding the 
    inverse of the left matrix or solving a system of equations as in
    Gaussian Elimination
    """
    def augmentedMatrixAsString(matrix: Matrix) -> str:
        """
        Returns a string representation of the augmented matrix
        """
        columnWidths = [0 for x in range(matrix.width)]

        for i in range(matrix.width):
            for j in range(matrix.height):
                columnWidths[i] = max(columnWidths[i], len(
                    str(matrix.get(i, j))))

        totalWidth = 3

        for x in columnWidths:
            totalWidth += x + 1

        string = "\n┌" + (" " * totalWidth) + "┐\n"

        for j in range(matrix.height):
            string += "│"
            for i in range(matrix.width):
                if i == matrix.height:
                    string += " │"
                string += leftpad(matrix.get(i, j), columnWidths[i] + 1)
            string += " │\n"

        string += "└" + (" " * totalWidth) + "┘\n"

        return string

    if type(left) != Matrix or type(right) != Matrix:
        raise TypeError("Arguments should be Matrices")

    if left.width != left.height:
        raise ValueError("Left matrix should be a square matrix")

    if left.height != right.height:
        raise ValueError(
            "The matrices should have the same number of rows")

    # Creating an augmented matrix of the two
    augmentedMatrix = Matrix(left.width + right.width, left.height)

    for x in range(left.width):
        for y in range(left.height):
            augmentedMatrix.set(x, y, left.get(x, y))

    for x in range(left.width, augmentedMatrix.width):
        for y in range(right.height):
            augmentedMatrix.set(x, y, right.get(x - left.width, y))

    # For each row from top to bottom...
    for r in range(augmentedMatrix.height - 1):
        if augmentedMatrix.get(r, r) == 0:
            for i in range(r + 1, augmentedMatrix.height):
                if augmentedMatrix.get(r, i) != 0:
                    augmentedMatrix = augmentedMatrix.swapRows(r, i)
                    break

        # If the value is still zero, it means the values below it are all zeros too
        if augmentedMatrix.get(r, r) != 0:
            if augmentedMatrix.get(r, r) != 1:
                divisor = augmentedMatrix.get(r, r)
                for i in range(r, augmentedMatrix.width):
                    augmentedMatrix.set(
                        i, r, augmentedMatrix.get(i, r) / divisor)

            for i in range(r + 1, augmentedMatrix.height):
                if augmentedMatrix.get(r, i) != 0:
                    multiple = -augmentedMatrix.get(r, i)
                    for j in range(r, augmentedMatrix.width):
                        augmentedMatrix.set(j, i, augmentedMatrix.get(
                            j, i) + (augmentedMatrix.get(j, r) * multiple))

    # For each row from bottom to top...
    for r in reversed(range(1, augmentedMatrix.height)):
        if augmentedMatrix.get(r, r) == 0:
            for i in reversed(range(0, r)):
                if augmentedMatrix.get(r, i) != 0:
                    augmentedMatrix = augmentedMatrix.swapRows(r, i)
                    break

        # If the value is still zero, it means the values above it are all zeros too
        if augmentedMatrix.get(r, r) != 0:
            if augmentedMatrix.get(r, r) != 1:
                divisor = augmentedMatrix.get(r, r)
                for i in range(r, augmentedMatrix.width):
                    augmentedMatrix.set(
                        i, r, augmentedMatrix.get(i, r) / divisor)

            for i in reversed(range(0, r)):
                if augmentedMatrix.get(r, i) != 0:
                    multiple = -augmentedMatrix.get(r, i)
                    for j in range(r, augmentedMatrix.width):
                        augmentedMatrix.set(j, i, augmentedMatrix.get(
                            j, i) + (augmentedMatrix.get(j, r) * multiple))

    print(augmentedMatrixAsString(augmentedMatrix))

    solution = Matrix(right.width, right.height)

    for x in range(left.width, augmentedMatrix.width):
        for y in range(augmentedMatrix.height):
            solution.set(x - left.width, y, augmentedMatrix.get(x, y))

    return solution


# D = Matrix(3, 3,
#            [1, 2, 3,
#             3, 1, -3,
#             -3, 4, 7])
# E = Matrix(1, 3,
#            [-5,
#             4,
#             -7])
# print(GaussJordanElimination(D, E))


def findInverseMatrix(matrix: Matrix) -> Matrix:
    if type(matrix) != Matrix:
        raise Exception("Input needs to be a matrix")
    if matrix.width != matrix.height:
        raise Exception("Input needs to be a square matrix")

    identityMatrix = Matrix(matrix.width, matrix.height)

    for i in range(matrix.width):
        identityMatrix.set(i, i, 1)

    return gaussJordanElimination(matrix, identityMatrix)


def enterMatrix(width: int, height: int, message: str = "Enter the values of your matrix separated by commas: ") -> Matrix:
    values = eval(
        "[" + input(message) + "]")

    if len(values) != width * height:
        raise ValueError("You needed to enter " +
                         str(width * height) + " elements")

    return Matrix(width, height, values)


def main():
    while True:
        choice = int(input("""Choose which type of operation you want to perform:

    1. Multiply two matrices
    2. Find the transpose of a matrix
    3. Find inverse of a matrix 
    4. Solve a system of equations using Gauss-Jordan elimination
    5. Exit

> """))

        if choice == 1:
            height = int(input("Enter the height of your first matrix: "))
            width = int(input("Enter the width of your first matrix: "))

            A = enterMatrix(width, height)

            print(A)

            height = int(input("Enter the height of your second matrix: "))
            width = int(input("Enter the width of your second matrix: "))

            B = enterMatrix(width, height)

            print(B)

            print("A × B: ", A * B)

        elif choice == 2:
            height = int(input("Enter the height of your matrix: "))
            width = int(input("Enter the width of your matrix: "))

            A = enterMatrix(width, height)
            print(A)

            print("Transpose:", A.transpose())

        elif choice == 3:
            height = int(input("Enter the height of your matrix: "))

            A = enterMatrix(height, height)
            print(A)

            print("Inverse matrix:", findInverseMatrix(A))

        elif choice == 4:
            height = int(input("Enter the height of your matrix: "))

            A = enterMatrix(height, height)
            print(A)

            B = enterMatrix(
                1, height, "Enter the values of the answer column matrix: ")
            print(B)

            print("Solutions:", gaussJordanElimination(A, B))

        elif choice == 5:
            break

        else:
            print("Invalid value!")

        yesOrNo = input("Continue? (y/n): ")

        if not yesOrNo.lower().startswith("y"):
            break


if __name__ == "__main__":
    main()
