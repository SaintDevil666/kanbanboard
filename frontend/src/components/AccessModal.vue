<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2>Налаштування доступу</h2>
      <div class="access-settings">
        <label>
          <input type="checkbox" v-model="publicAccess">
          Публічний доступ за посиланням
        </label>
      </div>
      <div class="invited-users">
        <h3>Запросити користувачів</h3>
        <ul>
          <li v-for="user in board.invited" :key="user.id">
            {{ user.name }} ({{ user.email }})
            <button @click="removeUser(user.id)">Видалити</button>
          </li>
        </ul>
        <div class="invite-user">
          <input type="email" v-model="inviteEmail" placeholder="Напишіть email для запрошення">
          <button @click="inviteUser">Запросити</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'AccessModal',
  props: {
    board: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      publicAccess: false,
      inviteEmail: ''
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    ...mapActions(['updateBoardPublicAccess', 'inviteUserToBoard', 'removeUserFromBoard']),
    getUserById(userId) {
      // Реалізувати отримання об'єкта користувача за його ID
    },
    closeModal() {
      this.$emit('close');
    },
    async updatePublicAccess() {
      await this.updateBoardPublicAccess({ boardId: this.board.id, publicAccess: this.publicAccess })
    },
    async inviteUser() {
      if (this.inviteEmail) {
        await this.inviteUserToBoard({ boardId: this.board.id, email: this.inviteEmail })
        this.inviteEmail = ''
      }
    },
    async removeUser(userId) {
      await this.removeUserFromBoard({ boardId: this.board.id, userId })
    }
  },
  mounted() {
    this.publicAccess = this.board.publicAccess
  },
  watch: {
    publicAccess(newValue) {
      this.updatePublicAccess()
    }
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

.access-settings {
  margin-bottom: 20px;
}

.invited-users ul {
  list-style-type: none;
  padding: 0;
}

.invited-users li {
  margin-bottom: 10px;
}

.invite-user {
  margin-top: 20px;
}

.invite-user input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

button {
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>