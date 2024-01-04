import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import axios from 'axios'
import VueAxios from 'vue-axios'
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Row from 'primevue/row'; 
import ColumnGroup from 'primevue/columngroup';
import Message from 'primevue/message';
import Dialog from 'primevue/dialog';
import InlineMessage from 'primevue/inlinemessage';
import MultiSelect from 'primevue/multiselect';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext'

import 'primeicons/primeicons.css';
import "primevue/resources/themes/lara-light-blue/theme.css";
import "primevue/resources/primevue.min.css";

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App).use(vuetify)
app.use(VueAxios, axios)
app.use(PrimeVue);
import './assets/main.css'

// const app = createApp(App)
app.use(router)
app.component('DataTable', DataTable);
app.component('Row', Row);
app.component('Column', Column);
app.component('ColumnGroup', ColumnGroup);
app.component('Message', Message);
app.component('Dialog',Dialog);
app.component('InlineMessage', InlineMessage);
app.component('MultiSelect', MultiSelect);
app.component('Button', Button);
app.component('InputText', InputText);
app.mount('#app')
