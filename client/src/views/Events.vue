<template>
    <v-container>
        <v-overlay :value="overlay">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
        <div v-if="!overlay">
            <v-row>
                <v-col
                    lg="12"
                    sm="12"
                    md="12"
                    v-for="event in getEvents" :key="event.id"
                >
                    <v-card
                    max-width="100%"
                    elevation
                    style="margin-bottom: 20px;">
                        <router-link :to="'/event/' + event.id">
                        <v-img
                            max-width="100%"
                            :src="'/images/' + event.image"
                        ></v-img></router-link>
                    </v-card>
                </v-col>
            </v-row>
        </div>
    </v-container>

</template>

<script>
    import {mapGetters} from 'vuex'
    export default {
        data() {
            return {
                events: [],
                date: [],
                dateFilt: [],
                show: true,
                isLoad: false,
                overlay: true
            }
        },

        computed: {
            ...mapGetters(['getEvents']),
            getUrl() {
                return this.$store.state.url
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

            document.title = 'Технополис "ЭРА" | Программа';
            this.$emit('update:title', 'Программа')

            this.overlay = await this.load()
        },

        methods: {
            async load() {
                await this.$store.dispatch('getEvents')
                return false
            },
            async getEvent(id) {
                this.$router.push({ path: `/event/${id}` })
            },

            // async sortEvents() {
            //     this.getEvents.events = await this.getEvents.events.sort(function (a, b) {
            //         if (a.timeStart > b.timeStart) {
            //             return 1;
            //         }
            //         if (a.timeStart < b.timeStart) {
            //             return -1;
            //         }
            //         return 0;
            //     });
            // },
            // async getBlue() {
            //     for (let i = 0; i < this.getEvents.events.length; i++) {
            //         if (Number(new Date(this.getEvents.events[i].timeStart)) < Date.now() && Number(new Date(this.getEvents.events[i].timeStop)) > Date.now()) {
            //             this.getEvents.events[i].isActive = 1
            //         }
            //         else if (Number(new Date(this.getEvents.events[i].timeStop)) < Date.now()) {
            //             this.getEvents.events[i].isActive = 2;
            //         }
            //         else if (Number(new Date(this.getEvents.events[i].timeStart)) > Date.now()) {
            //             this.getEvents.events[i].isActive = 0;
            //         }
            //     }
            // },
            // async addEvents() {
            //     for (let i = 0; i < this.getEvents.events.length; i++) {
            //         for(let j = 0; j < this.dateFilt.length; j++) {
            //             if (this.dateFilt[j].date == new Date(this.getEvents.events[i].timeStart).toLocaleDateString()) {
            //                 this.dateFilt[j].getEvents.events.push(this.getEvents.events[i])
            //             }
            //         }
            //     }
            // },
            // getWeekDay(date) {
            //     let days = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];
            //     return days[new Date(date).getDay() + 1];
            // }
        }
    }
</script>

<style scoped>
    .isNow {
        background: #d5e6a2;;
    }

    .v-expansion-panel-content__wrap {
        padding: 0px !important;
    }
</style>
