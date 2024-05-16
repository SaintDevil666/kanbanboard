<template>
  <div class="kanban-column bg-white shadow rounded flex-1 mx-2" >
    <div class="header flex items-center justify-between p-4" :style="{ borderColor: status.color }">
      <h2 class="font-bold text-lg">{{ status.name }}</h2>
    </div>
    <div class="card-container p-4" :style="{ backgroundColor: getPastelColor(status.color) }">
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
    </div>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import KanbanCard from './KanbanCard.vue';

export default {
  components: {
    draggable,
    KanbanCard
  },
  props: {
    status: Object,
    cards: Array,
  },
  methods: {
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
    getPastelColor(color) {
      const opacity = 0.08;
      const r = parseInt(color.slice(1, 3), 16);
      const g = parseInt(color.slice(3, 5), 16);
      const b = parseInt(color.slice(5, 7), 16);
      const pastelColor = `rgba(${r}, ${g}, ${b}, ${opacity})`;
      return pastelColor;
    },
    updateStatusColor(newColor) {
      this.$emit('update-status-color', this.status.name, newColor);
    },
  },
};
</script>

<style scoped>
.header {
  border-top-left-radius: 0.25rem;
  border-top-right-radius: 0.25rem;
  border-top: 4px solid;
}

.kanban-column {
  display: flex;
  flex-direction: column;
}

.card-container {
  flex-grow: 1;
  overflow-y: auto;
}
</style>