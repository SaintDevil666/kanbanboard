<template>
    <button @click="showAddModal = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
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
                @open-details="openCardEdit"
                @update-status-color="updateStatusColor"
            />
        </div>

        <AddCardModal
            :show="showAddModal"
            @update:show="showAddModal = false"
            @add-card="addNewCard"
        />

        <EditCardModal
            :show="showEditModal"
            :card="selectedCard"
            @close="closeCardEdit"
            @delete-card="handleDelete"
            @update-card="updateCard"
        />
    </div>
</template>

<script>
import { mapActions } from 'vuex'

import KanbanColumn from './KanbanColumn.vue';
import AddCardModal from './AddCardModal.vue';
import EditCardModal from './EditCardModal.vue';

export default {
    components: {
        KanbanColumn,
        AddCardModal,
        EditCardModal,
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
            showAddModal: false,
            showEditModal: false,
            selectedCard: null,
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
        addNewCard(card) {
            const newCard = {
                id: Date.now(),
                ...card,
                status: this.statuses[0].name,
                order: this.filteredCards(this.statuses[0].name).length,
                attachments: [],
            };
            this.addCardToBoard({ boardId: this.boardId, card: newCard });
            this.showAddModal = false;
        },
        openCardEdit(card) {
            this.selectedCard = card;
            this.showEditModal = true;
        },
        closeCardEdit() {
            this.selectedCard = null;
            this.showEditModal = false;
        },
        async handleDelete(cardId) {
            const index = this.cards.findIndex((card) => card.id === cardId);
            if (index !== -1) {
                const deletedCard = this.cards[index];
                this.deleteCardFromBoard({ boardId: this.boardId, card: deletedCard });
                this.updateCardOrders(deletedCard.status);
                this.showEditModal = false;
                this.selectedCard = null;
            }
        },
        async updateCard(updatedCard) {
            this.updateCardOnBoard({ boardId: this.boardId, card: updatedCard});
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