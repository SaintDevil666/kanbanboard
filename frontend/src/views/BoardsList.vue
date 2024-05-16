<template>
  <div class="boards-list">
    <div class="calendar">
      <div/>
      <VueDatePicker inline v-model="date" model-type="yyyy-MM-dd" @update:model-value="openBoardByDate" :highlight="highlightedDates" auto-apply :action-row="{'showSelect': false, 'showCancel': false}" :enable-time-picker="false" locale="uk-UA"></VueDatePicker>
      <div/>
    </div>
    <div class="filters">
      <input type="text" v-model="titleFilter" placeholder="Filter by title">
      <label>
        <input type="checkbox" v-model="publicAccessFilter">
        З публічним доступом
      </label>
      <label>
        <input type="checkbox" v-model="createdByMeFilter">
        Створені мною
      </label>
      <select v-model="sortOption">
        <option value="updatedAt">Останнє оновлення</option>
        <option value="createdAt">Дата створення</option>
        <option value="title">Назва</option>
      </select>
    </div>
    <button @click="createNewBoard" class="button">Створити нову дошку</button>
    <div class="boards-grid">
        <div class="board-card" v-for="board in filteredBoards" :key="board.id" @click="openBoard(board.id)">
          <h3>Назва: <b>{{ board.title?board.title:"Без назви" }}</b></h3>
          <p>Власник: {{ board.creator.name }}</p>
          <p>Останнє оновлення: {{ formatDate(board.updatedAt) }}</p>
        </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import moment from 'moment'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: 'BoardsList',
  components: {
    VueDatePicker,
  },
  data() {
    return {
      date: null,
      selectedDate: null,
      titleFilter: '',
      publicAccessFilter: false,
      createdByMeFilter: false,
      sortOption: 'updatedAt',
    }
  },
  computed: {
    ...mapGetters(['boards', 'user']),
    highlightedDates() {
      return this.boards
        .filter(board => board.date)
        .map(board => new Date(board.date))
    },
    filteredBoards() {
      let filtered = this.boards.filter(board => !board.date)
      if (this.titleFilter) {
        filtered = filtered.filter(board =>
          board.title.toLowerCase().includes(this.titleFilter.toLowerCase())
        )
      }
      if (this.publicAccessFilter) {
        filtered = filtered.filter(board => board.publicAccess)
      }
      if (this.createdByMeFilter) {
        filtered = filtered.filter(board => board.creator.id === this.user.id)
      }
      filtered.sort((a, b) => {
        if (this.sortOption === 'updatedAt') {
          return new Date(b.updatedAt) - new Date(a.updatedAt)
        } else if (this.sortOption === 'createdAt') {
          return new Date(b.createdAt) - new Date(a.createdAt)
        } else if (this.sortOption === 'title') {
          return a.title.localeCompare(b.title)
        }
      })
      return filtered
    },
  },
  methods: {
    ...mapActions(['fetchBoards', 'fetchBoard', 'createBoard']),
    formatDate(date) {
      return moment(date).format('YYYY-MM-DD')
    },
    openBoardByDate(date) {
      const formattedDate = this.formatDate(date)
      const board = this.boards.find(board => board.date === formattedDate)
      if (board) {
        this.$router.push(`/board/${board.id}`)
      } else {
        this.fetchBoard(formattedDate)
          .then(board => {
            this.$router.push(`/board/${board.id}`)
          })
          .catch(() => {
            // Handle error if board not found
          })
      }
    },
    openBoard(id){
      this.$router.push(`/board/${id}`);
    },
    async createNewBoard(){
      const board = await this.createBoard({});
      if (board && board.id){
        this.$router.push(`/board/${board.id}`)
      }
    }
  },
  created() {
    this.fetchBoards()
  },
}
</script>
<style scoped>
.boards-list {
  padding: 20px;
}

.calendar {
/*  margin-bottom: 20px;*/
  display: grid;
  grid-template-columns: 39% 22% 39%;
}

.boards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-gap: 20px;
}

.board-card {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  background-color: lightskyblue;
  cursor: pointer;
}

.filters {
  margin-top: 20px;
}

.filters input,
.filters select {
  margin-right: 10px;
}

.button{
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin:10px 0px;
}
</style>