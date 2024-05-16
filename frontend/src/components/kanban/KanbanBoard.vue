<template>
    <button @click="showModal = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Додати нову картку
    </button>
    <div class="kanban-board">
        <div class="flex justify-around p-5 bg-gray-100 min-h-screen">
            <KanbanColumn
                v-for="status in statuses"
                :key="status.name"
                :status="status"
                :cards="filteredCards(status.name)"
                @move-card="moveCard"
                @reorder-card="reorderCard"
                @open-details="showTaskDetails"
                @update-status-color="updateStatusColor"
            />
        </div>

        <TaskModal
            :show="showModal"
            @update:show="showModal = false"
            @add-task="addNewTask"
        />

        <TaskDetailsModal
            :show="showTaskModal"
            :task="selectedTask"
            @close="closeTaskDetails"
            @delete-task="handleDelete"
            @update-task="updateTask"
        />
    </div>
</template>

<script>
import { mapActions } from 'vuex'

import KanbanColumn from './KanbanColumn.vue';
import TaskModal from './TaskModal.vue';
import TaskDetailsModal from './TaskDetailsModal.vue';

export default {
    components: {
        KanbanColumn,
        TaskModal,
        TaskDetailsModal,
    },
    props: {
        boardId: {
            type: String,
            required: true
        },
        statuses: {
            type: Array,
            required: true,
        },
        cards: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            showModal: false,
            showTaskModal: false,
            selectedTask: null,
        };
    },
    methods: {
        ...mapActions(['addCardToBoard', 'updateCardOnBoard', 'deleteCardFromBoard']),
        filteredCards(statusName) {
            return this.cards
                .filter((card) => card.status === statusName)
                .sort((a, b) => a.order - b.order);
        },
        moveCard(cardId, newStatus) {
            let card = this.cards.find((card) => card.id === cardId);
            if (card){
                const oldStatus = card.status;
                card.status = newStatus;
                this.updateCardOnBoard({ boardId: this.boardId, card: card });
                if (card) {
                    card.status = newStatus;
                    card.order = this.filteredCards(newStatus).length;
                    this.updateCardOrders(oldStatus);
                    this.updateCardOrders(newStatus);
                }
            }
        },
        reorderCard(cardId, newOrder) {
            const card = this.cards.find((card) => card.id === cardId);
            if (card) {
                const oldOrder = card.order;
                card.order = newOrder;
                this.updateCardOrders(card.status, oldOrder, newOrder);
            }
        },
        updateCardOrders(status, oldOrder = null, newOrder = null) {
            const cards = this.filteredCards(status);
            cards.forEach((card, index) => {
                if (oldOrder !== null && newOrder !== null) {
                    if (card.order > oldOrder && card.order <= newOrder) {
                        card.order--;
                    } else if (card.order < oldOrder && card.order >= newOrder) {
                        card.order++;
                    }
                }
                card.order = index;
            });
        },
        addNewTask(task) {
            const newTask = {
                id: Date.now(),
                ...task,
                status: this.statuses[0].name,
                order: this.filteredCards(this.statuses[0].name).length,
                attachments: [],
            };
            this.addCardToBoard({ boardId: this.boardId, card: newTask });
            this.showModal = false;
        },
        showTaskDetails(task) {
            this.selectedTask = task;
            this.showTaskModal = true;
        },
        closeTaskDetails() {
            this.selectedTask = null;
            this.showTaskModal = false;
        },
        async handleDelete(taskId) {
            const index = this.cards.findIndex((card) => card.id === taskId);
            if (index !== -1) {
                const deletedTask = this.cards[index];
                this.deleteCardFromBoard({ boardId: this.boardId, card: deletedTask });
                this.updateCardOrders(deletedTask.status);
                this.showTaskModal = false;
                this.selectedTask = null;
            }
        },
        async updateTask(updatedTask) {
            this.updateCardOnBoard({ boardId: this.boardId, card: updatedTask});
        },
        updateStatusColor(statusName, newColor) {
            const status = this.statuses.find((status) => status.name === statusName);
            if (status) {
                const oldColor = status.color;
                status.color = newColor;
            }
        }
    },
};
</script>