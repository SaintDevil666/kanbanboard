<template>
  <div
    class="kanban-card bg-gray-100 rounded shadow p-3 mb-2 flex flex-col cursor-pointer"
    @click="$emit('open-details', card)"
  >
    <div>{{ card.title }}</div>
    <div class="mt-2 flex flex-wrap">
      <span
        v-for="(tag, index) in card.tags"
        :key="index"
        class="inline-block bg-gray-300 rounded-full px-2 py-1 text-xs font-semibold text-gray-700 mr-2 mb-2"
      >
        {{ tag }}
      </span>
    </div>
    <div class="mt-2 flex items-center">
      <svg v-if="card.description" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 mr-1">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
      </svg>
      <div v-if="card.attachments.length" class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 mr-1">
          <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
        </svg>
        <span v-if="card.attachments.length > 1" class="text-xs">{{ card.attachments.length }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    card: Object,
  },
  methods: {
    onDragStart(event) {
      event.dataTransfer.setData('cardId', this.card.id.toString());
    },
    emitOpenDetails() {
      this.$emit('open-details', this.card);
    },
  },
};
</script>