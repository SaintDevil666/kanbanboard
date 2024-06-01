<template>
  <div :style="{ backgroundImage: 'url(/' + status.color + ')' }" class="kanban-column shadow rounded">
    <div class="kanban-column__header">
      <span contenteditable @input="updateStatusName" class="kanban-column__title">{{ statusName }}</span>
      <div class="kanban-column__actions">
        <ColorPicker v-model="statusColor" />
        <img @click="deleteStatus" src="@/assets/trash.svg" alt="Delete" class="kanban-column__delete-icon" />
      </div>
    </div>
    <div class="kanban-column__card-container">
      <draggable
        :list="cards"
        :group="{ name: 'cards', pull: true, put: true }"
        item-key="id"
        @change="onCardMoved"
      >
        <template #item="{ element }">
          <KanbanCard
            :card="element"
            @open-details="$emit('open-details', $event)"
          />
        </template>
      </draggable>
      <div @click="addCard" class="kanban-column__add-card">
        <img class="kanban-column__add-card-icon" src="@/assets/plus2.svg" alt="">
      </div>
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import KanbanCard from './KanbanCard.vue';
import ColorPicker from '../ColorPicker.vue';

export default {
  components: {
    draggable,
    KanbanCard,
    ColorPicker
  },
  props: {
    status: Object,
    cards: Array,
    boardId: {}
  },
  data() {
    return {
      statusName: this.status.name,
      statusColor: this.status.color,
      previousStatusName: this.status.name
    };
  },
  watch: {
    statusName(newName, oldName) {
      if (newName !== oldName) {
        this.updateStatus({
          statusName: oldName,
          toStatusName: newName,
          toStatusColor: null
        });
      }
    },
    statusColor(newColor, oldColor) {
      console.log(newColor, oldColor);
      if (newColor !== oldColor) {
        this.updateStatus({
          statusName: this.statusName,
          toStatusName: null,
          toStatusColor: newColor
        });
      }
    }
  },
  methods: {
    addCard() {
      this.$emit('add-card');
    },
    onCardMoved(event) {
      if (event.added) {
        const cardId = event.added.element.id;
        this.$emit('move-card', cardId, this.status.name);
      } else if (event.moved) {
        const cardId = event.moved.element.id;
        const newOrder = event.moved.newIndex;
        this.$emit('reorder-card', cardId, newOrder);
      }
    },
    updateStatusName(event) {
      this.statusName = event.target.innerText;
    },
    deleteStatus() {
      this.$emit('delete-status', this.statusName);
    },
    updateStatus(data) {
      this.$emit('update-status', data);
    }
  }
};
</script>
<style scoped>
.kanban-column {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin: 0 0.5rem;
  border-radius: 10px;
}

.kanban-column__header {
  margin-top: 10px;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  display: flex;
  justify-content: center;
  position: relative;
}

.kanban-column__title {
  margin: 0;
  text-align: center;
  font-weight: bold;
  font-size: 1.5rem;
  outline: none;
}

.kanban-column__actions {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
}

.kanban-column__delete-icon {
  width: 30px;
  height: 30px;
  cursor: pointer;
  margin-left: 10px;
}

.kanban-column__card-container {
  padding: 1rem;
  flex-grow: 1;
  overflow-y: auto;
}

.kanban-column__add-card {
  width: 100%;
  display: flex;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.5);
  padding: 5px;
  border-radius: 10px;
  cursor: pointer;
}

.kanban-column__add-card-icon {
  user-select: none;
  height: 15px;
}
</style>