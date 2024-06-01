<template>
  <div class="login-page">
    <div class="login-form">
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <!-- <label for="email">E-mail</label> -->
          <input type="email" id="email" v-model="email" @blur="validateEmail" required placeholder="Електронна пошта">
          <div class="error" v-if="emailError">{{ emailError }}</div>
        </div>
        <div class="form-group">
          <!-- <label for="password">Пароль</label> -->
          <input type="password" id="password" v-model="password" @blur="validatePassword" required placeholder="Пароль">
          <div class="error" v-if="passwordError">{{ passwordError }}</div>
        </div>
        <button type="submit">Вхід</button>
      </form>
      <p>Ще не маєте акаунту? <router-link to="/register" class="link">Створити!</router-link></p>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { validateEmail, validatePassword } from '@/utils/validation'

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      emailError: '',
      passwordError: ''
    }
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      if (this.validateForm()) {
        const response = await this.login({ email: this.email, password: this.password })
        if (response.status === 200) {
          this.$router.push('/')
        } else {
          // Handle login error
        }
      }
    },
    validateForm() {
      this.emailError = validateEmail(this.email) ? '' : 'Invalid email'
      this.passwordError = validatePassword(this.password) ? '' : 'Invalid password'
      return !this.emailError && !this.passwordError
    },
    validateEmail() {
      this.emailError = validateEmail(this.email) ? '' : 'Invalid email'
    },
    validatePassword() {
      this.passwordError = validatePassword(this.password) ? '' : 'Invalid password'
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-form {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: white;
  filter: drop-shadow(2px 2px 2px grey);
}
form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.form-group {
  margin-bottom: 10px;
}
.link {
  color: blue;
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

.error {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

button {
  width: fit-content;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

p {
  margin-top: 10px;
  text-align: center;
}
</style>