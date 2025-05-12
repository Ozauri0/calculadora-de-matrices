#!/usr/bin/env python3
"""
Calculadora de Matrices
Una calculadora basada en consola para operaciones matriciales y métodos numéricos.

Autor: [Tu nombre]
Fecha: Mayo 2025
"""

def print_matrix(matrix, precision=4):
    """
    Muestra una matriz en un formato legible.
    
    Args:
        matrix: La matriz a mostrar
        precision: Precisión decimal para números de punto flotante
    """
    if not matrix:
        print("Matriz vacía")
        return
        
    # Encuentra el ancho máximo necesario para cada columna
    max_widths = []
    for j in range(len(matrix[0])):
        col_width = max(len(f"{round(matrix[i][j], precision):.{precision}f}") for i in range(len(matrix)))
        max_widths.append(col_width)
    
    # Imprime la matriz con formato adecuado
    print()
    for i in range(len(matrix)):
        print("  [", end="")
        for j in range(len(matrix[i])):
            num = matrix[i][j]
            # Formatea números como enteros si son números enteros
            if abs(num - round(num)) < 1e-10:
                formatted = f"{int(num):>{max_widths[j]}}"
            else:
                formatted = f"{num:>{max_widths[j]}.{precision}f}"
            print(f" {formatted}", end="")
        print(" ]")
    print()

def get_integer_input(prompt, min_val=None, max_val=None):
    """
    Obtiene una entrada de entero validada del usuario.
    
    Args:
        prompt: El mensaje de solicitud a mostrar
        min_val: Valor mínimo aceptable (inclusive)
        max_val: Valor máximo aceptable (inclusive)
        
    Returns:
        Un entero dentro del rango especificado
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Error: El valor debe ser al menos {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Error: El valor debe ser como máximo {max_val}.")
                continue
            return value
        except ValueError:
            print("Error: Por favor ingrese un entero válido.")

def get_float_input(prompt):
    """
    Obtiene una entrada de número flotante validada del usuario.
    
    Args:
        prompt: El mensaje de solicitud a mostrar
        
    Returns:
        Un número de punto flotante
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Por favor ingrese un número válido.")

def input_matrix():
    """
    Toma la entrada del usuario para crear una matriz.
    
    Returns:
        Una lista 2D que representa la matriz
    """
    print("\nIngrese las dimensiones de la matriz (1-4):")
    rows = get_integer_input("Número de filas: ", 1, 4)
    cols = get_integer_input("Número de columnas: ", 1, 4)
    
    matrix = []
    print(f"\nIngrese los elementos de la matriz {rows}x{cols}:")
    
    for i in range(rows):
        row = []
        for j in range(cols):
            value = get_float_input(f"Elemento en la posición ({i+1},{j+1}): ")
            row.append(value)
        matrix.append(row)
    
    print("\nMatriz ingresada:")
    print_matrix(matrix)
    return matrix

