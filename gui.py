"""
Aplicación web para operaciones con matrices.
Este módulo implementa una API web utilizando Flask para realizar operaciones
de álgebra lineal como suma, resta, multiplicación de matrices, cálculo de determinantes,
inversión de matrices, y métodos de resolución de sistemas de ecuaciones lineales.

"""
from flask import Flask, render_template, request, jsonify
import numpy as np
import io
import sys
import contextlib
from Calculadora import (
    print_matrix, get_matrix_dimensions, add_matrices, subtract_matrices, 
    multiply_matrices, determinant, calculate_inverse, gaussian_elimination, 
    gauss_jordan_elimination, lu_factorization, back_substitution
)

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Diccionario para almacenar matrices
stored_matrices = {}
next_matrix_id = 0  # Para controlar la asignación de letras como IDs
freed_matrix_ids = []  # Para almacenar IDs liberados que pueden ser reutilizados

@contextlib.contextmanager
def capture_stdout():
    """
    Captura la salida estándar para poder registrar los pasos de cálculo.
    
    Returns:
        str: El texto capturado de la salida estándar
    """
    stdout_backup = sys.stdout
    string_io = io.StringIO()
    sys.stdout = string_io
    try:
        yield string_io
    finally:
        sys.stdout = stdout_backup

def get_next_matrix_id():
    """
    Obtiene el siguiente ID en formato de letra mayúscula (A, B, C, ..., Z, AA, AB, ...)
    Reutiliza IDs liberados si están disponibles.
    
    Returns:
        str: Un ID único en formato de letra para identificar matrices
    """
    global next_matrix_id, freed_matrix_ids
    
    # Primero revisar si hay IDs liberados disponibles para reutilizar
    if freed_matrix_ids:
        return freed_matrix_ids.pop(0)  # Tomar y devolver el primer ID liberado
    
    # Si no hay IDs liberados, generar uno nuevo
    # Para los primeros 26 IDs, usar letras simples A-Z
    if next_matrix_id < 26:
        matrix_id = chr(65 + next_matrix_id)  # 65 es el código ASCII para 'A'
    else:
        # Para IDs posteriores, usar AA, AB, AC, etc.
        first_letter_index = (next_matrix_id // 26) - 1
        second_letter_index = next_matrix_id % 26
        matrix_id = chr(65 + first_letter_index) + chr(65 + second_letter_index)
    
    next_matrix_id += 1
    return matrix_id

@app.route('/')
def index():
    """
    Ruta principal que muestra la página inicial con las matrices almacenadas.
    
    Returns:
        str: Página HTML renderizada con las matrices disponibles
    """
    return render_template('index.html', matrices=stored_matrices)

@app.route('/create_matrix', methods=['POST'])
def create_matrix():
    """
    Crea una nueva matriz a partir de los datos proporcionados por el usuario.
    
    Returns:
        json: Respuesta JSON con el ID y los datos de la matriz creada
    """
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    matrix_data = []
    
    for i in range(rows):
        row = []
        for j in range(cols):
            value = float(request.form.get(f'cell_{i}_{j}', 0))
            row.append(value)
        matrix_data.append(row)
    
    # Asignar un ID a la matriz (ahora una letra)
    matrix_id = get_next_matrix_id()
    stored_matrices[matrix_id] = matrix_data
    
    return jsonify({
        'success': True,
        'message': f'Matriz {matrix_id} creada y almacenada',
        'matrix_id': matrix_id,
        'rows': rows,
        'cols': cols,
        'matrix': matrix_data
    })

@app.route('/view_matrices')
def view_matrices():
    """
    Obtiene información de todas las matrices almacenadas.
    
    Returns:
        json: Diccionario con información de todas las matrices (dimensiones y datos)
    """
    matrices_info = {}
    for matrix_id, matrix in stored_matrices.items():
        rows, cols = get_matrix_dimensions(matrix)
        matrices_info[matrix_id] = {
            'rows': rows,
            'cols': cols,
            'data': matrix
        }
    return jsonify(matrices_info)

@app.route('/add_matrices', methods=['POST'])
def add_matrices_route():
    """
    Suma dos matrices almacenadas.
    
    Returns:
        json: Respuesta JSON con el resultado de la suma y su ID asignado
    """
    matrix1_id = request.form['matrix1_id']
    matrix2_id = request.form['matrix2_id']
    
    if matrix1_id not in stored_matrices or matrix2_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'IDs de matriz inválidos'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        result = add_matrices(stored_matrices[matrix1_id], stored_matrices[matrix2_id])
    
    steps = output.getvalue()
    
    if result is not None:
        matrix_id = get_next_matrix_id()
        stored_matrices[matrix_id] = result
        return jsonify({
            'success': True,
            'message': f'Resultado guardado como Matriz {matrix_id}',
            'matrix_id': matrix_id,
            'result': result,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudieron sumar las matrices. Verifica las dimensiones.'
        })

@app.route('/subtract_matrices', methods=['POST'])
def subtract_matrices_route():
    """
    Resta dos matrices almacenadas.
    
    Returns:
        json: Respuesta JSON con el resultado de la resta y su ID asignado
    """
    matrix1_id = request.form['matrix1_id']
    matrix2_id = request.form['matrix2_id']
    
    if matrix1_id not in stored_matrices or matrix2_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'IDs de matriz inválidos'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        result = subtract_matrices(stored_matrices[matrix1_id], stored_matrices[matrix2_id])
    
    steps = output.getvalue()
    
    if result is not None:
        matrix_id = get_next_matrix_id()
        stored_matrices[matrix_id] = result
        return jsonify({
            'success': True,
            'message': f'Resultado guardado como Matriz {matrix_id}',
            'matrix_id': matrix_id,
            'result': result,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudieron restar las matrices. Verifica las dimensiones.'
        })

@app.route('/multiply_matrices', methods=['POST'])
def multiply_matrices_route():
    """
    Multiplica dos matrices almacenadas.
    
    Returns:
        json: Respuesta JSON con el resultado de la multiplicación y su ID asignado
    """
    matrix1_id = request.form['matrix1_id']
    matrix2_id = request.form['matrix2_id']
    
    if matrix1_id not in stored_matrices or matrix2_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'IDs de matriz inválidos'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        result = multiply_matrices(stored_matrices[matrix1_id], stored_matrices[matrix2_id])
    
    steps = output.getvalue()
    
    if result is not None:
        matrix_id = get_next_matrix_id()
        stored_matrices[matrix_id] = result
        return jsonify({
            'success': True,
            'message': f'Resultado guardado como Matriz {matrix_id}',
            'matrix_id': matrix_id,
            'result': result,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudieron multiplicar las matrices. Verifica las dimensiones.'
        })

@app.route('/determinant', methods=['POST'])
def determinant_route():
    """
    Calcula el determinante de una matriz.
    
    Returns:
        json: Respuesta JSON con el valor del determinante calculado y los pasos del cálculo
    """
    matrix_id = request.form['matrix_id']
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        det = determinant(stored_matrices[matrix_id])
    
    steps = output.getvalue()
    
    if det is not None:
        return jsonify({
            'success': True,
            'determinant': det,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudo calcular el determinante. La matriz debe ser cuadrada.'
        })

@app.route('/inverse', methods=['POST'])
def inverse_route():
    """
    Calcula la matriz inversa de una matriz dada.
    
    Returns:
        json: Respuesta JSON con la matriz inversa calculada y su ID asignado
    """
    matrix_id = request.form['matrix_id']
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        result = calculate_inverse(stored_matrices[matrix_id])
    
    steps = output.getvalue()
    
    if result is not None:
        matrix_id = get_next_matrix_id()
        stored_matrices[matrix_id] = result
        return jsonify({
            'success': True,
            'message': f'Inversa guardada como Matriz {matrix_id}',
            'matrix_id': matrix_id,
            'result': result,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudo calcular la inversa. La matriz debe ser cuadrada y no singular.'
        })

@app.route('/gaussian_elimination', methods=['POST'])
def gaussian_elimination_route():
    """
    Aplica el método de eliminación gaussiana a una matriz.
    Puede resolver un sistema de ecuaciones lineales si se proporciona el vector de términos independientes.
    
    Returns:
        json: Respuesta JSON con la forma escalonada de la matriz y la solución del sistema (si aplica)
    """
    matrix_id = request.form['matrix_id']
    solve_system = request.form.get('solve_system', 'false') == 'true'
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        if solve_system:
            # Obtener el vector b
            b_vector = []
            rows, _ = get_matrix_dimensions(stored_matrices[matrix_id])
            for i in range(rows):
                b_vector.append(float(request.form.get(f'b_{i}', 0)))
            
            A_echelon, b_echelon = gaussian_elimination(stored_matrices[matrix_id], b_vector)
            x = back_substitution(A_echelon, b_echelon)
            steps = output.getvalue()
            
            if x is not None:
                return jsonify({
                    'success': True,
                    'echelon_form': A_echelon,
                    'b_echelon': b_echelon,
                    'solution': x,
                    'steps': steps
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No se pudo resolver el sistema.'
                })
        else:
            result, _ = gaussian_elimination(stored_matrices[matrix_id])
            steps = output.getvalue()
            
            new_matrix_id = get_next_matrix_id()
            stored_matrices[new_matrix_id] = result
            return jsonify({
                'success': True,
                'message': f'Forma escalonada guardada como Matriz {new_matrix_id}',
                'matrix_id': new_matrix_id,
                'result': result,
                'steps': steps
            })

@app.route('/gauss_jordan', methods=['POST'])
def gauss_jordan_route():
    """
    Aplica el método de eliminación Gauss-Jordan a una matriz.
    Puede resolver un sistema de ecuaciones lineales si se proporciona el vector de términos independientes.
    
    Returns:
        json: Respuesta JSON con la forma escalonada reducida de la matriz y/o la solución del sistema
    """
    matrix_id = request.form['matrix_id']
    solve_system = request.form.get('solve_system', 'false') == 'true'
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        if solve_system:
            # Obtener el vector b
            b_vector = []
            rows, _ = get_matrix_dimensions(stored_matrices[matrix_id])
            for i in range(rows):
                b_vector.append(float(request.form.get(f'b_{i}', 0)))
            
            A_rref, b_rref = gauss_jordan_elimination(stored_matrices[matrix_id], b_vector)
            steps = output.getvalue()
            
            return jsonify({
                'success': True,
                'rref_form': A_rref,
                'solution': b_rref,
                'steps': steps
            })
        else:
            result, _ = gauss_jordan_elimination(stored_matrices[matrix_id])
            steps = output.getvalue()
            
            new_matrix_id = get_next_matrix_id()
            stored_matrices[new_matrix_id] = result
            return jsonify({
                'success': True,
                'message': f'Forma escalonada reducida guardada como Matriz {new_matrix_id}',
                'matrix_id': new_matrix_id,
                'result': result,
                'steps': steps
            })

@app.route('/lu_factorization', methods=['POST'])
def lu_factorization_route():
    """
    Realiza la factorización LU de una matriz.
    Descompone la matriz A en el producto de matrices L y U, donde L es triangular inferior y U es triangular superior.
    
    Returns:
        json: Respuesta JSON con las matrices L y U resultantes y sus IDs asignados
    """
    matrix_id = request.form['matrix_id']
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Capturar los pasos del cálculo
    with capture_stdout() as output:
        result = lu_factorization(stored_matrices[matrix_id])
    
    steps = output.getvalue()
    
    if result is not None:
        L, U = result
        L_id = get_next_matrix_id()
        stored_matrices[L_id] = L
        U_id = get_next_matrix_id()
        stored_matrices[U_id] = U
        return jsonify({
            'success': True,
            'message': f'Matriz L guardada como Matriz {L_id}, Matriz U guardada como Matriz {U_id}',
            'L_id': L_id,
            'U_id': U_id,
            'L_matrix': L,
            'U_matrix': U,
            'steps': steps
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No se pudo realizar la factorización LU. La matriz debe ser cuadrada.'
        })

@app.route('/delete_matrix', methods=['POST'])
def delete_matrix():
    """
    Elimina una matriz almacenada del sistema y libera su ID para reutilización.
    
    Returns:
        json: Respuesta JSON con el resultado de la operación de eliminación
    """
    matrix_id = request.form['matrix_id']
    
    if matrix_id not in stored_matrices:
        return jsonify({
            'success': False,
            'message': 'ID de matriz inválido'
        })
    
    # Eliminar la matriz
    del stored_matrices[matrix_id]
    
    # Guardar el ID liberado para reutilizarlo después
    freed_matrix_ids.append(matrix_id)
    # Ordenar los IDs liberados para usar primero los más bajos (A antes que B, etc.)
    freed_matrix_ids.sort()
    
    return jsonify({
        'success': True,
        'message': f'Matriz {matrix_id} eliminada correctamente'
    })

if __name__ == '__main__':
    app.run(debug=True)