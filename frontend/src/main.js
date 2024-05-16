import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { setupCalendar } from 'v-calendar'
import 'v-calendar/style.css'
import { KanbanPlugin } from '@syncfusion/ej2-vue-kanban'

import './style.css'

const app = createApp(App)

app.use(setupCalendar, {})
app.use(router)
app.use(store)
app.use(KanbanPlugin)

app.mount('#app')