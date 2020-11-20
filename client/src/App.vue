<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list dense>
        <div
          v-if="getUser.id && getUser.id !== '000'"
        >
            <v-container class="pa-2">
              <div class="text-center">
                <v-avatar color="primary" size="50" class="initials">
                  <span class="white--text headline">{{first_letters(getUser.last_name, getUser.name)}}</span>
                </v-avatar>
                <v-list-item color="rgba(0, 0, 0, .4)">
                    <v-list-item-content class="pt-1 text">
                        <v-list-item-title class="title" style="margin-bottom:10px;">{{ getUser.last_name + ' ' + getUser.name }}</v-list-item-title>
                        <!-- <v-list-item-subtitle>Организация: {{ getUser.organization }}</v-list-item-subtitle> -->
                    </v-list-item-content>
                </v-list-item>
              </div>
            </v-container>
            </div>
            <div
              v-else-if="getUser.id === '000'"
            >
                <v-container class="pa-2">
                  <div class="text-center">
                    <v-avatar color="primary" size="50" class="initials">
                      <v-img src="/images/sad_dog.jpg"></v-img>
                    </v-avatar>
                    <v-list-item color="rgba(0, 0, 0, .4)">
                        <v-list-item-content class="pt-1 text">
                            <v-list-item-title class="title" style="margin-bottom:10px;">{{ getUser.last_name }}</v-list-item-title>
                            <v-list-item-subtitle>К сожалению, Вас забыли добавить в список гостей...</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                  </div>
                </v-container>
                </div>
              <div v-else>
                <v-container class="pa-2">
                  <div class="text-center">
                    <v-avatar size="50" class="initials">
                      <v-img src="/images/question.png"></v-img>
                    </v-avatar>
                    <v-list-item color="rgba(0, 0, 0, .4)">
                        <v-list-item-content class="pt-1 text">
                            <v-list-item-title class="title" style="margin-bottom:10px;">{{ getUser.last_name }}</v-list-item-title>
                            <v-list-item-subtitle>Кажется, вы забыли авторизоваться...</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                  </div>
                  <v-card-text>Отсканируйте QR-код на Вашем бэйдже</v-card-text>
                </v-container>
              </div>
          <v-divider></v-divider>

      <router-link to="/add" v-if="isAdmin">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-tooltip-edit</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Редактировать</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </router-link>

        <router-link to="/">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Главная</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link>

        <router-link to="/events">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-bell-check-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Программа</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link>

        <router-link to="/guests_today">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Участники</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link>

        <!-- <router-link to="/structure">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-castle</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Структура</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </router-link> -->

        <router-link to="/chief">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-account-star</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Руководство</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link>

        <!-- router-link to="/scheme">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-map</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Схемы технополиса</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link> -->

        <!-- <router-link to="/howtouse">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-information</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Информация</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link> -->

        <router-link to="/contacts">
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-television-guide</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Контакты</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </router-link>
      </v-list>

    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-icon style="margin-right: 10px" @click="$router.go(-1)">mdi-arrow-left</v-icon>
        <v-icon style="margin-right: 10px" @click="$router.go(1)">mdi-arrow-right</v-icon>
      <v-toolbar-title>
        <router-link
        style="color:white;"
        to="/"
        >
          {{ title }}
        </router-link>
      </v-toolbar-title>

    </v-app-bar>

    <v-main>
        <router-view
          style="margin-top: 10px;"
          v-bind:title.sync="title"
          :key="$route.fullPath"
        />
    </v-main>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">&copy; {{ new Date().getFullYear() }}</span>
      <v-spacer>
      </v-spacer>
      <span class="white--text">ФГАУ ВИТ "ЭРА"</span>
    </v-footer>
  </v-app>
</template>

<script>
import {mapGetters} from 'vuex'
// import IconifyIcon from '@iconify/vue';
// import accountCheck from '@iconify/vue/icons-mdi/account-check';

  export default {
    props: {
      source: String,
    },

    components: {
      // IconifyIcon,
    },

    data: () => ({
      drawer: null,
      icons: {
          // accountCheck: accountCheck,
      },

      title: '',
      // isAdmin: !JSON.parse(localStorage.getItem('user')).isActive || false
    }),



    mounted() {

    },

    computed: {
      ...mapGetters(['getUser', 'isAdmin']),
    },

    methods: {
      check() {
      },

      goToAccount() {
        this.$router.push('/user/' + JSON.parse(localStorage.getItem('user')).user_id)
      },

      setTitle (title) {
        this.title = title
      },

      first_letters(name, surname) {
                let fl = surname[0]
                let sl = name[0]
                return sl+fl
            },
    },

  }
</script>

<style>

* {
  font-family: 'Oxygen';
}
  a {
    text-decoration: none;
  }
</style>
