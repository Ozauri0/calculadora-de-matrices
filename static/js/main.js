// Variables globales
let matrices = {} // Almacena las matrices disponibles localmente

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
  // Elementos para crear matrices
  const rowsInput = document.getElementById("rows")
  const colsInput = document.getElementById("cols")
  const generateFieldsBtn = document.getElementById("generateFields")
  const matrixInputContainer = document.getElementById("matrixInputContainer")
  const saveMatrixBtn = document.getElementById("saveMatrix")

  // Botones de operaciones básicas
  const addMatricesBtn = document.getElementById("addMatricesBtn")
  const subtractMatricesBtn = document.getElementById("subtractMatricesBtn")
  const multiplyMatricesBtn = document.getElementById("multiplyMatricesBtn")

  // Botones de operaciones avanzadas
  const determinantBtn = document.getElementById("determinantBtn")
  const inverseBtn = document.getElementById("inverseBtn")
  const luFactorizationBtn = document.getElementById("luFactorizationBtn")

  // Botones de métodos numéricos
  const gaussianEliminationBtn = document.getElementById("gaussianEliminationBtn")
  const gaussJordanBtn = document.getElementById("gaussJordanBtn")

  // Operación modal
  const operationTypeInput = document.getElementById("operationType")
  const matrix1Select = document.getElementById("matrix1")
  const matrix2Select = document.getElementById("matrix2")
  const performOperationBtn = document.getElementById("performOperation")

  // Single matriz modal
  const singleOperationTypeInput = document.getElementById("singleOperationType")
  const singleMatrixSelect = document.getElementById("singleMatrix")
  const performSingleOperationBtn = document.getElementById("performSingleOperation")
  const vectorBContainer = document.getElementById("vectorBContainer")
  const solveSystemCheck = document.getElementById("solveSystemCheck")
  const solveSystemCheckbox = document.getElementById("solveSystemCheckbox")

  // Contenedores de visualización
  const storedMatricesContainer = document.getElementById("storedMatricesContainer")
  const resultContainer = document.getElementById("resultContainer")
  const noMatricesMsg = document.getElementById("noMatricesMsg")

  // Inicializar comportamiento de acordeón para secciones de la barra lateral
  document.querySelectorAll(".sidebar-section-header").forEach((header) => {
    header.addEventListener("click", () => {
      const isExpanded = header.getAttribute("aria-expanded") === "true"
      header.setAttribute("aria-expanded", !isExpanded)
    })
  })

  // Event Listeners
  generateFieldsBtn.addEventListener("click", generateMatrixFields)
  saveMatrixBtn.addEventListener("click", saveMatrix)

  addMatricesBtn.addEventListener("click", () => openMatricesModal("add"))
  subtractMatricesBtn.addEventListener("click", () => openMatricesModal("subtract"))
  multiplyMatricesBtn.addEventListener("click", () => openMatricesModal("multiply"))

  determinantBtn.addEventListener("click", () => openSingleMatrixModal("determinant"))
  inverseBtn.addEventListener("click", () => openSingleMatrixModal("inverse"))
  luFactorizationBtn.addEventListener("click", () => openSingleMatrixModal("lu"))

  gaussianEliminationBtn.addEventListener("click", () => openSingleMatrixModal("gaussian", true))
  gaussJordanBtn.addEventListener("click", () => openSingleMatrixModal("gauss_jordan", true))

  performOperationBtn.addEventListener("click", performMatrixOperation)
  performSingleOperationBtn.addEventListener("click", performSingleMatrixOperation)

  solveSystemCheckbox.addEventListener("change", toggleVectorBFields)

  // Event listener para botones de eliminación de matrices (delegación de eventos)
  storedMatricesContainer.addEventListener("click", (event) => {
    const deleteButton = event.target.closest(".delete-matrix-btn")
    if (deleteButton) {
      const matrixId = deleteButton.dataset.matrixId
      if (confirm(`¿Estás seguro de que deseas eliminar la Matriz ${matrixId}?`)) {
        deleteMatrix(matrixId)
      }
    }
  })

  // Cargar matrices al inicio
  loadMatrices()

  // Función para formatear y mostrar los pasos de cálculo como un chat
  function formatCalculationSteps(steps) {
    if (!steps || typeof steps !== "string") return ""

    // Dividir los pasos en líneas
    const lines = steps.split("\n")

    // Filtrar líneas vacías y formatear como mensajes de chat
    let chatHtml = '<div class="calculation-steps">'

    for (const line of lines) {
      if (line.trim()) {
        // Identificar el tipo de línea para darle formato adecuado
        if (
          line.includes("=") &&
          (line.includes("+") || line.includes("-") || line.includes("*") || line.includes("/"))
        ) {
          // Ecuación o cálculo
          chatHtml += `<div class="step-item calculation-step">${line}</div>`
        } else if (line.trim().startsWith("[") || (line.includes("[") && line.includes("]"))) {
          // Matriz
          chatHtml += `<div class="step-item matrix-step">${line}</div>`
        } else if (
          line.includes("Matriz") ||
          line.includes("matriz") ||
          line.includes("Calculando") ||
          line.includes("Determinante") ||
          line.includes("Inversa") ||
          line.includes("Término")
        ) {
          // Título o encabezado
          chatHtml += `<div class="step-item title-step">${line}</div>`
        } else {
          // Otros mensajes explicativos
          chatHtml += `<div class="step-item calculation-step">${line}</div>`
        }
      }
    }

    chatHtml += "</div>"
    return chatHtml
  }

  // Funciones
  function generateMatrixFields() {
    const rows = Number.parseInt(rowsInput.value)
    const cols = Number.parseInt(colsInput.value)

    if (isNaN(rows) || isNaN(cols) || rows < 1 || rows > 4 || cols < 1 || cols > 4) {
      showAlert("Por favor ingresa dimensiones válidas (1-4)", "danger")
      return
    }

    let html = '<div class="matrix-input-container">'

    for (let i = 0; i < rows; i++) {
      html += '<div class="matrix-input-row">'
      for (let j = 0; j < cols; j++) {
        html += `<input type="number" class="form-control matrix-input-cell" 
                          id="cell_${i}_${j}" name="cell_${i}_${j}" value="0" step="any">`
      }
      html += "</div>"
    }

    html += "</div>"

    matrixInputContainer.innerHTML = html
    saveMatrixBtn.classList.remove("d-none")

    // Añadir animación
    matrixInputContainer.classList.add("fade-in")
    setTimeout(() => {
      matrixInputContainer.classList.remove("fade-in")
    }, 500)

    // Enfocar el primer campo
    setTimeout(() => {
      document.getElementById("cell_0_0").focus()
    }, 100)
  }

  function saveMatrix() {
    const rows = Number.parseInt(rowsInput.value)
    const cols = Number.parseInt(colsInput.value)
    const formData = new FormData()

    formData.append("rows", rows)
    formData.append("cols", cols)

    // Recopilar valores de la matriz
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const cellId = `cell_${i}_${j}`
        const cellValue = document.getElementById(cellId).value || "0"
        formData.append(cellId, cellValue)
      }
    }

    // Mostrar indicador de carga
    saveMatrixBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Guardando...'
    saveMatrixBtn.disabled = true

    // Enviar al servidor
    fetch("/create_matrix", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert(data.message, "success")
          // Actualizar la información de matrices localmente
          matrices[data.matrix_id] = {
            rows: data.rows,
            cols: data.cols,
            data: data.matrix,
          }
          displayStoredMatrices()

          // Limpiar el contenedor de entrada
          matrixInputContainer.innerHTML = ""
          saveMatrixBtn.classList.add("d-none")
        } else {
          showAlert("Error al guardar la matriz", "danger")
        }

        // Restaurar botón
        saveMatrixBtn.innerHTML = '<i class="fas fa-save me-2"></i>Guardar Matriz'
        saveMatrixBtn.disabled = false
      })
      .catch((error) => {
        console.error("Error:", error)
        showAlert("Error de comunicación con el servidor", "danger")

        // Restaurar botón
        saveMatrixBtn.innerHTML = '<i class="fas fa-save me-2"></i>Guardar Matriz'
        saveMatrixBtn.disabled = false
      })
  }

  function loadMatrices() {
    // Mostrar indicador de carga
    storedMatricesContainer.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando matrices...</p>
            </div>
        `

    fetch("/view_matrices")
      .then((response) => response.json())
      .then((data) => {
        matrices = data
        displayStoredMatrices()
      })
      .catch((error) => {
        console.error("Error:", error)
        showAlert("Error al cargar matrices", "warning")
        storedMatricesContainer.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error al cargar matrices. Por favor, recarga la página.
                </div>
            `
      })
  }

  function displayStoredMatrices() {
    if (Object.keys(matrices).length === 0) {
      noMatricesMsg.classList.remove("d-none")
      storedMatricesContainer.innerHTML = ""
      return
    }

    noMatricesMsg.classList.add("d-none")
    let html = ""

    for (const [id, matrix] of Object.entries(matrices)) {
      html += generateMatrixDisplay(id, matrix)
    }

    storedMatricesContainer.innerHTML = html

    // Añadir animación
    const matrixElements = document.querySelectorAll(".matrix-display")
    matrixElements.forEach((el, index) => {
      el.style.opacity = "0"
      el.style.transform = "translateY(10px)"
      setTimeout(() => {
        el.style.transition = "opacity 0.3s ease, transform 0.3s ease"
        el.style.opacity = "1"
        el.style.transform = "translateY(0)"
      }, index * 50)
    })
  }

  function generateMatrixDisplay(id, matrix) {
    let html = `<div class="matrix-display">
                    <button class="btn btn-sm btn-danger delete-matrix-btn" data-matrix-id="${id}" title="Eliminar matriz">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                    <div class="matrix-header">
                        <span>Matriz </span>
                        <div class="matrix-id-container">
                            <span class="matrix-id">${id}</span>
                        </div>
                        <span> (${matrix.rows}x${matrix.cols})</span>
                    </div>
                    <div class="matrix-content">`

    for (let i = 0; i < matrix.data.length; i++) {
      html += '<div class="matrix-row">'
      for (let j = 0; j < matrix.data[i].length; j++) {
        const value = Number.parseFloat(matrix.data[i][j])
        // Formatear para mostrar enteros sin decimales y limitar decimales
        const formattedValue = Number.isInteger(value) ? value : value.toFixed(2)
        html += `<div class="matrix-cell">${formattedValue}</div>`
      }
      html += "</div>"
    }

    html += `       </div>
                </div>`

    return html
  }

  function openMatricesModal(operation) {
    if (Object.keys(matrices).length < 2) {
      showAlert("Necesitas al menos dos matrices para esta operación", "warning")
      return
    }

    // Limpiar selects
    matrix1Select.innerHTML = ""
    matrix2Select.innerHTML = ""

    // Llenar los selects con las matrices disponibles
    for (const id in matrices) {
      const option1 = new Option(`Matriz ${id} (${matrices[id].rows}x${matrices[id].cols})`, id)
      const option2 = new Option(`Matriz ${id} (${matrices[id].rows}x${matrices[id].cols})`, id)
      matrix1Select.add(option1)
      matrix2Select.add(option2)
    }

    // Configurar el tipo de operación
    operationTypeInput.value = operation

    // Actualizar el título del modal
    const modalTitle = document.querySelector("#selectMatricesModal .modal-title")
    switch (operation) {
      case "add":
        modalTitle.textContent = "Suma de Matrices"
        break
      case "subtract":
        modalTitle.textContent = "Resta de Matrices"
        break
      case "multiply":
        modalTitle.textContent = "Multiplicación de Matrices"
        break
    }

    // Mostrar el modal
    const modalElement = document.getElementById("selectMatricesModal")
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }

  function openSingleMatrixModal(operation, showSystemOption = false) {
    if (Object.keys(matrices).length === 0) {
      showAlert("No hay matrices disponibles", "warning")
      return
    }

    // Limpiar select
    singleMatrixSelect.innerHTML = ""

    // Llenar el select con las matrices disponibles
    for (const id in matrices) {
      const option = new Option(`Matriz ${id} (${matrices[id].rows}x${matrices[id].cols})`, id)
      singleMatrixSelect.add(option)
    }

    // Configurar el tipo de operación
    singleOperationTypeInput.value = operation

    // Actualizar el título del modal y opciones adicionales
    const modalTitle = document.getElementById("singleMatrixModalTitle")

    switch (operation) {
      case "determinant":
        modalTitle.textContent = "Calcular Determinante"
        solveSystemCheck.classList.add("d-none")
        vectorBContainer.classList.add("d-none")
        break
      case "inverse":
        modalTitle.textContent = "Calcular Matriz Inversa"
        solveSystemCheck.classList.add("d-none")
        vectorBContainer.classList.add("d-none")
        break
      case "lu":
        modalTitle.textContent = "Factorización LU"
        solveSystemCheck.classList.add("d-none")
        vectorBContainer.classList.add("d-none")
        break
      case "gaussian":
        modalTitle.textContent = "Eliminación Gaussiana"
        solveSystemCheck.classList.remove("d-none")
        vectorBContainer.classList.add("d-none")
        break
      case "gauss_jordan":
        modalTitle.textContent = "Eliminación Gauss-Jordan"
        solveSystemCheck.classList.remove("d-none")
        vectorBContainer.classList.add("d-none")
        break
    }

    // Mostrar el modal
    const modalElement = document.getElementById("selectMatrixModal")
    // Declare bootstrap here
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }

  function toggleVectorBFields() {
    if (solveSystemCheckbox.checked) {
      const matrixId = singleMatrixSelect.value
      if (!matrixId) return

      const rows = matrices[matrixId].rows
      let html = '<div class="mt-3 mb-3">'
      html += '<label class="form-label">Vector b:</label>'

      for (let i = 0; i < rows; i++) {
        html += `
                <div class="mb-2">
                    <div class="input-group">
                        <span class="input-group-text">b<sub>${i + 1}</sub></span>
                        <input type="number" class="form-control" id="b_${i}" name="b_${i}" value="0" step="any">
                    </div>
                </div>`
      }

      html += "</div>"
      vectorBContainer.innerHTML = html
      vectorBContainer.classList.remove("d-none")

      // Añadir animación
      vectorBContainer.classList.add("fade-in")
      setTimeout(() => {
        vectorBContainer.classList.remove("fade-in")
      }, 500)
    } else {
      vectorBContainer.classList.add("d-none")
    }
  }

  function performMatrixOperation() {
    const operation = operationTypeInput.value
    const matrix1Id = matrix1Select.value
    const matrix2Id = matrix2Select.value

    if (!operation || !matrix1Id || !matrix2Id) {
      showAlert("Por favor selecciona ambas matrices", "warning")
      return
    }

    const formData = new FormData()
    formData.append("matrix1_id", matrix1Id)
    formData.append("matrix2_id", matrix2Id)

    let endpoint = ""
    switch (operation) {
      case "add":
        endpoint = "/add_matrices"
        break
      case "subtract":
        endpoint = "/subtract_matrices"
        break
      case "multiply":
        endpoint = "/multiply_matrices"
        break
    }

    // Mostrar indicador de carga
    performOperationBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...'
    performOperationBtn.disabled = true

    fetch(endpoint, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Cerrar el modal
        const selectMatricesModal = document.getElementById("selectMatricesModal")
        if (selectMatricesModal) {
          const modal = bootstrap.Modal.getInstance(selectMatricesModal)
          if (modal) {
            modal.hide()
          }
        }

        if (data.success) {
          // Actualizar matrices locales
          matrices[data.matrix_id] = {
            rows: data.result.length,
            cols: data.result[0].length,
            data: data.result,
          }

          displayStoredMatrices()

          // Preparar los pasos de cálculo formateados para mostrar
          let calculationStepsHtml = ""
          if (data.steps) {
            calculationStepsHtml = formatCalculationSteps(data.steps)
          }

          // Mostrar resultado
          let operationName = ""
          let operationSymbol = ""
          switch (operation) {
            case "add":
              operationName = "Suma"
              operationSymbol = "+"
              break
            case "subtract":
              operationName = "Resta"
              operationSymbol = "-"
              break
            case "multiply":
              operationName = "Multiplicación"
              operationSymbol = "×"
              break
          }

          showResult(
            `${operationName} de Matrices`,
            `<div class="operation-display">
                <div class="d-inline-block matrix-id-container">
                    <span class="matrix-id">${matrix1Id}</span>
                </div>
                <span class="operation-symbol mx-2">${operationSymbol}</span>
                <div class="d-inline-block matrix-id-container">
                    <span class="matrix-id">${matrix2Id}</span>
                </div>
                <span class="operation-symbol mx-2">=</span>
                <div class="d-inline-block matrix-id-container">
                    <span class="matrix-id">${data.matrix_id}</span>
                </div>
             </div>
             <div class="result-matrix">${generateMatrixDisplay(data.matrix_id, matrices[data.matrix_id])}</div>`,
            calculationStepsHtml,
          )
        } else {
          showAlert(data.message, "danger")
        }

        // Restaurar botón
        performOperationBtn.innerHTML = "Realizar Operación"
        performOperationBtn.disabled = false
      })
      .catch((error) => {
        console.error("Error:", error)
        showAlert("Error de comunicación con el servidor", "danger")

        // Restaurar botón
        performOperationBtn.innerHTML = "Realizar Operación"
        performOperationBtn.disabled = false
      })
  }

  function performSingleMatrixOperation() {
    const operation = singleOperationTypeInput.value
    const matrixId = singleMatrixSelect.value

    if (!operation || !matrixId) {
      showAlert("Por favor selecciona una matriz", "warning")
      return
    }

    const formData = new FormData()
    formData.append("matrix_id", matrixId)

    // Variables específicas para métodos que resuelven sistemas
    if (operation === "gaussian" || operation === "gauss_jordan") {
      formData.append("solve_system", solveSystemCheckbox.checked)

      if (solveSystemCheckbox.checked) {
        // Agregar vector b
        const rows = matrices[matrixId].rows
        for (let i = 0; i < rows; i++) {
          formData.append(`b_${i}`, document.getElementById(`b_${i}`).value || "0")
        }
      }
    }

    let endpoint = ""
    switch (operation) {
      case "determinant":
        endpoint = "/determinant"
        break
      case "inverse":
        endpoint = "/inverse"
        break
      case "lu":
        endpoint = "/lu_factorization"
        break
      case "gaussian":
        endpoint = "/gaussian_elimination"
        break
      case "gauss_jordan":
        endpoint = "/gauss_jordan"
        break
    }

    // Mostrar indicador de carga
    performSingleOperationBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...'
    performSingleOperationBtn.disabled = true

    fetch(endpoint, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Cerrar el modal
        const selectMatrixModal = document.getElementById("selectMatrixModal")
        if (selectMatrixModal) {
          const modal = bootstrap.Modal.getInstance(selectMatrixModal)
          if (modal) {
            modal.hide()
          }
        }

        if (data.success) {
          // Preparar los pasos de cálculo formateados para mostrar
          let calculationStepsHtml = ""
          if (data.steps) {
            calculationStepsHtml = formatCalculationSteps(data.steps)
          }

          switch (operation) {
            case "determinant":
              showResult(
                "Determinante",
                `<div class="operation-display">
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${matrixId}</span>
                    </div>
                 </div>
                 <p class="text-center">El determinante de la Matriz ${matrixId} es:</p>
                 <p class="text-center"><span class="result-value">${data.determinant}</span></p>`,
                calculationStepsHtml,
              )
              break

            case "inverse":
              // Actualizar matrices locales
              matrices[data.matrix_id] = {
                rows: data.result.length,
                cols: data.result[0].length,
                data: data.result,
              }

              displayStoredMatrices()

              showResult(
                "Matriz Inversa",
                `<div class="operation-display">
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${matrixId}</span>
                    </div>
                    <span class="operation-symbol mx-2">⁻¹</span>
                    <span class="operation-symbol mx-2">=</span>
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${data.matrix_id}</span>
                    </div>
                 </div>
                 <div class="result-matrix">${generateMatrixDisplay(data.matrix_id, matrices[data.matrix_id])}</div>`,
                calculationStepsHtml,
              )
              break

            case "lu":
              // Actualizar matrices locales
              matrices[data.L_id] = {
                rows: data.L_matrix.length,
                cols: data.L_matrix[0].length,
                data: data.L_matrix,
              }

              matrices[data.U_id] = {
                rows: data.U_matrix.length,
                cols: data.U_matrix[0].length,
                data: data.U_matrix,
              }

              displayStoredMatrices()

              showResult(
                "Factorización LU",
                `<div class="operation-display">
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${matrixId}</span>
                    </div>
                    <span class="operation-symbol mx-2">=</span>
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${data.L_id}</span>
                    </div>
                    <span class="operation-symbol mx-2">×</span>
                    <div class="d-inline-block matrix-id-container">
                        <span class="matrix-id">${data.U_id}</span>
                    </div>
                 </div>
                 <div class="row">
                   <div class="col-md-6">
                     <p class="text-center">Matriz L (${data.L_id}):</p>
                     <div class="result-matrix">${generateMatrixDisplay(data.L_id, matrices[data.L_id])}</div>
                   </div>
                   <div class="col-md-6">
                     <p class="text-center">Matriz U (${data.U_id}):</p>
                     <div class="result-matrix">${generateMatrixDisplay(data.U_id, matrices[data.U_id])}</div>
                   </div>
                 </div>`,
                calculationStepsHtml,
              )
              break

            case "gaussian":
              if (solveSystemCheckbox.checked) {
                // Mostrar la solución del sistema
                let solutionHtml =
                  '<p class="text-center mb-3">La solución del sistema es:</p><div class="row justify-content-center"><div class="col-md-8"><ul class="list-group">'
                for (let i = 0; i < data.solution.length; i++) {
                  solutionHtml += `<li class="list-group-item d-flex justify-content-between align-items-center">
                                  x<sub>${i + 1}</sub>
                                  <span class="result-value">${data.solution[i].toFixed(4)}</span>
                               </li>`
                }
                solutionHtml += "</ul></div></div>"

                // Forma escalonada
                const echelonMatrix = {
                  rows: data.echelon_form.length,
                  cols: data.echelon_form[0].length,
                  data: data.echelon_form,
                }

                showResult(
                  "Eliminación Gaussiana - Sistema Resuelto",
                  `<div class="operation-display">
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${matrixId}</span>
                      </div>
                   </div>
                   <p class="text-center">Matriz en forma escalonada:</p>
                   <div class="result-matrix" style="margin-bottom: 20px;">${generateMatrixDisplay("escalonada", echelonMatrix)}</div>
                   ${solutionHtml}`,
                  calculationStepsHtml,
                )
              } else {
                // Actualizar matrices locales
                matrices[data.matrix_id] = {
                  rows: data.result.length,
                  cols: data.result[0].length,
                  data: data.result,
                }

                displayStoredMatrices()

                showResult(
                  "Eliminación Gaussiana",
                  `<div class="operation-display">
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${matrixId}</span>
                      </div>
                      <span class="operation-symbol mx-2">→</span>
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${data.matrix_id}</span>
                      </div>
                   </div>
                   <p class="text-center">La forma escalonada de la Matriz ${matrixId} es la Matriz ${data.matrix_id}:</p>
                   <div class="result-matrix">${generateMatrixDisplay(data.matrix_id, matrices[data.matrix_id])}</div>`,
                  calculationStepsHtml,
                )
              }
              break

            case "gauss_jordan":
              if (solveSystemCheckbox.checked) {
                // Mostrar la solución del sistema
                let solutionHtml =
                  '<p class="text-center mb-3">La solución del sistema es:</p><div class="row justify-content-center"><div class="col-md-8"><ul class="list-group">'
                for (let i = 0; i < data.solution.length; i++) {
                  solutionHtml += `<li class="list-group-item d-flex justify-content-between align-items-center">
                                  x<sub>${i + 1}</sub>
                                  <span class="result-value">${data.solution[i].toFixed(4)}</span>
                               </li>`
                }
                solutionHtml += "</ul></div></div>"

                // Forma escalonada reducida
                const rrefMatrix = {
                  rows: data.rref_form.length,
                  cols: data.rref_form[0].length,
                  data: data.rref_form,
                }

                showResult(
                  "Eliminación Gauss-Jordan - Sistema Resuelto",
                  `<div class="operation-display">
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${matrixId}</span>
                      </div>
                   </div>
                   <p class="text-center">Matriz en forma escalonada reducida:</p>
                   <div class="result-matrix" style="margin-bottom: 20px;">${generateMatrixDisplay("reducida", rrefMatrix)}</div>
                   ${solutionHtml}`,
                  calculationStepsHtml,
                )
              } else {
                // Actualizar matrices locales
                matrices[data.matrix_id] = {
                  rows: data.result.length,
                  cols: data.result[0].length,
                  data: data.result,
                }

                displayStoredMatrices()

                showResult(
                  "Eliminación Gauss-Jordan",
                  `<div class="operation-display">
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${matrixId}</span>
                      </div>
                      <span class="operation-symbol mx-2">→</span>
                      <div class="d-inline-block matrix-id-container">
                          <span class="matrix-id">${data.matrix_id}</span>
                      </div>
                   </div>
                   <p class="text-center">La forma escalonada reducida de la Matriz ${matrixId} es la Matriz ${data.matrix_id}:</p>
                   <div class="result-matrix">${generateMatrixDisplay(data.matrix_id, matrices[data.matrix_id])}</div>`,
                  calculationStepsHtml,
                )
              }
              break
          }
        } else {
          showAlert(data.message, "danger")
        }

        // Restaurar botón
        performSingleOperationBtn.innerHTML = "Realizar Operación"
        performSingleOperationBtn.disabled = false
      })
      .catch((error) => {
        console.error("Error:", error)
        showAlert("Error de comunicación con el servidor", "danger")

        // Restaurar botón
        performSingleOperationBtn.innerHTML = "Realizar Operación"
        performSingleOperationBtn.disabled = false
      })
  }

  function getOperationSymbol(operation) {
    switch (operation) {
      case "add":
        return "+"
      case "subtract":
        return "-"
      case "multiply":
        return "×"
      default:
        return ""
    }
  }

  // Función para mostrar resultados con los pasos de cálculo al lado en pantallas grandes
  function showResult(title, content, calculationStepsHtml = "") {
    // Si hay pasos de cálculo, crear un diseño de dos columnas
    if (calculationStepsHtml) {
      resultContainer.innerHTML = `
        <div class="result-card">
          <div class="result-content">
            <div class="result-layout">
              <div class="result-main">
                <h5 class="operation-title mb-3">${title}</h5>
                ${content}
              </div>
              <div class="calculation-details">
                <h5 class="mb-3">Pasos del cálculo:</h5>
                ${calculationStepsHtml}
              </div>
            </div>
          </div>
        </div>
      `
    } else {
      // Si no hay pasos de cálculo, mostrar solo el resultado
      resultContainer.innerHTML = `
        <div class="result-card">
          <div class="result-content">
            <h5 class="operation-title mb-3">${title}</h5>
            ${content}
          </div>
        </div>
      `
    }
  }

  function showAlert(message, type = "info") {
    const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas ${getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `

    resultContainer.innerHTML = alertHtml

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      const alertElement = document.querySelector(".alert")
      if (alertElement) {
        const bsAlert = bootstrap.Alert.getInstance(alertElement)
        if (bsAlert) {
          bsAlert.close()
        }
      }
    }, 5000)
  }

  function getAlertIcon(type) {
    switch (type) {
      case "success":
        return "fa-check-circle"
      case "danger":
        return "fa-exclamation-circle"
      case "warning":
        return "fa-exclamation-triangle"
      case "info":
      default:
        return "fa-info-circle"
    }
  }

  function deleteMatrix(matrixId) {
    const formData = new FormData()
    formData.append("matrix_id", matrixId)

    // Mostrar indicador de carga
    const matrixElement = document.querySelector(
      `.matrix-display:has(.delete-matrix-btn[data-matrix-id="${matrixId}"])`,
    )
    if (matrixElement) {
      matrixElement.innerHTML = `
                <div class="text-center py-4">
                    <div class="spinner-border text-danger" role="status">
                        <span class="visually-hidden">Eliminando...</span>
                    </div>
                    <p class="mt-2">Eliminando matriz...</p>
                </div>
            `
    }

    fetch("/delete_matrix", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert(data.message, "success")
          delete matrices[matrixId]
          displayStoredMatrices()
        } else {
          showAlert(data.message, "danger")
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        showAlert("Error de comunicación con el servidor", "danger")
      })
  }
})
