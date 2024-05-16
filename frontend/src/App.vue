<template>
    <div id="app">
        <header>
            <div class="logo-container">
                <div class="logo"><i>kanbanboard.click</i></div>
            </div>
            <div class="user-icon" v-if="isAuthenticated" @click="openUserModal">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="user-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
            </div>
        </header>
        <router-view></router-view>
        <user-modal v-if="showUserModal" @close="closeUserModal"></user-modal>
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
header {
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f0f0f0;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    margin: 10px;
}

.user-icon {
    cursor: pointer;
    width:60px;
    height: 60px;
}
</style>