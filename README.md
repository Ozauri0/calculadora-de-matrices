# Documentación Técnica: Calculadora de Matrices

## Índice
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Operaciones Matriciales Básicas](#operaciones-matriciales-básicas)
   - [Suma de Matrices](#suma-de-matrices)
   - [Resta de Matrices](#resta-de-matrices)
   - [Multiplicación de Matrices](#multiplicación-de-matrices)
4. [Operaciones Avanzadas](#operaciones-avanzadas)
   - [Cálculo de Determinantes](#cálculo-de-determinantes)
   - [Cálculo de Matriz Inversa](#cálculo-de-matriz-inversa)
5. [Métodos de Álgebra Lineal](#métodos-de-álgebra-lineal)
   - [Eliminación Gaussiana](#eliminación-gaussiana)
   - [Eliminación Gauss-Jordan](#eliminación-gauss-jordan)
   - [Factorización LU](#factorización-lu)
   - [Resolución de Sistemas de Ecuaciones](#resolución-de-sistemas-de-ecuaciones)
6. [Interfaz Web](#interfaz-web)
7. [Manejo de Errores y Precisión Numérica](#manejo-de-errores-y-precisión-numérica)
8. [Referencias](#referencias)

## Introducción

Esta calculadora de matrices es una herramienta de álgebra lineal que permite realizar operaciones matriciales básicas y avanzadas. El sistema se ha implementado en Python y consta de dos componentes principales: un módulo de cálculo `Calculadora.py` y una interfaz web basada en Flask `gui.py`. 

La calculadora está diseñada para trabajar con matrices de hasta 4x4, proporcionando explicaciones detalladas de cada paso en los cálculos, haciendo que sea especialmente útil para fines educativos y de investigación en el campo del álgebra lineal.

## Arquitectura del Sistema

El sistema está compuesto por dos módulos principales:

1. **Calculadora.py**: Contiene la implementación de todos los algoritmos matemáticos para operaciones con matrices, incluyendo:
   - Operaciones matriciales básicas (suma, resta, multiplicación)
   - Cálculo de determinantes
   - Cálculo de inversas
   - Algoritmos de eliminación gaussiana
   - Factorización LU
   - Algoritmo de Gauss-Jordan
   - Funciones auxiliares para entrada/salida y validación

2. **gui.py**: Implementa una API web usando Flask que expone las funcionalidades de la calculadora a través de una interfaz REST, permitiendo:
   - Creación y almacenamiento de matrices
   - Operaciones sobre las matrices almacenadas
   - Visualización de resultados y pasos intermedios
   - Manejo de sesiones para trabajar con múltiples matrices

## Operaciones Matriciales Básicas

### Suma de Matrices

La suma de matrices es una operación que se realiza elemento por elemento entre dos matrices de igual dimensión. Si A y B son matrices de m×n, entonces C = A + B es también una matriz m×n donde cada elemento cᵢⱼ = aᵢⱼ + bᵢⱼ.

La implementación en el código verifica primero que ambas matrices tengan las mismas dimensiones:

```python
def add_matrices(matrix1, matrix2):
    rows1, cols1 = get_matrix_dimensions(matrix1)
    rows2, cols2 = get_matrix_dimensions(matrix2)
    
    if rows1 != rows2 or cols1 != cols2:
        print(f"Error: No se pueden sumar matrices de dimensiones {rows1}x{cols1} y {rows2}x{cols2}.")
        print("Las matrices deben tener las mismas dimensiones para la suma.")
        return None
```

Una vez verificada la compatibilidad, se procede a la suma elemento por elemento:

```python
for i in range(rows1):
    row = []
    for j in range(cols1):
        element = matrix1[i][j] + matrix2[i][j]
        calculation = f"Elemento en la posición ({i+1},{j+1}) = {matrix1[i][j]} + {matrix2[i][j]} = {element}"
        print(calculation)
        row.append(element)
    result.append(row)
```

### Resta de Matrices

Similar a la suma, la resta de matrices se realiza elemento por elemento. Si A y B son matrices de m×n, entonces C = A - B es también una matriz m×n donde cada elemento cᵢⱼ = aᵢⱼ - bᵢⱼ.

La implementación en la calculadora sigue el mismo patrón que la suma:

```python
def subtract_matrices(matrix1, matrix2):
    # Verificación de dimensiones similar a add_matrices
    
    for i in range(rows1):
        row = []
        for j in range(cols1):
            element = matrix1[i][j] - matrix2[i][j]
            calculation = f"Elemento en la posición ({i+1},{j+1}) = {matrix1[i][j]} - {matrix2[i][j]} = {element}"
            print(calculation)
            row.append(element)
        result.append(row)
```

### Multiplicación de Matrices

La multiplicación de matrices A(m×n) y B(n×p) produce una matriz C(m×p) donde cada elemento cᵢⱼ se calcula como la suma del producto de los elementos correspondientes de la fila i de A y la columna j de B.

La implementación verifica primero la compatibilidad de las dimensiones:

```python
def multiply_matrices(matrix1, matrix2):
    rows1, cols1 = get_matrix_dimensions(matrix1)
    rows2, cols2 = get_matrix_dimensions(matrix2)
    
    if cols1 != rows2:
        print(f"Error: No se pueden multiplicar matrices de dimensiones {rows1}x{cols1} y {rows2}x{cols2}.")
        print("Para la multiplicación de matrices, el número de columnas en la primera matriz debe ser igual al número de filas en la segunda matriz.")
        return None
```

Después, realiza la multiplicación siguiendo la definición matemática:

```python
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
```

## Operaciones Avanzadas

### Cálculo de Determinantes

El determinante es un valor escalar asociado a una matriz cuadrada que proporciona información sobre la singularidad de la matriz y se utiliza en diferentes contextos algebraicos. La calculadora implementa un algoritmo recursivo basado en la expansión por cofactores para matrices de cualquier tamaño.

Para matrices 2×2 (caso base):
```python
if rows == 2:
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    print(f"\nDeterminante de matriz 2x2 = ({matrix[0][0]} * {matrix[1][1]}) - ({matrix[0][1]} * {matrix[1][0]}) = {det}")
    return det
```

Para matrices 3×3 o mayores (caso recursivo):
```python
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
```

### Cálculo de Matriz Inversa

La inversa de una matriz A es otra matriz A⁻¹ tal que A·A⁻¹ = A⁻¹·A = I (matriz identidad). El método implementado utiliza la eliminación Gauss-Jordan para encontrar la inversa.

El proceso consiste en:
1. Verificar que la matriz sea cuadrada
2. Calcular y verificar que el determinante sea distinto de cero
3. Crear una matriz aumentada [A|I] donde I es la matriz identidad
4. Aplicar eliminación Gauss-Jordan para transformar la parte izquierda en la identidad
5. La parte derecha resultante será la matriz inversa

```python
# Aumentar la matriz con la identidad
A = [row[:] for row in matrix]
for i in range(rows):
    A[i].extend(identity[i])

# Aplicar eliminación Gauss-Jordan
# ... (código de eliminación Gauss-Jordan) ...

# Extraer la inversa de la mitad derecha de la matriz aumentada
inverse = []
for i in range(n):
    row = A[i][n:2*n]
    inverse.append(row)
```

## Métodos de Álgebra Lineal

### Eliminación Gaussiana

La eliminación gaussiana es un algoritmo para resolver sistemas de ecuaciones lineales y para reducir una matriz a su forma escalonada. El método consiste en:

1. Recorrer la matriz de izquierda a derecha, de arriba a abajo
2. Encontrar el pivote (elemento no nulo en la diagonal)
3. Eliminar todos los elementos debajo del pivote

La implementación incluye selección parcial de pivote para mejorar la estabilidad numérica:

```python
# Encuentra la fila pivote (con el mayor valor absoluto)
max_row = i
for k in range(i + 1, rows):
    if abs(A[k][i]) > abs(A[max_row][i]):
        max_row = k

# Intercambia la fila actual con la fila pivote si es necesario
if max_row != i:
    A[i], A[max_row] = A[max_row], A[i]
```

Luego, se eliminan los elementos debajo del pivote:

```python
for j in range(i + 1, rows):
    try:
        factor = A[j][i] / A[i][i]
    except ZeroDivisionError:
        continue
        
    for k in range(i, cols):
        A[j][k] -= factor * A[i][k]
```

### Eliminación Gauss-Jordan

La eliminación Gauss-Jordan extiende la eliminación gaussiana para obtener una matriz en forma escalonada reducida, donde:
- Cada fila tiene un 1 como primer elemento no nulo (pivote)
- Cada columna que contiene un pivote tiene ceros en todas las demás posiciones

El algoritmo añade estas operaciones adicionales a la eliminación gaussiana:

```python
# Escalar la fila pivote para hacer el pivote 1
pivot = A[i][i]
for j in range(i, cols):
    A[i][j] /= pivot

# Eliminar todas las demás filas (arriba y abajo del pivote)
for j in range(rows):
    if j != i:
        factor = A[j][i]
        for k in range(i, cols):
            A[j][k] -= factor * A[i][k]
```

### Factorización LU

La factorización LU descompone una matriz cuadrada A en el producto de dos matrices: L (triangular inferior) y U (triangular superior), de modo que A = L·U. 

El método implementado (Doolittle) construye ambas matrices simultáneamente:

```python
# Elementos diagonales de L son 1
for i in range(n):
    L[i][i] = 1.0

# Primera fila de U es la primera fila de A
for j in range(n):
    U[0][j] = matrix[0][j]

# Primera columna de L
for i in range(1, n):
    L[i][0] = matrix[i][0] / U[0][0]

# Resto de L y U
for i in range(1, n):
    # Calcular U[i][j] para j >= i
    for j in range(i, n):
        sum_val = 0
        for k in range(i):
            sum_val += L[i][k] * U[k][j]
        U[i][j] = matrix[i][j] - sum_val
    
    # Calcular L[i][j] para j > i
    for j in range(i + 1, n):
        sum_val = 0
        for k in range(i):
            sum_val += L[j][k] * U[k][i]
        L[j][i] = (matrix[j][i] - sum_val) / U[i][i]
```

### Resolución de Sistemas de Ecuaciones

La calculadora puede resolver sistemas de ecuaciones lineales Ax = b mediante varios métodos:

1. **Eliminación gaussiana con sustitución hacia atrás**:
   - Se aplica eliminación gaussiana a la matriz aumentada [A|b]
   - Se utiliza sustitución hacia atrás para encontrar los valores de las incógnitas

2. **Eliminación Gauss-Jordan**:
   - Se aplica directamente a la matriz aumentada [A|b]
   - Al completar, la solución se encuentra directamente en el vector b transformado

3. **Factorización LU**:
   - Se descompone A en L·U
   - Se resuelve Ly = b (sustitución hacia adelante)
   - Se resuelve Ux = y (sustitución hacia atrás)

Por ejemplo, la sustitución hacia atrás implementada:

```python
def back_substitution(A, b):
    rows = len(A)
    x = [0] * rows
    
    for i in range(rows - 1, -1, -1):
        sum_val = 0
        for j in range(pivot_col + 1, rows):
            if abs(A[i][j]) > 1e-10:
                sum_val += A[i][j] * x[j]
        
        x[pivot_col] = (b[i] - sum_val) / A[i][pivot_col]
    
    return x
```

## Interfaz Web

La interfaz web implementada con Flask permite acceder a todas las funcionalidades de la calculadora a través de una API RESTful. Los principales endpoints incluyen:

- `/create_matrix`: Crea una nueva matriz a partir de los datos proporcionados
- `/view_matrices`: Muestra todas las matrices almacenadas
- `/add_matrices`, `/subtract_matrices`, `/multiply_matrices`: Realizan operaciones básicas entre matrices
- `/determinant`, `/inverse`: Calculan el determinante o la inversa de una matriz
- `/gaussian_elimination`, `/gauss_jordan`, `/lu_factorization`: Aplican los respectivos métodos de álgebra lineal

La API utiliza un sistema de identificación de matrices basado en letras (A, B, C...) y mantiene un registro de matrices liberadas para su reutilización:

```python
def get_next_matrix_id():
    # Primero revisar si hay IDs liberados disponibles para reutilizar
    if freed_matrix_ids:
        return freed_matrix_ids.pop(0)
    
    # Si no hay IDs liberados, generar uno nuevo
    if next_matrix_id < 26:
        matrix_id = chr(65 + next_matrix_id)
    else:
        first_letter_index = (next_matrix_id // 26) - 1
        second_letter_index = next_matrix_id % 26
        matrix_id = chr(65 + first_letter_index) + chr(65 + second_letter_index)
    
    next_matrix_id += 1
    return matrix_id
```

## Manejo de Errores y Precisión Numérica

La calculadora implementa varios mecanismos para garantizar la precisión numérica y manejar errores comunes en cálculos matriciales:

1. **Verificación de dimensiones**: Las operaciones verifican la compatibilidad de dimensiones y retornan mensajes de error apropiados:
   ```python
   if rows1 != rows2 or cols1 != cols2:
       print("Las matrices deben tener las mismas dimensiones para la suma.")
       return None
   ```

2. **Detección de matrices singulares**: Se verifica si el determinante es cercano a cero:
   ```python
   if abs(det) < 1e-10:
       print("La matriz es singular (determinante es cero), por lo que no tiene inversa.")
       return None
   ```

3. **Manejo de divisiones por cero**: Las operaciones que podrían causar divisiones por cero son manejadas:
   ```python
   try:
       factor = A[j][i] / A[i][i]
   except ZeroDivisionError:
       print("Pivote cero encontrado. Operación fallida.")
       continue
   ```

4. **Control de errores de redondeo**: Se utiliza una tolerancia para valores cercanos a cero:
   ```python
   if abs(result) < 1e-10:
       result = 0.0
   ```

5. **Selección parcial de pivotes**: En eliminación gaussiana, se selecciona el pivote con mayor valor absoluto para mejorar la estabilidad numérica.

## Referencias

1. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
2. Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.
3. Trefethen, L. N., & Bau III, D. (1997). *Numerical Linear Algebra*. SIAM.
4. Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.