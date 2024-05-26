<template>
    <div v-if="show" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
        <div class="bg-white p-5 rounded-lg shadow-lg relative">
            <svg @click="closeModal" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 absolute top-2 right-2 cursor-pointer">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>

            <h2 class="text-lg font-bold mb-4">Нова картка</h2>
            
            <input
                v-model="card.title"
                type="text"
                placeholder="Назва картки"
                class="border p-2 w-full mb-2"
            />

            <textarea
                v-model="card.description"
                placeholder="Опис картки"
                class="border p-2 w-full mb-2"
                rows="3"
            ></textarea>

            <div class="mb-2">
                <label class="block mb-1">Теги:</label>
                <div class="flex items-center">
                    <input
                        v-model="newTag"
                        @keydown.enter="addTag"
                        type="text"
                        placeholder="Додайте новий тег"
                        class="border p-2 w-full"
                    />
                    <button
                        @click="addTag"
                        class="ml-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                        +
                    </button>
                </div>
                <div class="mt-2">
                    <span
                        v-for="(tag, index) in card.tags"
                        :key="index"
                        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
                    >
                        {{ tag }}
                        <svg
                            @click="removeTag(index)"
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-4 w-4 inline-block ml-1 cursor-pointer"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </span>
                </div>
            </div>

            <div>
                <label class="block mb-1">Прикріпіть файли:</label>
                <input type="file" @change="handleFileUpload" multiple>
                <ul v-if="card.attachments.length > 0" class="mt-2">
                    <li v-for="(attachment, index) in card.attachments" :key="index" class="flex items-center mb-1">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 mr-1">
                            <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
                        </svg>
                        {{ attachment.filename }}
                        <svg @click="deleteAttachment(index)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-1 cursor-pointer text-red-500 hover:text-red-700">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                        </svg>
                    </li>
                </ul>
            </div>

            <button
                @click="addCard"
                class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Зберегти
            </button>
        </div>
    </div>
</template>

<script>
import { uploadFile, apiPATCH } from '@/utils/api';
export default {
    props: {
        show: Boolean
    },
    data() {
        return {
            card: {
                title: '',
                description: '',
                tags: [],
                attachments: []
            },
            newTag: ''
        };
    },
    methods: {
        async addCard() {
            if (this.card.title.trim()) {
                this.$emit('add-card', this.card)
                this.resetCard()
                this.$emit('update:show', false)
            }
        },
        resetCard() {
            this.card = {
                title: '',
                description: '',
                tags: [],
                attachments: []
            };
        },
        closeModal() {
            this.resetCard();
            this.$emit('update:show', false);
        },
        async handleFileUpload(event) {
            const files = event.target.files
            for (let i = 0; i < files.length; i++) {
                const file = files[i]
                const { status, json } = await uploadFile(file)
                if (status === 201) {
                    if (!this.card.attachments)
                        this.card.attachments = [];
                    this.card.attachments.push({
                        filename: file.name,
                        fileID: json.id,
                    })
                } else {
                    console.error('File upload failed')
                }
            }
        },
        deleteAttachment(index) {
            this.card.attachments.splice(index, 1)
        },
        addTag() {
            if (this.newTag.trim()) {
                this.card.tags.push(this.newTag.trim());
                this.newTag = '';
            }
        },
        removeTag(index) {
            this.card.tags.splice(index, 1);
        }
    }
};
</script>