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
          <label for="defaultStatuses"><b>Статуси в нових дошках за замовчуванням</b></label>
          <div v-for="(status, index) in defaultStatuses" :key="index" style="display: flex; gap: 10px;"class="status-item">
            <input style="max-width: 120px" placeholder="Ім'я" type="text" v-model="status.name" required>
            <ColorPicker v-model="status.color"/>
            <!-- <input type="color" v-model="status.color" required> -->
            <button style="background-color: red;" type="button" @click="removeStatus(index)">
              <img src="@/assets/trash.svg" alt="">
            </button>
          </div>
          <button style="width: 100%; margin-top: 10px; display: flex; justify-content: center;" type="button" @click="addStatus">
            <img src="@/assets/plus.svg" alt="">
          </button>
        </div>
        <div class="submit-button">
          <button style="width: 100%; background-color: green" type="submit"> Зберегти</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ColorPicker from './ColorPicker.vue';

export default {
  name: 'UserModal',
  components: {
    ColorPicker
  },
  data() {
    return {
      name: '',
      email: '',
      currentPassword: '',
      newPassword: '',
      defaultStatuses: [],
      backgrounds: [
          ["#000000", "black.PNG", "Чорний"],
          ["#00FFFF", "cyan.PNG", "Морський"],
          ["#808080", "gray.PNG", "Сірий"],
          ["#008000", "green.PNG", "Зелений"],
          ["#FFA500", "orange.PNG", "Оранжевий"],
          ["#FFC0CB", "pink.PNG", "Рожевий"],
          ["#800080", "purple.PNG", "Фіолетовий"],
          ["#FF0000", "red.PNG", "Червоний"],
          ["#FFCC99", "skin.PNG", "Шкіряний"],
          ["#FFFFFF", "white.PNG", "Білий"],
          ["#FFFF00", "yellow.PNG", "Жовтий"]
      ]
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    ...mapActions(['updateUserProfile']),
    closeModal() {
      this.$emit('close');
    },
    addStatus() {
      this.defaultStatuses.push({ name: '', color: 'white' })
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
    },
    print(e){
      console.log(e.target.value);
    }
  },
  mounted() {
    this.name = this.user?.name || '';
    this.email = this.user?.email || '';
    this.defaultStatuses = this.user?.settings?.defaultStatuses || [];
    console.log(this);
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
  z-index: 10001;
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