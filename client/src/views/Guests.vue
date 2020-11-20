<template>
    <v-container>
        <v-overlay :value="overlay">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>

        <div v-if="!overlay && guestsGetter.guests.length > 0">

            <v-data-table
					    :headers="headers"
					    :items="guestsGetter.guests"
					    :items-per-page="5"
					    class="elevation-1"
					  >
							<template v-slot:item.isLoggedIn="{ item }">
				        <v-checkbox v-if="item.isLoggedIn == 1" :success="success" readonly v-model="ch1"></v-checkbox>
								<v-checkbox readonly :error="error" style="color:red !important;" v-model="ch2" v-if="item.isLoggedIn == 0"></v-checkbox>
				      </template>
						</v-data-table>

            <br>
            <v-card-actions class="justify-center">
                <v-btn
                    :loading="isLoad"
                    @click="getPlace"
                    outlined
                >Показать место
                </v-btn>
            </v-card-actions>
            <div v-if="img.length > 0">
                <v-card-title></v-card-title>
                <span v-html="img"></span>
            </div>
        </div>

        <div v-else-if="!overlay && guestsGetter.guests.length == 0">
            <v-container>
                <v-banner single-line>
                <v-icon
                  slot="icon"
                  color="warning"
                  size="36"
                >
                  mdi-wifi-strength-alert-outline
                </v-icon>
                На данное мероприятие еще никто не зарегистрировался!
              </v-banner>
            </v-container>
        </div>

    </v-container>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import axios from 'axios'

    export default {
        components: {
        },

        data() {
            return {
                isLoad: false,
                ch1: true,
                ch2: false,
                img: '',
                isSignUp: false,
                overlay: true,
                headers: [
                    { text: 'ФИО', value: 'name_all' },
                    { text: 'Статус', value: 'isLoggedIn' },
                  ],
                  success: true,
                  error: true
            }
        },

        async mounted() {
            if (!this.$store.state.user || Object.keys(this.$store.state.user).length == 0) {
            this.$fire({
                title: "Уведомление",
                text: "Необходимо авторизоваться!",
                type: "error",
            })
            .then(this.$router.push('/'));
            }

            await this.getGuests(this.$route.params.id)

            await this.$emit('update:title', await this.guestsGetter.main_event[0].title)
            document.title = 'Технополис "ЭРА" | Участники'
            this.overlay = false
        },

        methods: {
            ...mapActions(['getGuests']),

            async getPlace() {
                this.isLoad = true
                await this.$store.dispatch('getUsers')
                await axios.post(this.$store.state.getUrl + 'api/getPlace', {
                    guests: await this.$store.state.users,
                    user: JSON.parse(localStorage.getItem('user')).id
                })
                .then(res => {
                    this.img = res.data
                    this.isLoad = false
                })
            }
        },

        computed: {
          ...mapGetters(['guestsGetter', 'placeGetter']),
          }
    }
</script>

<style>

</style>
