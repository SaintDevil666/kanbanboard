<template>
  <div class="tag-input">
    <div class="flex flex-wrap">
      <span v-for="tag in tags" :key="tag" class="tag">
        {{ tag }}
        <svg @click="removeTag(tag)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 cursor-pointer">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </span>
    </div>
    <input
      v-model="newTag"
      @keydown.enter="addTag"
      type="text"
      placeholder="Add a tag"
      class="border p-2 w-full"
    />
  </div>
</template>

<script>
export default {
  props: {
    modelValue: Array,
  },
  data() {
    return {
      newTag: '',
    };
  },
  computed: {
    tags: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
  methods: {
    addTag() {
      if (this.newTag.trim()) {
        this.tags.push(this.newTag.trim());
        this.newTag = '';
      }
    },
    removeTag(tag) {
      const index = this.tags.indexOf(tag);
      if (index !== -1) {
        this.tags.splice(index, 1);
      }
    },
  },
};
</script>

<style scoped>
.tag {
  @apply bg-gray-200 text-gray-800 rounded-full px-3 py-1 mr-2 mb-2 flex items-center;
}
</style>