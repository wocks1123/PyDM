import Vue from 'vue'
import App from './App.vue'
import {store} from './store/store';
import {Constants} from "@/Const/Constants";
import {Request} from './plugins/Requests'
import {SocketPlugin} from './plugins/socket'
import vuetify from './plugins/vuetify';


Vue.config.productionTip = false

new Vue({
  store,
  Constants,
  SocketPlugin,
  Request,
  vuetify,
  render: h => h(App)
}).$mount('#app')
