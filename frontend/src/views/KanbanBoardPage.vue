<template>
  <div class="kanban-board">
    <div class="board-header" v-if="board">
      <router-link to="/" class="back-link">&lt; Повернутися до дошок</router-link>
      <h2>{{ board.title }}</h2>
      <button @click="editTitle" class="button">Змінити назву</button>
      <p>{{ board.description }}</p>
      <button @click="editDescription" class="button">Змінити опис</button>
      <button v-if="isCreator" @click="openAccessModal" class="access">Надати доступ</button>
    </div>
    <KanbanBoard v-if="board.statuses" :boardId="board.id" :statuses="board.statuses" :cards="board.cards"/>
    <access-modal v-if="showAccessModal" :board="board" @close="closeAccessModal"></access-modal>
  </div>
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
    ...mapActions(['fetchBoard', 'updateBoard']),
    async editTitle() {
      const newTitle = prompt('Enter new title', this.board.title)
      if (newTitle) {
        await this.updateBoard({ id: this.board.id, title: newTitle, description: this.board.description })
      }
    },
    async editDescription() {
      const newDescription = prompt('Enter new description', this.board.description)
      if (newDescription) {
        await this.updateBoard({ id: this.board.id, title: this.board.title, description: newDescription })
      }
    },
    openAccessModal() {
      this.showAccessModal = true
    },
    closeAccessModal() {
      this.showAccessModal = false
    },
    // async onDragStart(args) {
    //   args.cancel = !this.isCreator
    // },
    // async onDragStop(args) {
    //   if (args.data instanceof Array && args.data.length > 0) {
    //     const cardIds = args.data.map(card => card.id)
    //     const status = args.target.closest('.e-card')?.dataset.status
    //     if (status) {
    //       await apiPATCH(`/boards/${this.board.id}/cards`, {
    //         action: 'batch',
    //         changed: cardIds.map(id => ({ id, status }))
    //       })
    //     }
    //   }
    // },
  },
  async mounted(){
    await this.fetchBoard(this.$route.params.id)
  }
}
</script>

<style scoped>
.kanban-board {
  padding: 20px;
}

.board-header {
  margin-bottom: 20px;
}

.back-link {
  display: inline-block;
  margin-bottom: 10px;
}

#kanban {
  height: 500px;
}

.header-template {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-text {
  font-weight: bold;
}

.card-template {
  padding: 10px;
}

.card-title {
  font-weight: bold;
}

.card-tags {
  margin-top: 5px;
}

.card-tag {
  background-color: #f0f0f0;
  padding: 2px 5px;
  border-radius: 4px;
  margin-right: 5px;
}

.dialog-template {
  padding: 20px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 5px;
}

.attachments {
  margin-bottom: 10px;
}

.attachment {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.attachment span {
  margin-right: 10px;
}
button{
  padding: 8px 12px;
  margin:5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}
.access{
  background-color: lightskyblue;
}
</style>
<style>
.kanban-overview.e-kanban .header-template-wrap {
  display: inline-flex;
  font-size: 15px;
  font-weight: 500;
}

.kanban-overview.e-kanban .header-template-wrap .header-icon {
  font-family: "Kanban priority icons";
  margin-top: 3px;
  width: 10%;
}

.kanban-overview.e-kanban .header-template-wrap .header-text {
  margin-left: 15px;
}

.kanban-overview.e-kanban.e-rtl .header-template-wrap .header-text {
  margin-right: 15px;
}

.kanban-overview.e-kanban.e-rtl .e-card-avatar {
  left: 12px;
  right: auto;
}

.kanban-overview.e-kanban .e-card-avatar {
  width: 30px;
  height: 30px;
  text-align: center;
  background-color: gainsboro;
  color: #6b6b6b;
  border-radius: 50%;
  position: absolute;
  right: 12px;
  bottom: 10px;
  font-size: 12px;
  font-weight: 400;
  padding: 10px 0px 0px 1px;
}

.kanban-overview.e-kanban .Open::before {
  content: "\e700";
  color: #0251cc;
  font-size: 16px;
}

.kanban-overview.e-kanban .InProgress::before {
  content: "\e703";
  color: #ea9713;
  font-size: 16px;
}

.kanban-overview.e-kanban .e-image img {
  background: #ececec;
  border: 1px solid #c8c8c8;
  border-radius: 50%;
}

.kanban-overview.e-kanban .Review::before {
  content: "\e701";
  color: #8e4399;
  font-size: 16px;
}

.kanban-overview.e-kanban .Close::before {
  content: "\e702";
  color: #63ba3c;
  font-size: 16px;
}

.kanban-overview.e-kanban .e-card .e-card-tag-field {
  background: #ececec;
  color: #6b6b6b;
  margin-right: 5px;
  line-height: 1.1;
  font-size: 13px;
  border-radius: 3px;
  padding: 4px;
}

.kanban-overview.e-kanban .e-card-custom-footer {
  display: flex;
  padding: 0px 12px 12px;
  line-height: 1;
  height: 35px;
}

.kanban-overview.e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Low,
.kanban-overview.e-kanban.e-rtl
  .e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Low {
  border-left: 3px solid #ffd600;
}

.kanban-overview.e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.High,
.kanban-overview.e-kanban.e-rtl
  .e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.High {
  border-left: 3px solid #990099;
}

.kanban-overview.e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Normal,
.kanban-overview.e-kanban.e-rtl
  .e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Normal {
  border-left: 3px solid #66cc33;
}

.kanban-overview.e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Critical,
.kanban-overview.e-kanban.e-rtl
  .e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card.Critical {
  border-left: 3px solid #cc0000;
}

.kanban-overview.e-kanban.e-rtl
  .e-kanban
  .e-kanban-content
  .e-content-row
  .e-content-cells
  .e-card-wrapper
  .e-card {
  border-left: none;
}

[class^="sf-icon-"],
[class*=" sf-icon-"] {
  speak: none;
  font-size: 55px;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>