def get_matrix_dimensions(matrix):
    """
    Obtiene las dimensiones de una matriz.
    
    Args:
        matrix: La matriz a medir
        
    Returns:
        Una tupla (filas, columnas)
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    return rows, cols

def add_matrices(matrix1, matrix2):
    """
    Suma dos matrices elemento por elemento.
    
    Args:
        matrix1: Primera matriz
        matrix2: Segunda matriz
        
    Returns:
        La matriz resultante o None si las dimensiones son incompatibles
    """
    rows1, cols1 = get_matrix_dimensions(matrix1)
    rows2, cols2 = get_matrix_dimensions(matrix2)
    
    if rows1 != rows2 or cols1 != cols2:
        print(f"Error: No se pueden sumar matrices de dimensiones {rows1}x{cols1} y {rows2}x{cols2}.")
        print("Las matrices deben tener las mismas dimensiones para la suma.")
        return None
    
    result = []
    
    # Mostrar los pasos de la suma
    print("\nPasos de la suma:")
    
    for i in range(rows1):
        row = []
        for j in range(cols1):
            element = matrix1[i][j] + matrix2[i][j]
            calculation = f"Elemento en la posición ({i+1},{j+1}) = {matrix1[i][j]} + {matrix2[i][j]} = {element}"
            print(calculation)
            row.append(element)
        result.append(row)
    
    return result

def subtract_matrices(matrix1, matrix2):
    """
    Resta la matriz2 de la matriz1 elemento por elemento.
    
    Args:
        matrix1: Primera matriz
        matrix2: Segunda matriz
        
    Returns:
        La matriz resultante o None si las dimensiones son incompatibles
    """
    rows1, cols1 = get_matrix_dimensions(matrix1)
    rows2, cols2 = get_matrix_dimensions(matrix2)
    
    if rows1 != rows2 or cols1 != cols2:
        print(f"Error: No se pueden restar matrices de dimensiones {rows1}x{cols1} y {rows2}x{cols2}.")
        print("Las matrices deben tener las mismas dimensiones para la resta.")
        return None
    
    result = []
    
    # Mostrar los pasos de la resta
    print("\nPasos de la resta:")
    
    for i in range(rows1):
        row = []
        for j in range(cols1):
            element = matrix1[i][j] - matrix2[i][j]
            calculation = f"Elemento en la posición ({i+1},{j+1}) = {matrix1[i][j]} - {matrix2[i][j]} = {element}"
            print(calculation)
            row.append(element)
        result.append(row)
    
    return result

def multiply_matrices(matrix1, matrix2):
    """
    Multiplica dos matrices.
    
    Args:
        matrix1: Primera matriz
        matrix2: Segunda matriz
        
    Returns:
        La matriz resultante o None si las dimensiones son incompatibles
    """
    rows1, cols1 = get_matrix_dimensions(matrix1)
    rows2, cols2 = get_matrix_dimensions(matrix2)
    
    if cols1 != rows2:
        print(f"Error: No se pueden multiplicar matrices de dimensiones {rows1}x{cols1} y {rows2}x{cols2}.")
        print("Para la multiplicación de matrices, el número de columnas en la primera matriz debe ser igual al número de filas en la segunda matriz.")
        return None
    
    result = []
    print("\nPasos de la multiplicación:")
    
    for i in range(rows1):
        row = []
        for j in range(cols2):
            element = 0
            calculation = f"Elemento en la posición ({i+1},{j+1}) = "
            for k in range(cols1):
                element += matrix1[i][k] * matrix2[k][j]
                calculation += f"{matrix1[i][k]} * {matrix2[k][j]}"
                if k < cols1 - 1:
                    calculation += " + "
            calculation += f" = {element}"
            print(calculation)
            row.append(element)
        result.append(row)
    
    return result

def determinant(matrix):
    """
    Calcula el determinante de una matriz cuadrada de forma recursiva.
    
    Args:
        matrix: La matriz cuadrada
        
    Returns:
        El valor del determinante o None si la matriz no es cuadrada
    """
    rows, cols = get_matrix_dimensions(matrix)
    
    if rows != cols:
        print(f"Error: No se puede calcular el determinante de una matriz {rows}x{cols}.")
        print("La matriz debe ser cuadrada para calcular el determinante.")
        return None
    
    # Caso base: matriz 1x1
    if rows == 1:
        return matrix[0][0]
    
    # Caso base: matriz 2x2
    if rows == 2:
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        print(f"\nDeterminante de matriz 2x2 = ({matrix[0][0]} * {matrix[1][1]}) - ({matrix[0][1]} * {matrix[1][0]}) = {det}")
        return det
    
    # Caso recursivo: expandir a lo largo de la primera fila
    det = 0
    print("\nCalculando determinante por expansión a lo largo de la primera fila:")
    
    for j in range(cols):
        # Crear submatriz excluyendo primera fila y columna actual
        submatrix = []
        for i in range(1, rows):
            row = []
            for k in range(cols):
                if k != j:
                    row.append(matrix[i][k])
            submatrix.append(row)
        
        # Calcular cofactor
        sign = 1 if j % 2 == 0 else -1
        subdet = determinant(submatrix)
        det += sign * matrix[0][j] * subdet
        
        print(f"Término {j+1}: {sign} * {matrix[0][j]} * {subdet} = {sign * matrix[0][j] * subdet}")
    
    print(f"Determinante final = {det}")
    return det

def get_minor(matrix, row, col):
    """
    Calcula el menor de un elemento de la matriz (determinante de la submatriz).
    
    Args:
        matrix: La matriz cuadrada
        row: La fila a excluir
        col: La columna a excluir
        
    Returns:
        La matriz menor (con fila y columna eliminadas)
    """
    minor = []
    for i in range(len(matrix)):
        if i != row:
            minor_row = []
            for j in range(len(matrix[0])):
                if j != col:
                    minor_row.append(matrix[i][j])
            minor.append(minor_row)
    return minor

def gaussian_elimination(matrix, b=None, show_steps=True):
    """
    Aplica eliminación gaussiana para transformar una matriz a forma escalonada.
    
    Args:
        matrix: La matriz de coeficientes a transformar
        b: El vector de términos independientes (opcional)
        show_steps: Si se deben mostrar los pasos
        
    Returns:
        La matriz en forma escalonada y el vector b transformado
    """
    rows, cols = get_matrix_dimensions(matrix)
    # Crea una copia profunda de la matriz
    A = [row[:] for row in matrix]
    
    # Crea la matriz aumentada si se proporciona b
    if b is not None:
        for i in range(rows):
            A[i].append(b[i])
        cols += 1
    
    if show_steps:
        print("\nIniciando Eliminación Gaussiana:")
        if b is not None:
            print("Matriz aumentada:")
        print_matrix(A)
    
    # Eliminación hacia adelante
    for i in range(rows):
        # Encuentra la fila pivote
        max_row = i
        for k in range(i + 1, rows):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Intercambia la fila actual con la fila pivote si es necesario
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            if show_steps:
                print(f"Intercambiar filas {i+1} y {max_row+1}:")
                print_matrix(A)
        
        # Omite si el pivote es cero (matriz singular)
        if abs(A[i][i]) < 1e-10:
            continue
        
        # Elimina todas las filas debajo
        for j in range(i + 1, rows):
            try:
                factor = A[j][i] / A[i][i]
            except ZeroDivisionError:
                if show_steps:
                    print(f"Pivote en la posición ({i+1},{i+1}) es cero, omitiendo eliminación para esta columna.")
                continue
                
            if show_steps and abs(factor) > 1e-10:
                print(f"F{j+1} = F{j+1} - {factor:.4f} * F{i+1}")
                
            for k in range(i, cols):
                A[j][k] -= factor * A[i][k]
                
            if show_steps and abs(factor) > 1e-10:
                print_matrix(A)
    
    # Extrae el vector b transformado si fue proporcionado
    if b is not None:
        b_new = [row[-1] for row in A]
        for i in range(rows):
            A[i].pop()  # Elimina la última columna
        return A, b_new
    
    return A, None

def back_substitution(A, b):
    """
    Aplica sustitución hacia atrás para resolver el sistema Ax = b donde A está en forma escalonada.
    
    Args:
        A: La matriz de coeficientes en forma escalonada
        b: El vector de términos independientes
        
    Returns:
        El vector solución x
    """
    rows = len(A)
    x = [0] * rows
    
    print("\nSustitución hacia atrás:")
    
    for i in range(rows - 1, -1, -1):
        # Verificar si la fila es toda ceros
        if all(abs(A[i][j]) < 1e-10 for j in range(rows)):
            if abs(b[i]) < 1e-10:
                print(f"Fila {i+1} es toda ceros con término independiente cero (soluciones infinitas).")
                continue
            else:
                print(f"Fila {i+1} es toda ceros con término independiente no nulo (sin solución).")
                return None
        
        # Encontrar la columna pivote
        pivot_col = -1
        for j in range(rows):
            if abs(A[i][j]) > 1e-10:
                pivot_col = j
                break
        
        if pivot_col == -1:
            continue
        
        # Calcular el valor de x[pivot_col]
        sum_val = 0
        calculation = f"x{pivot_col+1} = ("
        
        calculation += f"{b[i]:.4f}"
        for j in range(pivot_col + 1, rows):
            if abs(A[i][j]) > 1e-10:
                sum_val += A[i][j] * x[j]
                calculation += f" - {A[i][j]:.4f} * {x[j]:.4f}"
        
        x[pivot_col] = (b[i] - sum_val) / A[i][pivot_col]
        calculation += f") / {A[i][pivot_col]:.4f} = {x[pivot_col]:.4f}"
        print(calculation)
    
    return x

def gauss_jordan_elimination(matrix, b=None, show_steps=True):
    """
    Aplica eliminación Gauss-Jordan para transformar una matriz a forma escalonada reducida.
    
    Args:
        matrix: La matriz de coeficientes a transformar
        b: El vector de términos independientes (opcional)
        show_steps: Si se deben mostrar los pasos
        
    Returns:
        La matriz en forma escalonada reducida y el vector b transformado
    """
    rows, cols = get_matrix_dimensions(matrix)
    # Crea una copia profunda de la matriz
    A = [row[:] for row in matrix]
    
    # Crea la matriz aumentada si se proporciona b
    if b is not None:
        for i in range(rows):
            A[i].append(b[i])
        cols += 1
    
    if show_steps:
        print("\nIniciando Eliminación Gauss-Jordan:")
        if b is not None:
            print("Matriz aumentada:")
        print_matrix(A)
    
    # Eliminación hacia adelante (similar a la eliminación gaussiana)
    for i in range(rows):
        # Encuentra la fila pivote
        max_row = i
        for k in range(i + 1, rows):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Intercambia la fila actual con la fila pivote si es necesario
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            if show_steps:
                print(f"Intercambiar filas {i+1} y {max_row+1}:")
                print_matrix(A)
        
        # Omite si el pivote es cero (matriz singular)
        if abs(A[i][i]) < 1e-10:
            continue
        
        # Escalar la fila pivote para hacer el pivote 1
        pivot = A[i][i]
        for j in range(i, cols):
            A[i][j] /= pivot
        
        if show_steps:
            print(f"F{i+1} = F{i+1} / {pivot:.4f}")
            print_matrix(A)
        
        # Eliminar todas las demás filas
        for j in range(rows):
            if j != i:
                factor = A[j][i]
                if abs(factor) < 1e-10:
                    continue
                    
                if show_steps:
                    print(f"F{j+1} = F{j+1} - {factor:.4f} * F{i+1}")
                
                for k in range(i, cols):
                    A[j][k] -= factor * A[i][k]
                
                if show_steps:
                    print_matrix(A)
    
    # Extrae el vector b transformado si fue proporcionado
    if b is not None:
        b_new = [row[-1] for row in A]
        for i in range(rows):
            A[i].pop()  # Elimina la última columna
        return A, b_new
    
    return A, None

def calculate_inverse(matrix):
    """
    Calcula la inversa de una matriz cuadrada usando eliminación Gauss-Jordan.
    
    Args:
        matrix: La matriz cuadrada a invertir
        
    Returns:
        La matriz inversa o None si la matriz es singular o no cuadrada
    """
    rows, cols = get_matrix_dimensions(matrix)
    
    if rows != cols:
        print(f"Error: No se puede calcular la inversa de una matriz {rows}x{cols}.")
        print("La matriz debe ser cuadrada para calcular la inversa.")
        return None
    
    # Verificar el determinante
    det = determinant(matrix)
    if abs(det) < 1e-10:
        print("Error: La matriz es singular (determinante es cero), por lo que no tiene inversa.")
        return None
    
    # Crear una matriz identidad del mismo tamaño
    identity = []
    for i in range(rows):
        row = []
        for j in range(rows):
            row.append(1 if i == j else 0)
        identity.append(row)
    
    print("\nCalculando inversa usando eliminación Gauss-Jordan")
    print("Matriz original (A):")
    print_matrix(matrix)
    print("Matriz identidad (I):")
    print_matrix(identity)
    
    # Aumentar la matriz con la identidad
    A = [row[:] for row in matrix]
    for i in range(rows):
        A[i].extend(identity[i])
    
    print("Matriz aumentada [A|I]:")
    print_matrix(A)
    
    # Aplicar eliminación Gauss-Jordan
    n = rows
    for i in range(n):
        # Encontrar el elemento pivote máximo
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Intercambiar filas si es necesario
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            print(f"Intercambiar filas {i+1} y {max_row+1}:")
            print_matrix(A)
        
        # Verificar singularidad
        if abs(A[i][i]) < 1e-10:
            print("Error: La matriz es singular, la inversa no existe.")
            return None
        
        # Escalar la fila pivote para hacer el pivote 1
        pivot = A[i][i]
        for j in range(2*n):
            A[i][j] /= pivot
        
        print(f"F{i+1} = F{i+1} / {pivot:.4f}")
        print_matrix(A)
        
        # Eliminar todas las demás filas
        for j in range(n):
            if j != i:
                factor = A[j][i]
                if abs(factor) < 1e-10:
                    continue
                
                print(f"F{j+1} = F{j+1} - {factor:.4f} * F{i+1}")
                
                # Cálculo mejorado con mejor estabilidad numérica
                for k in range(2*n):
                    # Calcular producto con mayor precisión
                    product = factor * A[i][k]
                    
                    # Manejar casos donde esperamos resultados exactos de enteros
                    result = A[j][k] - product
                    
                    # Verificar si está muy cerca de un valor entero
                    nearest_int = round(result)
                    if abs(result - nearest_int) < 1e-10:
                        result = float(nearest_int)  # Convertir a valor entero exacto
                    
                    # Asegurar que valores muy pequeños se traten como cero
                    if abs(result) < 1e-10:
                        result = 0.0
                        
                    A[j][k] = result
                
                print_matrix(A)
    
    # Extraer la inversa de la mitad derecha de la matriz aumentada
    inverse = []
    for i in range(n):
        row = A[i][n:2*n]
        inverse.append(row)
    
    print("Matriz inversa:")
    print_matrix(inverse)
    return inverse

def lu_factorization(matrix):
    """
    Realiza la factorización LU (método de Doolittle) en una matriz cuadrada.
    
    Args:
        matrix: La matriz cuadrada a factorizar
        
    Returns:
        Una tupla (L, U) que contiene las matrices triangulares inferior y superior
        o None si la factorización no es posible
    """
    rows, cols = get_matrix_dimensions(matrix)
    
    if rows != cols:
        print(f"Error: No se puede realizar la factorización LU en una matriz {rows}x{cols}.")
        print("La matriz debe ser cuadrada para la factorización LU.")
        return None
    
    n = rows
    # Crear matrices de ceros para L y U
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    print("\nRealizando Factorización LU (método de Doolittle):")
    print("Matriz original:")
    print_matrix(matrix)
    
    try:
        # Establecer elementos diagonales de L a 1
        for i in range(n):
            L[i][i] = 1.0
        
        # Primera fila de U es la primera fila de A
        for j in range(n):
            U[0][j] = matrix[0][j]
        
        # Primera columna de L
        for i in range(1, n):
            if abs(U[0][0]) < 1e-10:
                print("Error: Pivote cero encontrado. Factorización LU fallida.")
                return None
            L[i][0] = matrix[i][0] / U[0][0]
            print(f"L[{i+1}][1] = {matrix[i][0]:.4f} / {U[0][0]:.4f} = {L[i][0]:.4f}")
        
        # Resto de L y U
        for i in range(1, n):
            # Calcular U[i][j] para j >= i
            for j in range(i, n):
                sum_val = 0
                calculation = f"U[{i+1}][{j+1}] = {matrix[i][j]:.4f}"
                for k in range(i):
                    sum_val += L[i][k] * U[k][j]
                    calculation += f" - {L[i][k]:.4f} * {U[k][j]:.4f}"
                U[i][j] = matrix[i][j] - sum_val
                calculation += f" = {U[i][j]:.4f}"
                print(calculation)
            
            # Calcular L[i][j] para j > i
            for j in range(i + 1, n):
                sum_val = 0
                calculation = f"L[{j+1}][{i+1}] = ({matrix[j][i]:.4f}"
                for k in range(i):
                    sum_val += L[j][k] * U[k][i]
                    calculation += f" - {L[j][k]:.4f} * {U[k][i]:.4f}"
                
                if abs(U[i][i]) < 1e-10:
                    print("Error: Pivote cero encontrado. Factorización LU fallida.")
                    return None
                    
                L[j][i] = (matrix[j][i] - sum_val) / U[i][i]
                calculation += f") / {U[i][i]:.4f} = {L[j][i]:.4f}"
                print(calculation)
                
        print("\nMatriz L:")
        print_matrix(L)
        print("\nMatriz U:")
        print_matrix(U)
        
        # Verificar LU = A
        product = multiply_matrices(L, U)
        print("\nVerificación - LU debe ser igual a A:")
        print_matrix(product)
        
        return L, U
    
    except ZeroDivisionError:
        print("Error: Pivote cero encontrado. Factorización LU fallida.")
        return None

def main_menu():
    """
    Muestra el menú principal y gestiona la entrada del usuario.
    """
    matrices = {}  # Diccionario para almacenar matrices para reutilización
    
    while True:
        print("\n" + "=" * 60)
        print("CALCULADORA DE MATRICES".center(60))
        print("=" * 60)
        print("\nMenú Principal:")
        print("1. Crear una nueva matriz")
        print("2. Ver matrices almacenadas")
        print("3. Suma de Matrices")
        print("4. Resta de Matrices")
        print("5. Multiplicación de Matrices")
        print("6. Calcular Determinante")
        print("7. Calcular Inversa")
        print("8. Eliminación Gaussiana")
        print("9. Eliminación Gauss-Jordan")
        print("10. Factorización LU")
        print("0. Salir")
        
        choice = get_integer_input("\nIngrese su elección (0-10): ", 0, 10)
        
        if choice == 0:
            print("\nSaliendo de la Calculadora de Matrices. ¡Adiós!")
            break
            
        elif choice == 1:
            # Crear una nueva matriz
            matrix_id = len(matrices) + 1
            matrices[matrix_id] = input_matrix()
            print(f"Matriz {matrix_id} ha sido creada y almacenada.")
            
        elif choice == 2:
            # Ver matrices almacenadas
            if not matrices:
                print("\nNo hay matrices almacenadas aún.")
            else:
                print("\nMatrices Almacenadas:")
                for matrix_id, matrix in matrices.items():
                    rows, cols = get_matrix_dimensions(matrix)
                    print(f"Matriz {matrix_id} ({rows}x{cols}):")
                    print_matrix(matrix)
                    
        elif choice == 3:
            # Suma de Matrices
            if len(matrices) < 2:
                print("\nError: Necesita al menos dos matrices para la suma.")
                print("Por favor cree más matrices primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix1_id = get_integer_input("\nIngrese ID de la primera matriz: ", 1, len(matrices))
            matrix2_id = get_integer_input("Ingrese ID de la segunda matriz: ", 1, len(matrices))
            
            result = add_matrices(matrices[matrix1_id], matrices[matrix2_id])
            if result is not None:
                print("\nResultado de la suma:")
                print_matrix(result)
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Resultado almacenado como Matriz {matrix_id}.")
                
        elif choice == 4:
            # Resta de Matrices
            if len(matrices) < 2:
                print("\nError: Necesita al menos dos matrices para la resta.")
                print("Por favor cree más matrices primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix1_id = get_integer_input("\nIngrese ID de la primera matriz: ", 1, len(matrices))
            matrix2_id = get_integer_input("Ingrese ID de la segunda matriz: ", 1, len(matrices))
            
            result = subtract_matrices(matrices[matrix1_id], matrices[matrix2_id])
            if result is not None:
                print("\nResultado de la resta:")
                print_matrix(result)
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Resultado almacenado como Matriz {matrix_id}.")
                
        elif choice == 5:
            # Multiplicación de Matrices
            if len(matrices) < 2:
                print("\nError: Necesita al menos dos matrices para la multiplicación.")
                print("Por favor cree más matrices primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix1_id = get_integer_input("\nIngrese ID de la primera matriz: ", 1, len(matrices))
            matrix2_id = get_integer_input("Ingrese ID de la segunda matriz: ", 1, len(matrices))
            
            result = multiply_matrices(matrices[matrix1_id], matrices[matrix2_id])
            if result is not None:
                print("\nResultado de la multiplicación:")
                print_matrix(result)
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Resultado almacenado como Matriz {matrix_id}.")
                
        elif choice == 6:
            # Calcular Determinante
            if not matrices:
                print("\nNo hay matrices almacenadas aún. Por favor cree una matriz primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix_id = get_integer_input("\nIngrese ID de la matriz para calcular el determinante: ", 1, len(matrices))
            
            det = determinant(matrices[matrix_id])
            if det is not None:
                print(f"\nDeterminante = {det}")
                
        elif choice == 7:
            # Calcular Inversa
            if not matrices:
                print("\nNo hay matrices almacenadas aún. Por favor cree una matriz primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix_id = get_integer_input("\nIngrese ID de la matriz para calcular la inversa: ", 1, len(matrices))
            
            result = calculate_inverse(matrices[matrix_id])
            if result is not None:
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Inversa almacenada como Matriz {matrix_id}.")
                
        elif choice == 8:
            # Eliminación Gaussiana
            if not matrices:
                print("\nNo hay matrices almacenadas aún. Por favor cree una matriz primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix_id = get_integer_input("\nIngrese ID de la matriz de coeficientes: ", 1, len(matrices))
            
            print("\n¿Desea resolver un sistema de ecuaciones (Ax = b)?")
            print("1. Sí - Transformar la matriz a forma escalonada y resolver")
            print("2. No - Solo transformar la matriz a forma escalonada")
            
            sub_choice = get_integer_input("\nIngrese elección (1-2): ", 1, 2)
            
            if sub_choice == 1:
                rows, _ = get_matrix_dimensions(matrices[matrix_id])
                b = []
                print(f"\nIngrese los {rows} elementos del vector de términos independientes b:")
                for i in range(rows):
                    b.append(get_float_input(f"b[{i+1}]: "))
                    
                A_echelon, b_echelon = gaussian_elimination(matrices[matrix_id], b)
                print("\nMatriz en forma escalonada:")
                print_matrix(A_echelon)
                print("\nVector b transformado:")
                print(b_echelon)
                
                x = back_substitution(A_echelon, b_echelon)
                if x is not None:
                    print("\nVector solución x:")
                    for i, val in enumerate(x):
                        print(f"x{i+1} = {val:.4f}")
            else:
                result, _ = gaussian_elimination(matrices[matrix_id])
                print("\nMatriz en forma escalonada:")
                print_matrix(result)
                
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Resultado almacenado como Matriz {matrix_id}.")
                
        elif choice == 9:
            # Eliminación Gauss-Jordan
            if not matrices:
                print("\nNo hay matrices almacenadas aún. Por favor cree una matriz primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix_id = get_integer_input("\nIngrese ID de la matriz: ", 1, len(matrices))
            
            print("\n¿Desea resolver un sistema de ecuaciones (Ax = b)?")
            print("1. Sí - Transformar la matriz y resolver")
            print("2. No - Solo transformar la matriz a forma escalonada reducida")
            
            sub_choice = get_integer_input("\nIngrese elección (1-2): ", 1, 2)
            
            if sub_choice == 1:
                rows, _ = get_matrix_dimensions(matrices[matrix_id])
                b = []
                print(f"\nIngrese los {rows} elementos del vector de términos independientes b:")
                for i in range(rows):
                    b.append(get_float_input(f"b[{i+1}]: "))
                    
                A_rref, b_rref = gauss_jordan_elimination(matrices[matrix_id], b)
                print("\nMatriz en forma escalonada reducida:")
                print_matrix(A_rref)
                print("\nVector solución x:")
                for i in range(rows):
                    print(f"x{i+1} = {b_rref[i]:.4f}")
            else:
                result, _ = gauss_jordan_elimination(matrices[matrix_id])
                print("\nMatriz en forma escalonada reducida:")
                print_matrix(result)
                
                matrix_id = len(matrices) + 1
                matrices[matrix_id] = result
                print(f"Resultado almacenado como Matriz {matrix_id}.")
                
        elif choice == 10:
            # Factorización LU
            if not matrices:
                print("\nNo hay matrices almacenadas aún. Por favor cree una matriz primero.")
                continue
                
            print("\nMatrices disponibles:")
            for matrix_id in matrices:
                rows, cols = get_matrix_dimensions(matrices[matrix_id])
                print(f"Matriz {matrix_id} ({rows}x{cols})")
                
            matrix_id = get_integer_input("\nIngrese ID de la matriz para factorización LU: ", 1, len(matrices))
            
            result = lu_factorization(matrices[matrix_id])
            if result is not None:
                L, U = result
                
                # Almacenar matrices L y U
                L_id = len(matrices) + 1
                matrices[L_id] = L
                print(f"Matriz L almacenada como Matriz {L_id}.")
                
                U_id = len(matrices) + 1
                matrices[U_id] = U
                print(f"Matriz U almacenada como Matriz {U_id}.")

if __name__ == "__main__":
    print("Welcome to the Matrix Calculator!")
    print("This program allows you to perform various matrix operations.")
    main_menu()
