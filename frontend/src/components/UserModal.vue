<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <form @submit.prevent="handleUpdateProfile">
        <div class="form-group">
          <label for="name">Ім'я</label>
          <input type="text" id="name" v-model="name" required>
        </div>
        <div class="form-group">
          <label for="email">E-mail</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <h2><b>Зміна паролю</b></h2>
        <div class="form-group">
          <label for="currentPassword">Поточний</label>
          <input type="password" id="currentPassword" v-model="currentPassword">
        </div>
        <div class="form-group">
          <label for="newPassword">Новий пароль</label>
          <input type="password" id="newPassword" v-model="newPassword">
        </div>
        <div class="form-group">
          <label for="defaultStatuses">Статуси в нових дошках за замовчуванням</label>
          <div v-for="(status, index) in defaultStatuses" :key="index" class="status-item">
            <input type="text" v-model="status.name" required>
            <input type="color" v-model="status.color" required>
            <button type="button" @click="removeStatus(index)">Видалити</button>
          </div>
          <button type="button" @click="addStatus">Додати</button>
        </div>
        <div class="submit-button">
          <button type="submit"> Зберегти</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'UserModal',
  data() {
    return {
      name: '',
      email: '',
      currentPassword: '',
      newPassword: '',
      defaultStatuses: []
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    ...mapActions(['updateUserProfile']),
    closeModal() {
      this.$emit('close')
    },
    addStatus() {
      this.defaultStatuses.push({ name: '', color: '#000000' })
    },
    removeStatus(index) {
      this.defaultStatuses.splice(index, 1)
    },
    async handleUpdateProfile() {
      const settings = {
        name: this.name,
        email: this.email,
        currentPassword: this.currentPassword,
        newPassword: this.newPassword,
        settings: { defaultStatuses: this.defaultStatuses }
      }
      const response = await this.updateUserProfile(settings)
      if (response.status === 200) {
        this.closeModal()
      } else {
        // Handle update error
      }
    }
  },
  mounted() {
    this.name = this.user?.name || ''
    this.email = this.user?.email || ''
    this.defaultStatuses = this.user?.settings?.defaultStatuses || []
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  max-width: 400px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.status-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.status-item input[type="text"] {
  flex: 1;
  margin-right: 5px;
}

.status-item input[type="color"] {
  width: 30px;
  height: 30px;
  border: none;
  padding: 0;
  margin-right: 5px;
}

button {
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button{
  display:flex;
  justify-content: center;
}
</style>