import { createStore } from 'vuex'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { apiGET, apiPOST, apiPATCH, apiDELETE } from '@/utils/api'

const store = createStore({
    state: {
        token: getToken(),
        user: null,
        boards: [],
        board: {},
        boardCreated: false,
        user: null
    },
    mutations: {
        SET_TOKEN(state, token) {
            state.token = token
            setToken(token)
        },
        SET_USER(state, user) {
            if (user)
            state.user = user
        },
        CLEAR_USER(state) {
            state.user = null
            removeToken()
        },
        SET_BOARDS(state, boards) {
            state.boards = boards
        },
        ADD_BOARD(state, board) {
            state.boards.push(board)
        },
        SET_BOARD(state, board) {
            state.board = board
        },
        UPDATE_BOARD(state, { id, title, description }) {
            if (state.board.id === id) {
                state.board.title = title
                state.board.description = description
            }
        },
        UPDATE_BOARD_ACCESS(state, { boardId, publicAccess }) {
            if (state.board.id === boardId) {
                state.board.publicAccess = publicAccess
            }
        },
        ADD_BOARD_USER(state, { boardId, user }) {
            if (state.board.id === boardId) {
                state.board.invited.push(user)
            }
        },
        REMOVE_BOARD_USER(state, { boardId, userId }) {
            if (state.board.id === boardId) {
                const index = state.board.invited.findIndex(user => user.id === userId)
                if (index !== -1) {
                    state.board.invited.splice(index, 1)
                }
            }
        },
        ADD_CARD(state, { boardId, card }){
            if (state.board.id === boardId) {
                card['attachments'] = [];
                state.board.cards.push(card);
            }
        },
        UPDATE_CARD(state, { boardId, card }){
            if (state.board.id === boardId) {
                let i = state.board.cards.findIndex(c => c.id == card.id);
                state.board.cards[i] = Object.assign(state.board.cards[i], card);
            }
        },
        DELETE_CARD(state, { boardId, card }){
            state.board.cards = state.board.cards.filter(c => c.id != card.id);
        },
        ADD_FILE_TO_CARD(state, { boardId, cardId, file }) {
            const card = state.board.cards.find(c => c.id === cardId);
            if (card) {
                console.log(card);
                if (card.attachments)
                    card.attachments.push(file);
                else
                    card.attachments = [file];
            }
        },
        REMOVE_FILE_FROM_CARD(state, { boardId, cardId, fileId }) {
            const card = state.board.cards.find(c => c.id === cardId);
            if (card) {
                card.attachments = card.attachments.filter(file => file.fileID !== fileId);
            }
        },
        UPDATE_STATUS(state, { statusName, toStatusName, toStatusColor }) {
            const status = state.board.statuses.find(status => status.name === statusName);
            if (status) {
              if (toStatusName) {
                status.name = toStatusName;
              }
              if (toStatusColor) {
                status.color = toStatusColor;
              }
            }
        },
        DELETE_STATUS(state, statusName) {
            state.board.statuses = state.board.statuses.filter(status => status.name !== statusName);
        }
    },
    actions: {
        async login({ commit }, { email, password }) {
            const response = await apiPOST('/login', { email, password });
            if (response.status === 200 && response.json.token) {
                commit('SET_TOKEN', response.json.token);
            }
            return response;
        },
        async register({ commit }, { name, email, password }) {
            const response = await apiPOST('/register', { name, email, password });
            if (response.status === 201) {
                commit('SET_TOKEN', response.json.token);
            }
            return response;
        },
        async loadProfile({ commit }) {
            const response = await apiGET('/profile');
            if (response.status === 200) {
                commit('SET_USER', response.json);
            } else if (response.status == 401){
                commit('CLEAR_USER');
            }
            return response;
        },
        async logout({ commit }) {
            await apiPOST('/logout')
            commit('CLEAR_USER')
        },
        async updateUserProfile({ commit, state }, { name, email, currentPassword, newPassword, settings }){
            let update = {};
            if (name)
                update.name = name;
            if (email)
                update.email = email;
            if (currentPassword && newPassword){
                update.currentPassword = currentPassword;
                update.newPassword = newPassword;
            }
            if (settings)
                update.settings = settings;

            console.log(JSON.stringify(update, null, 2));

            const response = await apiPATCH('/profile', update)
            if (response.status == 200){
                let upd_user = state.user;
                if (update.name)
                    upd_user.name = update.name;
                if (update.email)
                    upd_user.email = update.email;
                if (update.settings)
                    upd_user.settings = update.settings;
                commit('SET_USER', upd_user);
            }
            return response.json;
        },
        async fetchBoards({ commit }) {
            const response = await apiGET('/boards')
            if (response.status === 200) {
                commit('SET_BOARDS', response.json)
            }
        },
        async fetchBoard({ commit }, boardId) {
            const response = await apiGET(`/boards/${boardId}`)
            if (response.status === 200) {
                commit('SET_BOARD', response.json)
                return response.json
            } else if (response.status === 201) {
                commit('ADD_BOARD', response.json)
                commit('SET_BOARD', response.json)
                return response.json
            }
        },
        async createBoard({ commit }, { title, description, statuses}) {
            const response = await apiPOST(`/boards`, {});
            if (response.status === 201){
                return response.json;
            }
        },
        async updateBoard({ commit }, { id, title, description }) {
            const response = await apiPATCH(`/boards/${id}/info`, { title, description })
            if (response.status === 200) {
                commit('UPDATE_BOARD', { id, title, description })
            }
        },
        async updateBoardPublicAccess({ commit }, { boardId, publicAccess }) {
            const response = await apiPATCH(`/boards/${boardId}/publicAccess`, { access: publicAccess })
            if (response.status === 200) {
                commit('UPDATE_BOARD_ACCESS', { boardId, publicAccess })
            }
        },
        async inviteUserToBoard({ commit }, { boardId, email }) {
            const response = await apiPOST(`/boards/${boardId}/invite`, { email })
            if (response.status === 200) {
                commit('ADD_BOARD_USER', { boardId, user: response.json })
            }
        },
        async removeUserFromBoard({ commit }, { boardId, userId }) {
            const response = await apiDELETE(`/boards/${boardId}/invite`, { id: userId });
            if (response.status === 200) {
                commit('REMOVE_BOARD_USER', { boardId, userId });
            }
        },
        async addCardToBoard({ commit }, { boardId, status }){
            let card = { 'status': status, 'title': '', 'description': '', 'tags': [] }
            const response = await apiPATCH(`/boards/${boardId}/cards`, { 'action': 'add', 'card': card });
            if (response.status == 200){
                card['id'] = response.json.cardId;
                commit('ADD_CARD', { boardId, card });
                return response.json;
            }
        },
        async updateCardOnBoard({ commit }, { boardId, card }){
            const response = await apiPATCH(`/boards/${boardId}/cards`, { 'action': 'update', 'card': card });
            if (response.status == 200){
                commit('UPDATE_CARD', { boardId, card });
                return response.json;
            }
        },
        async deleteCardFromBoard({ commit }, { boardId, card }){
            const response = await apiPATCH(`/boards/${boardId}/cards`, { 'action': 'delete', 'card': card });
            if (response.status == 200){
                commit('DELETE_CARD', { boardId, card });
                return response.json;
            }
        },
        async uploadFileToCard({ commit }, { boardId, cardId, file }) {
          const response = await apiPOST(`/upload/${cardId}`, { boardId, cardId, file });
          if (response.status === 201) {
            commit('ADD_FILE_TO_CARD', { boardId, cardId, file: response.json });
          }
        },
        async deleteFileFromCard({ commit }, { boardId, cardId, fileId }) {
            const response = await apiDELETE(`/upload/${fileId}`);
            if (response.status === 200) {
                commit('REMOVE_FILE_FROM_CARD', { boardId, cardId, fileId });
            }
        },
        async updateBoardStatus({ commit }, { boardId, statusName, toStatusName, toStatusColor }) {
            const response = await apiPATCH(`/boards/${boardId}/status`, {
              action: 'modify',
              statusName,
              toStatusName,
              toStatusColor
            });
            if (response.status === 200) {
              commit('UPDATE_STATUS', { statusName, toStatusName, toStatusColor });
            }
          },
          async deleteBoardStatus({ commit }, { boardId, statusName }) {
            const response = await apiPATCH(`/boards/${boardId}/status`, {
              action: 'delete',
              statusName
            });
            if (response.status === 200) {
              commit('DELETE_STATUS', statusName);
            }
          }
    },
    getters: {
        isAuthenticated: state => !!state.token,
        user: state => state.user,
        boards: state => state.boards,
        board: state => state.board,
        boardCreated: state => state.boardCreated,
        user: state => state.user
    }
})

export default store