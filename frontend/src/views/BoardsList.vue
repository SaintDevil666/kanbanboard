<template>
  <main>
    <div class="side">
      <VueDatePicker 
        class="date-picker"
        inline
        v-model="date"
        model-type="yyyy-MM-dd"
        @update:model-value="openBoardByDate"
        :highlight="highlightedDates"
        auto-apply
        :action-row="{'showSelect': false, 'showCancel': false}"
        :enable-time-picker="false"
        locale="uk-UA"/>
    </div>
    <div class="side right">
      <div class="search-bar">
        <div class="search-bar__input">
          <img src="@/assets/search.png" alt="" class="search-bar__icon">
          <input class="search-input" v-model="titleFilter" placeholder="Пошук за назвою" type="text" autofocus>
        </div>
        <div class="filters">
          <div class="filter">
            <Checkbox v-model="publicAccessFilter"/>
            <p class="filter__label">З публічним доступом</p>
          </div>
          <div class="filter">
            <Checkbox v-model="createdByMeFilter"/>
            <p class="filter__label">Створені мною</p>
          </div>
          <div class="filter filter--column">
            <p class="filter__label">За статусом</p>
            <select class="select" v-model="sortOption">
              <option value="updatedAt">Останнє оновлення</option>
              <option value="createdAt">Дата створення</option>
              <option value="title">Назва</option>
            </select>
          </div>
        </div>
      </div>
      <div class="boards">
        <div @click="createNewBoard" class="board add-board">
          <img src="@/assets/plus.svg" class="add-board__icon">
        </div>
        <div class="board basic shadow" v-for="board in filteredBoards" :key="board.id" @click="openBoard(board.id)">
          <p class="board__title">{{board.title}}</p>
          <div class="board__info-container">
            <div class="board__info">
              <div class="user">
                <img class="user__icon" src="@/assets/user.svg" alt="">
              </div>
              <p>{{board.creator.name}}</p>
            </div>
            <div class="board__info">
              <div class="user">
                <img class="user__icon" src="@/assets/clock.svg" alt="">
              </div>
              <p>{{formatDisplayDate(board.updatedAt)}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import Checkbox from '../components/Сheckbox.vue'
import moment from 'moment'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: 'BoardsList',
  components: {
    VueDatePicker,
    Checkbox
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
        .map(board => new Date(board.date));
    },
    filteredBoards() {
      let filtered = this.boards.filter(board => !board.date);
      if (this.titleFilter) {
        filtered = filtered.filter(board =>
          board.title.toLowerCase().includes(this.titleFilter.toLowerCase())
        )
      }
      if (this.publicAccessFilter) {
        filtered = filtered.filter(board => board.publicAccess);
      }
      if (this.createdByMeFilter) {
        filtered = filtered.filter(board => board.creator.id === this.user.id);
      }
      filtered.sort((a, b) => {
        if (this.sortOption === 'updatedAt') {
          return new Date(b.updatedAt) - new Date(a.updatedAt);
        } else if (this.sortOption === 'createdAt') {
          return new Date(b.createdAt) - new Date(a.createdAt);
        } else if (this.sortOption === 'title') {
          return a.title.localeCompare(b.title);
        }
      })
      return filtered;
    },
  },
  methods: {
    ...mapActions(['fetchBoards', 'fetchBoard', 'createBoard']),
    formatDisplayDate(date){
      return moment(date).format('HH:mm DD/MM');
    },
    formatBoardDate(date) {
      return moment(date).format('YYYY-MM-DD');
    },
    openBoardByDate(date) {
      const formattedDate = this.formatBoardDate(date);
      const board = this.boards.find(board => board.date === formattedDate);
      if (board) {
        this.$router.push(`/board/${board.id}`);
      } else {
        this.fetchBoard(formattedDate)
          .then(board => {
            this.$router.push(`/board/${board.id}`);
          });
      }
    },
    openBoard(id){
      this.$router.push(`/board/${id}`);
    },
    async createNewBoard(){
      const board = await this.createBoard({});
      if (board && board.id){
        this.$router.push(`/board/${board.id}`);
      }
    }
  },
  created() {
    this.fetchBoards();
  },
}
</script>
<style scoped>
  main {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 10px;
    height: 100%;
  }

  .side {
    display: flex;
    flex-flow: column;
    align-items: center;
    gap: 10px;
  }

  .right {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .boards {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto;
    gap: 10px;
    padding-bottom: 10px;
  }

  .date-picker {
    display: flex;
  }

  .search-bar {
    width: 100%;
    background-color: white;
    border-radius: 10px;
    border: rgb(172, 172, 172) solid 1px;
    display: flex;
    flex-direction: column;
    padding: 10px;
  }

  .search-bar__input {
    display: flex;
    align-items: center;
  }

  .search-bar__icon {
    height: 25px;
    margin-right: 10px;
  }

  .search-input {
    margin-bottom: 7px;
    width: 100%;
    border-bottom: 2px solid rgb(224, 222, 222);
    cursor: pointer;
    z-index: 10000;
  }

  .search-input:focus {
    outline: none;
  }

  .filters {
    margin-top: 30px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    row-gap: 10px;
    column-gap: 20px;
  }

  .filter {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .filter__label {
    margin-left: 10px;
  }

  .filter--column {
    flex-direction: column;
    width: 100%;
    align-items: start;
  }

  .select {
    z-index: 10000;
    border: black solid 1px;
    border-radius: 5px;
    height: 40px;
    width: 100%;
    cursor: pointer;
  }

  .boards::-webkit-scrollbar {
    width: 5px; /* Width of the scrollbar */
  }

  .boards::-webkit-scrollbar-track {
    background-color: #92c2f1c4; /* Color of the track */
  }

  .boards::-webkit-scrollbar-thumb {
    background-color: #007bff; /* Color of the thumb */
    border-radius: 10px; /* Roundness of the thumb */
    border: 3px solid #f1f1f1; /* Padding around thumb */
  }

  .board {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: calc(25% - 10px);
    box-sizing: border-box;
    height: 200px;
    border-radius: 10px;
    padding: 20px;
    background-color: white;
  }

  .shadow {
    filter: drop-shadow(grey 2px 2px 2px);
    transition: 0.3s;
  }
  .shadow:hover {
    filter: drop-shadow(grey 4px 4px 4px);
  }

  .add-board {
    background-color: rgba(51, 163, 255, 0.16);
    transition: all 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    z-index: 1;
  }

  .add-board::after {
    border-radius: 10px;
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.2);
    opacity: 0;
    transition: opacity 0.3s;
    z-index: -1;
  }

  .add-board:hover::after {
    opacity: 1;
  }

  .add-board__icon {
    height: 60px;
    margin: 0;
    padding: 0;
    color: white;
    transition: all 1.5s;
  }

  .add-board:hover .add-board__icon {
    transform: rotate(180deg);
    transition: 1.5s;
  }

  .board__title {
    font-weight: 600;
    font-size: 20px;
    text-align: center;
    padding-top: 10px;
  }
  .board__info-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  .board__info {
    display: flex;
    align-items: center;
    gap: 10px;
    word-wrap: break-word;
    word-break: break-word;
    overflow-wrap: break-word;
  }

  .user {
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    background-color: #33a3ff;
    border-radius: 5px;
    padding: 5px;
    cursor: pointer;
    transition: all 0.3s;
    border: #1e5385 solid 1px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .user__icon {
    height: 20px;
    width: 20px;
  }

  @media (max-width: 800px) {
    main {
      flex-direction: column;
    }
    .side {
      width: 100%;
    }
    .date-picker {
      margin: 0;
    }
    .board {
      width: 100%;
    }
    .right {
      width: 100%;
    }
  }
</style>