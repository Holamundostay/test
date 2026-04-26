<template>
  <div class="app">
    <!-- Login Screen -->
    <div v-if="!currentUser" class="login-container">
      <div class="login-box">
        <h1>🏥 Sistema de Inventario</h1>
        <h2>Quirófano CEYE</h2>
        <p>Selecciona tu usuario para continuar</p>
        
        <div class="user-selection">
          <div v-for="user in availableUsers" :key="user.id" class="user-card" @click="selectUser(user)">
            <div class="user-avatar">{{ user.full_name.charAt(0).toUpperCase() }}</div>
            <div class="user-info">
              <p class="user-name">{{ user.full_name }}</p>
              <p class="user-role">{{ user.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main App -->
    <div v-else class="main-container">
      <!-- Header -->
      <header class="app-header">
        <div class="header-left">
          <h1>🏥 Control de Inventario CEYE</h1>
          <p>Quirófano Esterilización</p>
        </div>
        <div class="header-right">
          <div class="user-badge">
            <span class="user-initial">{{ currentUser.full_name.charAt(0).toUpperCase() }}</span>
            <div class="user-info-badge">
              <p>{{ currentUser.full_name }}</p>
              <small>{{ currentUser.role }}</small>
            </div>
          </div>
          <button @click="logout" class="btn-logout">Salir</button>
        </div>
      </header>

      <!-- Navigation Tabs -->
      <nav class="nav-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </nav>

      <!-- Tab Content -->
      <main class="tab-content">
        
        <!-- 1. INVENTARIO ACTUAL -->
        <section v-if="activeTab === 'inventory'" class="content-section">
          <h2>📦 Inventario Actual</h2>
          
          <!-- Filtros -->
          <div class="filters">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar artículo..."
              class="search-input"
            />
            <select v-model="filterCategory" class="filter-select">
              <option value="">Todas las categorías</option>
              <option value="Instrumentos quirúrgicos">Instrumentos quirúrgicos</option>
              <option value="Medicamentos">Medicamentos</option>
              <option value="Materiales desechables">Materiales desechables</option>
              <option value="Equipo médico">Equipo médico</option>
              <option value="Otros">Otros</option>
            </select>
          </div>

          <!-- Items Grid -->
          <div class="items-grid">
            <div v-if="filteredItems.length === 0" class="no-items">
              No hay artículos que coincidan con la búsqueda
            </div>
            <div v-for="item in filteredItems" :key="item.id" class="item-card">
              <div class="item-header">
                <h3>{{ item.name }}</h3>
                <span class="category-badge">{{ item.category }}</span>
              </div>
              <p class="description">{{ item.description }}</p>
              
              <div class="item-stats">
                <div class="stat">
                  <label>Cantidad:</label>
                  <span class="quantity">{{ item.quantity }}</span>
                </div>
                <div class="stat">
                  <label>Última actualización:</label>
                  <small>{{ formatDate(item.last_updated) }}</small>
                </div>
                <div class="stat">
                  <label>Por:</label>
                  <small>{{ item.updated_by }}</small>
                </div>
              </div>

              <div class="item-actions">
                <button @click="openAdjustQuantity(item)" class="btn-adjust">
                  ✏️ Ajustar cantidad
                </button>
                <button @click="openCountItem(item)" class="btn-count">
                  📋 Realizar conteo
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- 2. AGREGAR NUEVO ARTÍCULO -->
        <section v-if="activeTab === 'add-item'" class="content-section">
          <h2>➕ Agregar Nuevo Artículo</h2>
          
          <form @submit.prevent="addNewItem" class="form">
            <div class="form-group">
              <label>Nombre del artículo *</label>
              <input v-model="newItem.name" type="text" required placeholder="Ej: Guantes quirúrgicos" />
            </div>

            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="newItem.description" rows="2" placeholder="Detalles del artículo"></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Cantidad inicial *</label>
                <input v-model.number="newItem.quantity" type="number" step="1" min="0" required />
              </div>

              <div class="form-group">
                <label>Categoría *</label>
                <select v-model="newItem.category" required>
                  <option value="">Seleccionar categoría</option>
                  <option value="Instrumentos quirúrgicos">Instrumentos quirúrgicos</option>
                  <option value="Medicamentos">Medicamentos</option>
                  <option value="Materiales desechables">Materiales desechables</option>
                  <option value="Equipo médico">Equipo médico</option>
                  <option value="Otros">Otros</option>
                </select>
              </div>
            </div>

            <button type="submit" class="btn-primary">Agregar Artículo</button>
            <div v-if="message" :class="['message', message.type]">{{ message.text }}</div>
          </form>
        </section>

        <!-- 3. REALIZAR CONTEO -->
        <section v-if="activeTab === 'count'" class="content-section">
          <h2>📋 Realizar Conteo de Inventario</h2>
          
          <!-- PASO 1: Elegir Gas o Vapor -->
          <div v-if="countStep === 'select_type'" class="count-type-selector">
            <h3>¿Qué quieres contar?</h3>
            <div class="type-buttons">
              <button class="type-btn gas-btn" @click="selectCountType('gas')">
                <span class="icon">⚙️</span>
                <span class="label">Gas</span>
              </button>
              <button class="type-btn vapor-btn" @click="selectCountType('vapor')">
                <span class="icon">💨</span>
                <span class="label">Vapor</span>
              </button>
            </div>
          </div>

          <!-- PASO 2: Contar items -->
          <div v-else-if="countStep === 'count_items'" class="count-items-section">
            <button type="button" @click="countStep = 'select_type'" class="btn-back">← Cambiar tipo</button>
            
            <h3>Conteo de Materiales - {{ countType === 'gas' ? '⚙️ Gas' : '💨 Vapor' }}</h3>
            
            <div class="items-count-list">
              <div v-for="item in items" :key="item.id" class="item-count-card">
                <div class="item-count-header">
                  <h4>{{ item.name }}</h4>
                  <small class="category">{{ item.category }}</small>
                </div>
                
                <div class="item-count-stats">
                  <div class="stat-row">
                    <span class="stat-label">Cantidad registrada:</span>
                    <span class="stat-value">{{ item.quantity }} pzas</span>
                  </div>
                  
                  <div class="stat-row">
                    <span class="stat-label">Cantidad encontrada:</span>
                    <input 
                      v-model.number="countingData[item.id].quantity_on_hand" 
                      type="number" 
                      step="1" 
                      min="0"
                      class="count-input"
                      placeholder="0"
                    />
                    <span class="stat-label"> pzas</span>
                  </div>
                  
                  <div v-if="countingData[item.id].quantity_on_hand !== null" class="stat-row difference">
                    <span class="stat-label">Diferencia:</span>
                    <span :class="{ 
                      'difference-value': true,
                      'positive': countingData[item.id].quantity_on_hand > item.quantity,
                      'negative': countingData[item.id].quantity_on_hand < item.quantity,
                      'equal': countingData[item.id].quantity_on_hand === item.quantity
                    }">
                      {{ countingData[item.id].quantity_on_hand > item.quantity ? '+' : '' }}{{ countingData[item.id].quantity_on_hand - item.quantity }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <button @click="submitBatchCount" class="btn-primary btn-save-count">💾 Guardar Conteo</button>
          </div>
        </section>

        <!-- 4. REPORTES Y HISTÓRICO -->
        <section v-if="activeTab === 'reports'" class="content-section">
          <h2>📊 Reportes y Histórico</h2>
          
          <div class="reports-container">
            <!-- Conteos recientes -->
            <div class="report-section">
              <h3>📋 Conteos Recientes</h3>
              <div class="filter-group">
                <input v-model="filterReportItem" type="text" placeholder="Filtrar por artículo...">
                <select v-model="filterReportUser">
                  <option value="">Todos los usuarios</option>
                  <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                    {{ user.full_name }}
                  </option>
                </select>
              </div>

              <div v-if="filteredCounts.length === 0" class="no-data">
                No hay conteos registrados
              </div>
              <div v-else class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>Artículo</th>
                      <th>Esperado</th>
                      <th>Encontrado</th>
                      <th>Diferencia</th>
                      <th>Usuario</th>
                      <th>Fecha</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="count in filteredCounts" :key="count.id" :class="{ 'discrepancy-row': count.discrepancy !== 0 }">
                      <td>{{ count.item.name }}</td>
                      <td>{{ count.expected_quantity }}</td>
                      <td>{{ count.quantity_on_hand }}</td>
                      <td :class="{ 'positive': count.discrepancy > 0, 'negative': count.discrepancy < 0, 'neutral': count.discrepancy === 0 }">
                        {{ count.discrepancy >= 0 ? '+' : '' }}{{ count.discrepancy }}
                      </td>
                      <td>{{ count.user.full_name }}</td>
                      <td>{{ formatDate(count.count_date) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Auditoría -->
            <div class="report-section">
              <h3>🔍 Auditoría de Cambios</h3>
              <div v-if="auditLogs.length === 0" class="no-data">
                No hay cambios registrados
              </div>
              <div v-else class="audit-list">
                <div v-for="log in auditLogs.slice(0, 50)" :key="log.id" class="audit-entry">
                  <span class="action-badge" :class="log.action">{{ log.action }}</span>
                  <div class="entry-content">
                    <strong>{{ log.item.name }}</strong>
                    <p v-if="log.action === 'counted'">
                      Conteo realizado por <strong>{{ log.user.full_name }}</strong>
                    </p>
                    <p v-else>
                      Cambio de {{ log.old_quantity }} → {{ log.new_quantity }} por <strong>{{ log.user ? log.user.full_name : 'Sistema' }}</strong>
                    </p>
                    <small>{{ formatDate(log.action_date) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <!-- Modales -->
    <!-- Modal para ajustar cantidad -->
    <div v-if="showAdjustModal" class="modal-overlay" @click="showAdjustModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Ajustar cantidad: {{ adjustingItem?.name }}</h3>
          <button @click="showAdjustModal = false" class="btn-close">✕</button>
        </div>
        <form @submit.prevent="applyQuantityAdjustment" class="modal-body">
          <div class="form-group">
            <label>Cantidad actual: <strong>{{ adjustingItem?.quantity }}</strong></label>
          </div>
          <div class="form-group">
            <label>Nueva cantidad *</label>
            <input v-model.number="adjustForm.newQuantity" type="number" step="1" min="0" required autofocus />
          </div>
          <div class="form-group">
            <label>Ajuste (diferencia)</label>
            <input 
              :value="adjustForm.newQuantity - (adjustingItem?.quantity || 0)" 
              type="number" 
              disabled 
            />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Aplicar cambio</button>
            <button type="button" @click="showAdjustModal = false" class="btn-secondary">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default {
  name: 'App',
  setup() {
    // State
    const currentUser = ref(null)
    const availableUsers = ref([])
    const items = ref([])
    const counts = ref([])
    const auditLogs = ref([])
    const activeTab = ref('inventory')
    const message = ref(null)

    // Form states
    const newItem = ref({
      name: '',
      description: '',
      quantity: 0,
      category: ''
    })

    const countForm = ref({
      quantity_on_hand: null,
      count_type: 'gas',
      notes: ''
    })

    // Nuevo: Estado para flujo de conteo por tipo
    const countStep = ref('select_type') // 'select_type' o 'count_items'
    const countType = ref('gas') // 'gas' o 'vapor'
    const countingData = ref({}) // { itemId: { quantity_on_hand: number } }

    const adjustForm = ref({
      newQuantity: 0
    })

    // UI States
    const countingItem = ref(null)
    const adjustingItem = ref(null)
    const showAdjustModal = ref(false)
    const searchQuery = ref('')
    const filterCategory = ref('')
    const filterReportItem = ref('')
    const filterReportUser = ref('')

    // Axios instance
    const API = axios.create({
      baseURL: API_URL,
      headers: { 'Content-Type': 'application/json' }
    })

    // Tab definitions
    const tabs = [
      { id: 'inventory', label: 'Inventario', icon: '📦' },
      { id: 'add-item', label: 'Agregar artículo', icon: '➕' },
      { id: 'count', label: 'Realizar conteo', icon: '📋' },
      { id: 'reports', label: 'Reportes', icon: '📊' }
    ]

    // Computed properties
    const filteredItems = computed(() => {
      return items.value.filter(item => {
        const matchesSearch = item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                            item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCategory = !filterCategory.value || item.category === filterCategory.value
        return matchesSearch && matchesCategory
      })
    })

    const filteredCounts = computed(() => {
      return counts.value.filter(count => {
        const matchesItem = !filterReportItem.value || 
                          count.item.name.toLowerCase().includes(filterReportItem.value.toLowerCase())
        const matchesUser = !filterReportUser.value || count.user_id === parseInt(filterReportUser.value)
        return matchesItem && matchesUser
      })
    })

    // Methods
    const selectUser = (user) => {
      currentUser.value = user
      loadData()
    }

    const logout = () => {
      currentUser.value = null
      activeTab.value = 'inventory'
    }

    const loadData = async () => {
      try {
        const [itemsRes, countsRes, logsRes] = await Promise.all([
          API.get('/items'),
          API.get('/counts'),
          API.get('/audit-logs')
        ])
        items.value = itemsRes.data
        counts.value = countsRes.data
        auditLogs.value = logsRes.data
      } catch (error) {
        console.error('Error loading data:', error)
        showMessage('Error cargando datos', 'error')
      }
    }

    const loadUsers = async () => {
      try {
        const res = await API.get('/users')
        availableUsers.value = res.data
      } catch (error) {
        console.error('Error loading users:', error)
      }
    }

    const addNewItem = async () => {
      if (!newItem.value.name || !newItem.value.category || newItem.value.quantity < 0) {
        showMessage('Por favor completa los campos obligatorios', 'error')
        return
      }

      try {
        await API.post('/items', {
          ...newItem.value,
          updated_by: currentUser.value.full_name
        })
        showMessage('Artículo agregado exitosamente', 'success')
        newItem.value = { name: '', description: '', quantity: 0, category: '' }
        activeTab.value = 'inventory'
        await loadData()
      } catch (error) {
        showMessage('Error agregando artículo: ' + error.message, 'error')
      }
    }

    const openAdjustQuantity = (item) => {
      adjustingItem.value = item
      adjustForm.value.newQuantity = item.quantity
      showAdjustModal.value = true
    }

    const applyQuantityAdjustment = async () => {
      if (adjustForm.value.newQuantity < 0) {
        showMessage('La cantidad no puede ser negativa', 'error')
        return
      }

      try {
        await API.put(`/items/${adjustingItem.value.id}`, {
          quantity: adjustForm.value.newQuantity,
          updated_by: currentUser.value.full_name
        })
        showMessage('Cantidad actualizada', 'success')
        showAdjustModal.value = false
        await loadData()
      } catch (error) {
        showMessage('Error actualizando cantidad: ' + error.message, 'error')
      }
    }

    const selectCountType = (type) => {
      countType.value = type
      countStep.value = 'count_items'
      // Inicializar el objeto de datos de conteo
      countingData.value = {}
      items.value.forEach(item => {
        countingData.value[item.id] = { quantity_on_hand: null }
      })
    }

    const submitBatchCount = async () => {
      // Validar que al menos un item tenga cantidad registrada
      const hasData = Object.values(countingData.value).some(data => data.quantity_on_hand !== null)
      if (!hasData) {
        showMessage('Por favor ingresa al menos una cantidad', 'error')
        return
      }

      try {
        // Enviar cada conteo al servidor
        for (const item of items.value) {
          if (countingData.value[item.id]?.quantity_on_hand !== null) {
            await API.post('/counts', {
              item_id: item.id,
              user_id: currentUser.value.id,
              quantity_on_hand: countingData.value[item.id].quantity_on_hand,
              expected_quantity: item.quantity,
              count_type: countType.value
            })
          }
        }
        showMessage('Conteo registrado exitosamente', 'success')
        countStep.value = 'select_type'
        countingData.value = {}
        await loadData()
        activeTab.value = 'reports'
      } catch (error) {
        showMessage('Error registrando conteo: ' + error.message, 'error')
      }
    }

    const openCountItem = (item) => {
      countingItem.value = item
      countForm.value = {
        quantity_on_hand: null,
        count_type: 'gas',
        notes: ''
      }
      activeTab.value = 'count'
    }

    const submitCount = async () => {
      if (countForm.value.quantity_on_hand === null) {
        showMessage('Por favor ingresa la cantidad encontrada', 'error')
        return
      }

      try {
        await API.post('/counts', {
          item_id: countingItem.value.id,
          user_id: currentUser.value.id,
          quantity_on_hand: countForm.value.quantity_on_hand,
          expected_quantity: countingItem.value.quantity,
          count_type: countForm.value.count_type,
          notes: countForm.value.notes
        })
        showMessage('Conteo registrado exitosamente', 'success')
        countingItem.value = null
        activeTab.value = 'reports'
        await loadData()
      } catch (error) {
        showMessage('Error registrando conteo: ' + error.message, 'error')
      }
    }

    const showMessage = (text, type) => {
      message.value = { text, type }
      setTimeout(() => { message.value = null }, 4000)
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('es-ES')
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      currentUser,
      availableUsers,
      items,
      counts,
      auditLogs,
      activeTab,
      tabs,
      message,
      newItem,
      countForm,
      adjustForm,
      countingItem,
      adjustingItem,
      showAdjustModal,
      searchQuery,
      filterCategory,
      filterReportItem,
      filterReportUser,
      filteredItems,
      filteredCounts,
      countStep,
      countType,
      countingData,
      selectUser,
      logout,
      addNewItem,
      openAdjustQuantity,
      applyQuantityAdjustment,
      openCountItem,
      submitCount,
      selectCountType,
      submitBatchCount,
      formatDate
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ============ LOGIN ============ */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.login-box h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 10px;
}

.login-box h2 {
  font-size: 1.5em;
  color: #667eea;
  margin-bottom: 20px;
}

.login-box p {
  color: #7f8c8d;
  margin-bottom: 30px;
  font-size: 1.1em;
}

.user-selection {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 30px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 2px solid #ecf0f1;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-card:hover {
  border-color: #667eea;
  background: #f8f9ff;
  transform: translateY(-5px);
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.5em;
  flex-shrink: 0;
}

.user-info {
  text-align: left;
}

.user-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 3px;
}

.user-role {
  font-size: 0.9em;
  color: #95a5a6;
  text-transform: capitalize;
}

/* ============ MAIN CONTAINER ============ */
.main-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f5f7fa;
}

.app-header {
  background: white;
  padding: 20px 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.header-left p {
  color: #7f8c8d;
  font-size: 0.9em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-initial {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2em;
}

.user-info-badge {
  text-align: left;
}

.user-info-badge p {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
}

.user-info-badge small {
  color: #7f8c8d;
  text-transform: capitalize;
}

.btn-logout {
  padding: 8px 15px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

/* ============ NAVIGATION ============ */
.nav-tabs {
  background: white;
  padding: 15px 30px;
  display: flex;
  gap: 10px;
  border-bottom: 2px solid #ecf0f1;
  overflow-x: auto;
}

.tab-button {
  padding: 10px 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #7f8c8d;
  font-weight: 600;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
}

.tab-button:hover {
  color: #667eea;
}

.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

/* ============ CONTENT ============ */
.tab-content {
  flex: 1;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.content-section {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.content-section h2 {
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 1.8em;
}

/* ============ FILTERS ============ */
.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.search-input,
.filter-select {
  flex: 1;
  padding: 10px 15px;
  border: 2px solid #ecf0f1;
  border-radius: 5px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

/* ============ ITEMS GRID ============ */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.item-card {
  background: white;
  border: 2px solid #ecf0f1;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
}

.item-card:hover {
  border-color: #667eea;
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
  transform: translateY(-5px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.item-header h3 {
  color: #2c3e50;
  margin: 0;
  flex: 1;
}

.category-badge {
  background: #ecf0f1;
  color: #2c3e50;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: 600;
  white-space: nowrap;
}

.description {
  color: #7f8c8d;
  font-size: 0.95em;
  margin-bottom: 15px;
}

.item-stats {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: grid;
  gap: 10px;
}

.stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.95em;
}

.stat label {
  color: #7f8c8d;
  font-weight: 600;
}

.quantity {
  color: #667eea;
  font-weight: bold;
  font-size: 1.1em;
}

.item-actions {
  display: flex;
  gap: 10px;
}

.btn-adjust,
.btn-count {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.95em;
}

.btn-adjust {
  background: #3498db;
  color: white;
}

.btn-adjust:hover {
  background: #2980b9;
}

.btn-count {
  background: #667eea;
  color: white;
}

.btn-count:hover {
  background: #5568d3;
}

/* ============ FORMS ============ */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.95em;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 12px;
  border: 2px solid #ecf0f1;
  border-radius: 5px;
  font-size: 1em;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.form-group small {
  color: #7f8c8d;
  font-size: 0.85em;
}

.form-group .discrepancy {
  font-weight: bold;
  margin-top: 5px;
}

.form-group .discrepancy.positive {
  color: #27ae60;
}

.form-group .discrepancy.negative {
  color: #e74c3c;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.btn-primary,
.btn-secondary,
.btn-back {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1em;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #ecf0f1;
  color: #2c3e50;
}

.btn-secondary:hover {
  background: #bdc3c7;
}

.btn-back {
  background: #95a5a6;
  color: white;
  align-self: flex-start;
  margin-bottom: 10px;
}

.btn-back:hover {
  background: #7f8c8d;
}

.btn-small {
  padding: 5px 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-small:hover {
  background: #5568d3;
}

.message {
  padding: 12px 15px;
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

/* ============ COUNTING ============ */
.count-start {
  text-align: center;
  color: #7f8c8d;
  margin-bottom: 30px;
}

.count-start p {
  font-size: 1.1em;
  margin-bottom: 20px;
}

.items-list-simple {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 500px;
  overflow-y: auto;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.item-row:hover {
  background: #ecf0f1;
}

.count-form {
  max-width: 600px;
}

.count-item-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #667eea;
}

.count-item-info h3 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.stock-info {
  color: #667eea;
  font-weight: 600;
  margin-top: 10px;
}

/* ============ REPORTS ============ */
.reports-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.report-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.report-section h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.filter-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-group input,
.filter-group select {
  flex: 1;
  padding: 10px;
  border: 2px solid #ecf0f1;
  border-radius: 5px;
  font-size: 0.95em;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #667eea;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.data-table thead {
  background: #ecf0f1;
}

.data-table th {
  padding: 12px;
  text-align: left;
  color: #2c3e50;
  font-weight: 600;
  border-bottom: 2px solid #bdc3c7;
}

.data-table td {
  padding: 12px;
  border-bottom: 1px solid #ecf0f1;
}

.data-table tbody tr:hover {
  background: #f8f9fa;
}

.data-table .discrepancy-row {
  background: #fff3cd;
}

.data-table .positive {
  color: #27ae60;
  font-weight: 600;
}

.data-table .negative {
  color: #e74c3c;
  font-weight: 600;
}

.data-table .neutral {
  color: #7f8c8d;
}

.no-data {
  text-align: center;
  color: #7f8c8d;
  padding: 30px;
  background: white;
  border-radius: 5px;
}

.audit-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 600px;
  overflow-y: auto;
}

.audit-entry {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.action-badge {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: 600;
  white-space: nowrap;
  text-transform: uppercase;
  flex-shrink: 0;
}

.action-badge.created {
  background: #d4edda;
  color: #155724;
}

.action-badge.updated {
  background: #cce5ff;
  color: #004085;
}

.action-badge.counted {
  background: #fff3cd;
  color: #856404;
}

.action-badge.deleted {
  background: #f8d7da;
  color: #721c24;
}

.entry-content {
  flex: 1;
}

.entry-content strong {
  color: #2c3e50;
}

.entry-content p {
  margin: 5px 0;
  color: #7f8c8d;
  font-size: 0.95em;
}

.entry-content small {
  color: #95a5a6;
  font-size: 0.85em;
}

.no-items {
  text-align: center;
  color: #7f8c8d;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* ============ MODALES ============ */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 2px solid #ecf0f1;
}

.modal-header h3 {
  color: #2c3e50;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5em;
  color: #7f8c8d;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #2c3e50;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.form-actions button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* ============ RESPONSIVE ============ */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .header-right {
    flex-direction: column;
    gap: 10px;
    align-items: flex-end;
  }

  .nav-tabs {
    flex-wrap: wrap;
  }

  .filters {
    flex-direction: column;
  }

  .data-table {
    font-size: 0.9em;
  }

  .data-table th,
  .data-table td {
    padding: 8px;
  }

  .user-selection {
    grid-template-columns: 1fr;
  }
}

/* ===== NUEVOS ESTILOS PARA CONTEO POR TIPO ===== */

.count-type-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
  text-align: center;
}

.count-type-selector h3 {
  font-size: 28px;
  margin-bottom: 50px;
  font-weight: 600;
}

.type-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
  max-width: 500px;
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  color: #333;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.type-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.type-btn .icon {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
}

.type-btn .label {
  font-size: 20px;
}

.gas-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.gas-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #6a4195 100%);
}

.vapor-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.vapor-btn:hover {
  background: linear-gradient(135deg, #d97dde 0%, #e23a55 100%);
}

/* Sección de conteo de items */
.count-items-section {
  padding: 20px 0;
}

.count-items-section h3 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 22px;
  color: #333;
}

.items-count-list {
  max-height: 600px;
  overflow-y: auto;
  padding: 20px 0;
  margin-bottom: 30px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.item-count-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
}

.item-count-card:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.item-count-header {
  margin-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.item-count-header h4 {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #333;
}

.item-count-header .category {
  color: #888;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.item-count-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
}

.stat-label {
  flex: 0 0 auto;
  font-weight: 500;
  color: #666;
  font-size: 14px;
  min-width: 160px;
}

.stat-value {
  flex: 1;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.count-input {
  flex: 1;
  padding: 10px 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  text-align: right;
  transition: all 0.3s ease;
}

.count-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.stat-row.difference {
  background: #f9f9f9;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #ffc107;
  margin-top: 8px;
}

.difference-value {
  font-size: 18px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 6px;
  background: #f0f0f0;
}

.difference-value.positive {
  background: #d4edda;
  color: #155724;
}

.difference-value.negative {
  background: #f8d7da;
  color: #721c24;
}

.difference-value.equal {
  background: #d1ecf1;
  color: #0c5460;
}

.btn-save-count {
  width: 100%;
  padding: 16px;
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.btn-save-count:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-save-count:active {
  transform: translateY(0);
}

/* Scroll personalizado */
.items-count-list::-webkit-scrollbar {
  width: 8px;
}

.items-count-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.items-count-list::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 10px;
}

.items-count-list::-webkit-scrollbar-thumb:hover {
  background: #5568d3;
}
</style>
