<template>
  <main>
    <header class="board-header">
      <div class="board-header__top">
        <img @click="toMain" class="board-header__back-icon" src="@/assets/back.svg" alt="">
        <input @input="editBoard" v-model="board.title" type="text" placeholder="Назва" class="board-header__title-input">
        <img v-if="isCreator" @click="openAccessModal" class="board-header__share-icon" src="@/assets/share.svg" alt="">
      </div>
      <input @input="editBoard" v-model="board.description" placeholder="Опис" type="text" class="board-header__description-input">
    </header>
    <KanbanBoard v-if="board.statuses" :boardId="board.id" :statuses="board.statuses" :cards="board.cards"/>
    <access-modal v-if="showAccessModal" :board="board" @close="closeAccessModal"/>
  </main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import AccessModal from '@/components/AccessModal.vue'
import { apiPATCH } from '@/utils/api'
import KanbanBoard from '@/components/kanban/KanbanBoard.vue'

export default {
  name: 'KanbanBoardPage',
  components: {
    KanbanBoard,
    AccessModal
  },
  data() {
    return {
      showAccessModal: false,
      kanban: null
    }
  },
  computed: {
    ...mapGetters(['board', 'user']),
    isCreator() {
      return this.board?.creator?.id === this.user?.id
    }
  },
  methods: {
    toMain() {
      location.replace('/')
    },
    ...mapActions(['fetchBoard', 'updateBoard']),
    editBoard() {
      this.updateBoard({ id: this.board.id, title: this.board.title, description: this.board.description })
    },
    openAccessModal() {
      this.showAccessModal = true
    },
    closeAccessModal() {
      this.showAccessModal = false
    },
  },
  async mounted(){
    await this.fetchBoard(this.$route.params.id)
  }
}
</script>
<style scoped>
  main {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .board-header {
    margin-bottom: 30px;
    width: 100%;
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 10px;
    border: rgb(156, 156, 156) solid 1px;
    padding: 10px;
    justify-content: center;
    align-items: center;
  }

  .board-header__top {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .board-header__back-icon,
  .board-header__share-icon {
    width: 30px;
    cursor: pointer;
  }

  .board-header__title-input {
    font-size: 20px;
    border-bottom: 2px solid rgb(224, 222, 222);
    text-align: center;
  }

  .board-header__description-input {
    font-size: 15px;
    margin-top: 20px;
    width: 50%;
    border-bottom: 2px solid rgb(224, 222, 222);
    text-align: center;
  }

  .board-header__title-input:focus,
  .board-header__description-input:focus {
    outline: none;
  }

  @media (max-width: 800px) {
    .board-header {
      width: 100%;
      border-radius: 0;
    }
  }
</style>
