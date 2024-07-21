from enum import Enum

class Operations(Enum):
    Addition = 'addition'
    Subtration = 'subtraction'
    Multiplication = 'multiplication'

class Matrix_Manipulation:

    def check_matrices_validity_for(self, operation: str, mat_1, mat_2):
        # check for addition and subtraction
        if operation == Operations.Addition or operation == Operations.Subtration:
           if len(mat_1) != len(mat_2):
                return False
           for i in range(len(mat_1)):
                if len(mat_1[i]) != len(mat_2[i]):
                    return False
           return True
        
        # check for multiplication validation
        if operation == Operations.Multiplication:
            rows_in_mat_1 = len(mat_1)
            cols_in_mat_2 = len(mat_2[0])

            # the below loop checks if all the row contain same elements
            for row in mat_2:
                if len(row) != cols_in_mat_2:
                    return False

            if rows_in_mat_1 != cols_in_mat_2:
                return False
            
            return True
    
    def add_matrix(self, mat_1, mat_2):
        if self.check_matrices_validity_for(Operations.Addition, mat_1, mat_2) == False :
             return "Invalid Matrices"
        for i in range(len(mat_1)):
            for j in range(len(mat_1[i])):
                mat_1[i][j] += mat_2[i][j]

        return mat_1            
        
    def subtract_matrix(self, mat_1, mat_2):
        if self.check_matrices_validity_for(Operations.Subtration, mat_1, mat_2) == False :
             return "Invalid Matrices"
        for i in range(len(mat_1)):
            for j in range(len(mat_1[i])):
                mat_1[i][j] -= mat_2[i][j]

        return mat_1            

    def multiply_matrices(self, mat_1, mat_2):
        if self.check_matrices_validity_for(Operations.Multiplication, mat_1, mat_2)  == False:
            return "Invalid matrices"          
        else: 
            new_matrix = [[0 for _ in row] for row in mat_1]
            for i in range(len(mat_1)):
                for j in range(len(mat_2[0])):
                    for k in range(len(mat_1[0])):
                        new_matrix[i][j] += mat_1[i][k] * mat_2[k][j]
            return new_matrix

    def transpose(self, matrix):
        new_matrix = [[0 for _ in row] for row in matrix]   
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                new_matrix[i][j] = matrix[j][i]
        return new_matrix