<template>
    <div class="kanban-board">
        <div class="columns">
            <KanbanColumn
                class="column"
                v-for="status in statuses"
                :boardId="boardId"
                :key="status.name"
                :status="status"
                :cards="filteredCards(status.name)"
                @add-card="addNewCard(status.name)"
                @move-card="moveCard"
                @reorder-card="reorderCard"
                @open-details="openCardEdit"
                @update-status="updateStatus"
                @delete-status="deleteStatus"
            />
        </div>

        <EditCardModal
            v-if="showEditModal"
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
import EditCardModal from './EditCardModal.vue';

export default {
    components: {
        KanbanColumn,
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
        ...mapActions(['addCardToBoard', 'updateCardOnBoard', 'deleteCardFromBoard', 'updateBoardStatus', 'deleteBoardStatus']),
        filteredCards(statusName) {
            return this.cards
                .filter((card) => card.status === statusName)
                .sort((a, b) => a.order - b.order);
        },
        async moveCard(cardId, newStatus) {
          const card = this.cards.find((card) => card.id === cardId);
          if (card) {
            const oldStatus = card.status;
            const oldOrder = card.order;
            
            // Видалення картки з попереднього статусу
            this.cards = this.cards.filter((card) => card.id !== cardId);
            
            // Додавання картки в новий статус з оновленим order
            card.status = newStatus;
            card.order = this.getMaxOrder(newStatus) + 1;
            this.cards.push(card);
            
            // Оновлення order карток в попередньому статусі
            this.updateCardOrders(oldStatus, oldOrder);
            
            // Збереження змін в бекенді
            await this.updateCardOnBoard({ boardId: this.boardId, card: card });
          }
        },

        getMaxOrder(status) {
          const cards = this.cards.filter((card) => card.status === status);
          return cards.length > 0 ? Math.max(...cards.map((card) => card.order)) : 0;
        },

        updateCardOrders(status, removedOrder) {
          this.cards
            .filter((card) => card.status === status && card.order > removedOrder)
            .forEach((card) => card.order--);
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
        async addNewCard(status) {
            const response = await this.addCardToBoard({ boardId: this.boardId, status: status });
            if (response && response.cardId) {
                this.openCardEdit({ id: response.cardId });
            }
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
        updateStatus(data) {
          this.updateBoardStatus({
            boardId: this.boardId,
            statusName: data.statusName,
            toStatusName: data.toStatusName,
            toStatusColor: data.toStatusColor
          });
        },
        deleteStatus(statusName) {
          this.deleteBoardStatus({
            boardId: this.boardId,
            statusName: statusName
          });
        }
    },
};
</script>

<style scoped>
    .kanban-board {
        width: 100%;
        background-color: transparent !important;
    }

    .columns {
        display: flex;
        height: 70svh;
        justify-content: space-around;
        width: 100%;
    }
    .columns::-webkit-scrollbar {
        width: 5px; /* Width of the scrollbar */
    }
    .columns::-webkit-scrollbar-track {
        background-color: #92c2f1c4; /* Color of the track */
    }
    .columns::-webkit-scrollbar-thumb {
        background-color: #007bff; /* Color of the thumb */
        border-radius: 10px; /* Roundness of the thumb */
        border: 3px solid #f1f1f1; /* Padding around thumb */
    }
    .column {
        width: 100%;
    }
    @media (max-width: 800px) {
        .kanban-board {
            width: 100%;
        }
    }
</style>