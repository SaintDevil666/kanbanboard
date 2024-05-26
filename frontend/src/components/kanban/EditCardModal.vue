<template>
    <div v-if="show" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
        <div class="bg-white rounded-lg p-5 m-4 max-w-2xl max-h-full overflow-y-auto relative">
            <svg @click="close" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 absolute top-2 right-2 cursor-pointer">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>

            <div class="mt-8">
                <h3 class="text-lg font-semibold mb-2">
                    <input v-model="updatedCard.title" type="text" class="border p-2 w-full">
                </h3>
                <textarea v-model="updatedCard.description" class="border p-2 w-full mb-4" rows="3"></textarea>
                
                <div class="mb-4">
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
                            v-for="(tag, index) in updatedCard.tags"
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
                    <label class="block mb-1">Прикріплені файли:</label>
                    <ul>
                        <li v-for="(attachment, index) in updatedCard.attachments" :key="index" class="mb-2 flex items-center">
                            <a @click="downloadAttachment(attachment.fileID, attachment.filename)" class="text-blue-500 hover:underline cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 mr-1 inline-block">
                                    <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
                                </svg>
                                {{ attachment.filename }}
                            </a>
                            <svg @click="deleteAttachment(attachment.fileID)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 ml-2 cursor-pointer text-red-500 hover:text-red-700">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                            </svg>
                        </li>
                    </ul>
                    <input type="file" @change="handleFileUpload" multiple class="mt-2">
                </div>

            <button @click="deleteCard(card.id)" class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Видалити картку
            </button>
        </div>
    </div>
</div>
</template>

<script>
import { uploadFile, downloadFile } from '@/utils/api';
import { mapActions } from 'vuex';
export default {
    props: {
        show: Boolean,
        card: Object
    },
    data() {
        return {
            newTag: ''
        };
    },
    computed: {
        updatedCard(){
            return Object.assign({}, this.card);
        }
    },
    methods: {
        ...mapActions(['updateCardOnBoard', 'deleteCardFromBoard']),
        deleteCard(cardId) {
            this.$emit('delete-card', cardId);
        },
        emitUpdate(){
            this.$emit('update-card', this.updatedCard);
        },
        close() {
            this.emitUpdate();
            this.$emit('close');
        },
        downloadFile(file) {
            // Додайте логіку завантаження файлу тут
            const url = URL.createObjectURL(file);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', file.name);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        },
        async deleteAttachment(fileId) {
            await this.deleteFileFromCard({
                boardId: this.boardId,
                cardId: this.card.id,
                fileId: fileId,
            });
        },
        async handleFileUpload(event) {
            const files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                await this.uploadFileToCard({
                    boardId: this.boardId,
                    cardId: this.card.id,
                    file: file,
                });
            }
        },
        async downloadAttachment(fileID, filename) {
            const response = await downloadFile(fileID)
            if (response.ok) {
                console.log(response);
                const blob = await response.blob()
                const url = URL.createObjectURL(blob)
                const link = document.createElement('a')
                link.href = url
                link.download = filename // Встановіть бажане ім'я файлу
                link.click()
                URL.revokeObjectURL(url)
            } else {
                console.error('File download failed')
            }
        },
        addTag() {
            if (this.newTag.trim()) {
                this.updatedCard.tags.push(this.newTag.trim());
                this.emitUpdate();
                this.newTag = '';
            }
        },
        removeTag(index) {
            this.updatedCard.tags.splice(index, 1);
            this.emitUpdate();
        }
    },
};
</script>