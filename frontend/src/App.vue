<template>
  <div class="container">
    <h1>Daily Appreciation Journal</h1>
    
    <div class="form-section">
      <form @submit.prevent="saveEntry">
        <div class="form-group">
          <label for="appreciation">Appreciation (something positive):</label>
          <textarea 
            id="appreciation" 
            v-model="form.appreciation" 
            rows="4" 
            required
            placeholder="What are you grateful for today?"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="negative">First Negative (something bad happening):</label>
          <textarea 
            id="negative" 
            v-model="form.negative" 
            rows="4" 
            required
            placeholder="What challenge did you face today?"
          ></textarea>
        </div>
        
        <button type="submit" class="btn-save">Save Entry</button>
        <div v-if="message" class="message" :class="message.type">{{ message.text }}</div>
      </form>
    </div>
    
    <div class="entries-section">
      <h2>Past Entries</h2>
      <div v-if="entries.length === 0" class="no-entries">No entries yet</div>
      <div v-for="entry in entries" :key="entry.id" class="entry">
        <h3>{{ entry.date }}</h3>
        <p><strong>Appreciation:</strong> {{ entry.appreciation }}</p>
        <p><strong>Negative:</strong> {{ entry.negative }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default {
  setup() {
    const form = ref({
      appreciation: '',
      negative: ''
    })
    const entries = ref([])
    const message = ref(null)
    
    const API = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    const saveEntry = async () => {
      try {
        const response = await API.post('/save', {
          appreciation: form.value.appreciation,
          negative: form.value.negative
        })
        message.value = { type: 'success', text: 'Entry saved successfully!' }
        form.value = { appreciation: '', negative: '' }
        loadEntries()
        setTimeout(() => { message.value = null }, 3000)
      } catch (error) {
        message.value = { type: 'error', text: 'Error saving entry: ' + error.message }
      }
    }
    
    const loadEntries = async () => {
      try {
        const response = await API.get('/entries')
        entries.value = response.data
      } catch (error) {
        console.error('Error loading entries:', error)
      }
    }
    
    onMounted(() => {
      loadEntries()
    })
    
    return {
      form,
      entries,
      message,
      saveEntry
    }
  }
}
</script>

<style scoped>
.container {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

h1 {
  color: #667eea;
  margin-bottom: 30px;
  text-align: center;
  font-size: 2.5em;
}

h2 {
  color: #667eea;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 1.5em;
}

.form-section {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 1.1em;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-family: inherit;
  font-size: 1em;
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
