<template>
  <div class="color-picker" ref="colorPicker">
    <div class="color-picker__selected" :style="{ backgroundColor: selectedColor }" @click="toggleDropdown"></div>
    <div class="color-picker__dropdown" v-show="showDropdown">
      <div
        v-for="color in colors"
        :key="color.value"
        class="color-picker__option"
        :style="{ backgroundColor: color.hex, border: color.hex == selectedColor ? '2px solid red' : '1px solid #ccc' }"
        @click="selectColor(color.value)"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ColorPicker',
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showDropdown: false,
      colors: [
        { value: 'black',   'hex': '#000' },
        { value: 'gray',    'hex': '#ccc' },
        { value: 'dodgerblue', 'hex': '#6a5acd' },
        { value: 'orange',  'hex': '#ffa500' },
        { value: 'red',     'hex': '#dc143c' },
        { value: 'purple',  'hex': '#970096' },
        { value: 'white',   'hex': '#fff' },
        { value: 'cream',   'hex': '#f79f6f' },
        { value: 'lightskyblue', 'hex': '#87cefa'},
        { value: 'yellow',  'hex': '#fff75c' },
        { value: 'pink',    'hex': '#ff7a9e' },
        { value: 'green', 'hex': '#32cd32' },
      ],
    };
  },
  computed: {
    selectedColor() {
      return this.colors.find(c=>c.value == this.modelValue.replace('.PNG', '')).hex;
    },
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    selectColor(color) {
      this.$emit('update:modelValue', color+'.PNG');
      this.showDropdown = false;
    },
    closeDropdown(event) {
      if (!this.$refs.colorPicker.contains(event.target)) {
        this.showDropdown = false;
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdown);
  },
};
</script>

<style scoped>
.color-picker {
  position: relative;
  display: inline-block;
}

.color-picker__selected {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #ccc;
}

.color-picker__dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 10;
  background-color: white;
  border-radius: 4px;
  padding: 5px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-gap: 5px;
}

.color-picker__option {
  width: 24px;
  height: 24px;
  margin: 2px;
  border-radius: 4px;
  cursor: pointer;
  display: inline-block;
  border: 1px solid #ccc;
}
</style>