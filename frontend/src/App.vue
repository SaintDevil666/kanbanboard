<template>
    <div id="app">
        <nav style="display: flex; flex-direction: row; align-items: center; padding: 10px;">
            <img @click="$router.push('/')" class="logo" src="@/assets/logo.png" alt="">
            <div @click="openUserModal" class="user">
                <img src="@/assets/user.svg" alt="">
            </div>
        </nav>
        <router-view class="router-view"/>
        <user-modal v-if="showUserModal" @close="closeUserModal"/>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import UserModal from '@/components/UserModal.vue'

export default {
    name: 'App',
    components: {
        UserModal
    },
    data() {
        return {
            showUserModal: false
        }
    },
    computed: {
        ...mapGetters(['isAuthenticated'])
    },
    methods: {
        ...mapActions(['loadProfile', 'logout']),
        openUserModal() {
            this.showUserModal = true
        },
        closeUserModal() {
            this.showUserModal = false
        }
    },
    created() {
        if (this.isAuthenticated) {
            this.loadProfile()
        }
    }
}
</script>

<style scoped>
#app {
  display: flex;
  flex-flow: column;
  align-items: center;
  background-image: url(@/assets/background.jpg);
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
}

nav {
    margin-top: 10px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px;
    background-color: #f3f4f5;
    border-radius: 10px;
    width: 75%;
    border: #1e5385 solid 1px;
}

.router-view {
    width: 75%;
    flex: 1;
    overflow: hidden;
}

.logo {
    height: 50px;
    cursor: pointer;
}

.user {
    margin-left: auto;
    width: 40px;
    height: 40px;
    background-color: #33a3ff;
    border-radius: 5px;
    padding: 5px;
    cursor: pointer;
    transition: all 0.3s;
    border: #1e5385 solid 1px;
}

.user:hover {
    background-color: #3283a8d8;
}


@media (max-width: 600px) {
    nav {
        margin: 0;
        width: 100%;
        border-radius: 0;
        margin-bottom: 10px;
    }
}
</style>