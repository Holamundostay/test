<template>
  <div class="container">
    <h1>Control de Inventario - Quirófano Ceye</h1>

    <div class="shift-info">
      <label for="currentShift">Turno actual:</label>
      <select id="currentShift" v-model="currentShift">
        <option value="Mañana">Mañana</option>
        <option value="Tarde">Tarde</option>
        <option value="Noche">Noche</option>
      </select>
    </div>

    <div class="form-section">
      <h2>Agregar Nuevo Artículo</h2>
      <form @submit.prevent="createItem">
        <div class="form-group">
          <label for="name">Nombre del artículo:</label>
          <input
            id="name"
            v-model="newItem.name"
            required
            placeholder="Ej: Guantes quirúrgicos"
          />
        </div>

        <div class="form-group">
          <label for="description">Descripción:</label>
          <textarea
            id="description"
            v-model="newItem.description"
            rows="2"
            placeholder="Descripción del artículo"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="quantity">Cantidad inicial:</label>
            <input
              id="quantity"
              v-model.number="newItem.quantity"
              type="number"
              step="0.01"
              min="0"
              required
            />
          </div>

          <div class="form-group">
            <label for="category">Categoría:</label>
            <select id="category" v-model="newItem.category" required>
              <option value="">Seleccionar categoría</option>
              <option value="Instrumentos quirúrgicos">Instrumentos quirúrgicos</option>
              <option value="Medicamentos">Medicamentos</option>
              <option value="Materiales desechables">Materiales desechables</option>
              <option value="Equipo médico">Equipo médico</option>
              <option value="Otros">Otros</option>
            </select>
          </div>
        </div>

        <button type="submit" class="btn-save">Agregar Artículo</button>
        <div v-if="message" class="message" :class="message.type">{{ message.text }}</div>
      </form>
    </div>

    <div class="filter-section">
      <label for="filterCategory">Filtrar por categoría:</label>
      <select id="filterCategory" v-model="filterCategory" @change="filterItems">
        <option value="">Todas las categorías</option>
        <option value="Instrumentos quirúrgicos">Instrumentos quirúrgicos</option>
        <option value="Medicamentos">Medicamentos</option>
        <option value="Materiales desechables">Materiales desechables</option>
        <option value="Equipo médico">Equipo médico</option>
        <option value="Otros">Otros</option>
      </select>
    </div>

    <div class="items-section">
      <h2>Inventario Actual</h2>
      <div v-if="filteredItems.length === 0" class="no-items">No hay artículos en el inventario</div>
      <div v-for="item in filteredItems" :key="item.id" class="item-card">
        <div class="item-header">
          <h3>{{ item.name }}</h3>
          <span class="category">{{ item.category }}</span>
        </div>
        <p class="description">{{ item.description }}</p>
        <div class="item-details">
          <div class="quantity-section">
            <label>Cantidad actual: <strong>{{ item.quantity }}</strong></label>
            <div class="quantity-controls">
              <button @click="adjustQuantity(item, -1)" class="btn-adjust">-</button>
              <input
                v-model.number="adjustAmounts[item.id]"
                type="number"
                step="0.01"
                min="-999"
                max="999"
                placeholder="0"
                class="adjust-input"
              />
              <button @click="adjustQuantity(item, 1)" class="btn-adjust">+</button>
              <button @click="applyAdjustment(item)" class="btn-apply">Aplicar</button>
            </div>
          </div>
          <div class="item-info">
            <p><small>Última actualización: {{ formatDate(item.last_updated) }}</small></p>
            <p><small>Actualizado por: {{ item.updated_by }}</small></p>
          </div>
        </div>
        <button @click="deleteItem(item)" class="btn-delete">Eliminar</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default {
  setup() {
    const currentShift = ref('Mañana')
    const newItem = ref({
      name: '',
      description: '',
      quantity: 0,
      category: '',
      location: 'Quirófano Ceye'
    })
    const items = ref([])
    const filterCategory = ref('')
    const filteredItems = ref([])
    const adjustAmounts = ref({})
    const message = ref(null)

    const API = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const createItem = async () => {
      try {
        const response = await API.post('/items', {
          ...newItem.value,
          updated_by: currentShift.value
        })
        message.value = { type: 'success', text: 'Artículo agregado exitosamente!' }
        newItem.value = { name: '', description: '', quantity: 0, category: '', location: 'Quirófano Ceye' }
        loadItems()
        setTimeout(() => { message.value = null }, 3000)
      } catch (error) {
        message.value = { type: 'error', text: 'Error agregando artículo: ' + error.message }
      }
    }

    const loadItems = async () => {
      try {
        const response = await API.get('/items')
        items.value = response.data
        filterItems()
      } catch (error) {
        console.error('Error loading items:', error)
      }
    }

    const filterItems = () => {
      if (filterCategory.value === '') {
        filteredItems.value = items.value
      } else {
        filteredItems.value = items.value.filter(item => item.category === filterCategory.value)
      }
    }

    const adjustQuantity = (item, direction) => {
      const current = adjustAmounts.value[item.id] || 0
      adjustAmounts.value[item.id] = current + direction
    }

    const applyAdjustment = async (item) => {
      const adjustment = adjustAmounts.value[item.id] || 0
      if (adjustment === 0) return

      const newQuantity = item.quantity + adjustment
      if (newQuantity < 0) {
        alert('La cantidad no puede ser negativa')
        return
      }

      try {
        await API.put(`/items/${item.id}`, {
          quantity: newQuantity,
          updated_by: currentShift.value
        })
        adjustAmounts.value[item.id] = 0
        loadItems()
        message.value = { type: 'success', text: 'Cantidad actualizada!' }
        setTimeout(() => { message.value = null }, 2000)
      } catch (error) {
        message.value = { type: 'error', text: 'Error actualizando cantidad: ' + error.message }
      }
    }

    const deleteItem = async (item) => {
      if (!confirm(`¿Está seguro de eliminar "${item.name}"?`)) return

      try {
        await API.delete(`/items/${item.id}`)
        loadItems()
        message.value = { type: 'success', text: 'Artículo eliminado!' }
        setTimeout(() => { message.value = null }, 2000)
      } catch (error) {
        message.value = { type: 'error', text: 'Error eliminando artículo: ' + error.message }
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('es-ES')
    }

    onMounted(() => {
      loadItems()
    })

    return {
      currentShift,
      newItem,
      items,
      filterCategory,
      filteredItems,
      adjustAmounts,
      message,
      createItem,
      loadItems,
      filterItems,
      adjustQuantity,
      applyAdjustment,
      deleteItem,
      formatDate
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
  font-size: 2.5em;
}

h2 {
  color: #34495e;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 1.5em;
}

.shift-info {
  text-align: center;
  margin-bottom: 30px;
}

.shift-info label {
  margin-right: 10px;
  font-weight: 600;
}

.shift-info select {
  padding: 8px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1em;
}

.form-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  margin-bottom: 15px;
  flex: 1;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
  font-weight: 600;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-family: inherit;
  font-size: 1em;
}

textarea {
  resize: vertical;
}

.btn-save {
  background: #27ae60;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  margin-top: 10px;
}

.btn-save:hover {
  background: #229954;
}

.filter-section {
  margin-bottom: 20px;
  text-align: center;
}

.items-section {
  margin-top: 30px;
}

.no-items {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
  padding: 40px;
}

.item-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.item-header h3 {
  margin: 0;
  color: #2c3e50;
}

.category {
  background: #3498db;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: 600;
}

.description {
  color: #7f8c8d;
  margin-bottom: 15px;
}

.item-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.quantity-section {
  flex: 1;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.btn-adjust {
  background: #95a5a6;
  color: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-adjust:hover {
  background: #7f8c8d;
}

.adjust-input {
  width: 80px;
  text-align: center;
}

.btn-apply {
  background: #f39c12;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-apply:hover {
  background: #e67e22;
}

.item-info {
  text-align: right;
  color: #7f8c8d;
}

.btn-delete {
  background: #e74c3c;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-delete:hover {
  background: #c0392b;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  font-weight: 600;
}

.message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
  resize: vertical;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  transition: transform 0.2s;
  margin-top: 10px;
}

.btn-save:hover {
  transform: scale(1.05);
}

.btn-save:active {
  transform: scale(0.95);
}

.message {
  margin-top: 15px;
  padding: 12px;
  border-radius: 5px;
  text-align: center;
  font-weight: 600;
}

.message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.entries-section {
  margin-top: 30px;
}

.no-entries {
  text-align: center;
  color: #999;
  padding: 20px;
  font-style: italic;
}

.entry {
  background: #f8f9fa;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.entry h3 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 1.2em;
}

.entry p {
  color: #555;
  margin: 8px 0;
  line-height: 1.6;
}

.entry strong {
  color: #333;
}
</style>
