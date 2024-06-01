<template>
  <div class="register-page">
    <div class="register-form">
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <input type="text" id="name" v-model="name" required placeholder="Ім'я">
        </div>
        <div class="form-group">
          <input type="email" id="email" v-model="email" @blur="validateEmail" required placeholder="Електронна пошта">
          <div class="error" v-if="emailError">{{ emailError }}</div>
        </div>
        <div class="form-group">
          <input type="password" id="password" v-model="password" @blur="validatePassword" required placeholder="Пароль">
          <div class="error" v-if="passwordError">{{ passwordError }}</div>
        </div>
        <div class="form-group">
          <input type="password" id="confirmPassword" v-model="confirmPassword" @blur="validateConfirmPassword" required placeholder="Повторіть пароль">
          <div class="error" v-if="confirmPasswordError">{{ confirmPasswordError }}</div>
        </div>
        <button type="submit">Зареєструватись</button>
      </form>
      <p>Вже маєте акаунт? <router-link to="/login" class="link">Увійти</router-link></p>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { validateEmail, validatePassword } from '@/utils/validation'

export default {
  name: 'RegisterPage',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      emailError: '',
      passwordError: '',
      confirmPasswordError: ''
    }
  },
  methods: {
    ...mapActions(['register']),
    async handleRegister() {
      if (this.validateForm()) {
        const response = await this.register({ name: this.name, email: this.email, password: this.password })
        if (response.status === 201) {
          this.$router.push('/')
          location.reload()
        } else {
          // Handle registration error
        }
      }
    },
    validateForm() {
      this.emailError = validateEmail(this.email) ? '' : 'Некоректна пошта'
      this.passwordError = validatePassword(this.password) ? '' : 'Некоректний пароль'
      this.confirmPasswordError = this.password === this.confirmPassword ? '' : 'Паролі не співпадають'
      return !this.emailError && !this.passwordError && !this.confirmPasswordError
    },
    validateEmail() {
      this.emailError = validateEmail(this.email) ? '' : 'Некоректна пошта'
    },
    validatePassword() {
      this.passwordError = validatePassword(this.password) ? '' : 'Некоректний пароль'
    },
    validateConfirmPassword() {
      this.confirmPasswordError = this.password === this.confirmPassword ? '' : 'Паролі не співпадають'
    }
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.register-form {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  filter: drop-shadow(2px 2px 2px grey);
  background-color: white;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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