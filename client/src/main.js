import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueSimpleAlert from "vue-simple-alert";

import { Datetime } from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'

import * as VueGoogleMaps from "vue2-google-maps";
Vue.use(Datetime)
Vue.config.productionTip = false;
Vue.use(VueSimpleAlert);

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyDwV-pw8AvDaeecQNg1-Wfmg_T__z99kNM",
    libraries: "places" // necessary for places input
  }
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
