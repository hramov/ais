<template>
    <v-container>
        <v-overlay :value="overlay">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>

        <div v-if="!overlay" style="margin-top:20px;">
          <div style="font-size: 0rem;">{{ pg_arr }} {{ pg_sub_arr}} </div>
        <v-row>
            <v-col
                lg="6"
                md="6"
                sm="12"
                xs="12"
            >
                <v-card
                style="margin-top: -30px;"
                flat>
                    <v-img
                        :src="'/images/' + mainEvent.image"
                        ></v-img>
                    <v-card-text style="font-size: 1.1rem; text-align: justify;">{{ mainEvent.mainDesc }}</v-card-text>
                </v-card>
            </v-col>
            <v-col
                lg="6"
                md="6"
                sm="12"
                xs="12"
            >
            <v-card
                flat
                style="padding: 10px; margin-top:-40px"
            >

                <v-expand-transition>
                <div v-show="show">
                <v-expansion-panels flat popout accordion multiple>
                    <v-expansion-panel
                        v-for="event in mainEvent.events"
                        :key="event.id"
                        style="margin-bottom: 5px; padding: 0px;"
                    >
                    <!-- :value="timeBar(event.timeStart, event.timeStop)" -->


                        <v-expansion-panel-header
                        v-if="event.isActive == 1"
                        >
                            <v-icon>mdi-access-point</v-icon><div style="font-size: 0.9rem; text-align: left !important; padding-left: 7px;"> {{ new Date(event.timeStart).toLocaleDateString('en-GB')}} | {{ event.title }}</div>
                        </v-expansion-panel-header>

                        <v-progress-linear
                        style="border-radius: 5px;"
                        color="green"
                        height="15"
                        v-if="event.isActive == 1"
                        v-model="event.progress"
                        >{{ event.progress.toFixed(2) }}%</v-progress-linear>

                    <v-expansion-panel-header
                    v-if="event.isActive == 2"
                    style="background-color:#E0E0E0; border-radius: 5px;"
                    >
                        {{ event.title }}
                    </v-expansion-panel-header>

                    <v-expansion-panel-header
                    v-else-if="event.isActive == 0"
                    style="background-color:#29B6F6; border-radius: 5px;"
                    >
                      {{ new Date(event.timeStart).toLocaleDateString('en-GB')}} | {{ event.title }}
                    </v-expansion-panel-header>

                    <v-expansion-panel-content v-if="event.subevents">
                        <v-icon size="15">mdi-clock</v-icon>
                        {{ new Date(event.timeStart).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
                 -
                 {{ new Date(event.timeStop).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
                        <br />
                        <div v-if="event.place !== '-'">
                          <v-icon size="20">mdi-google-maps</v-icon>{{ event.place }}
                        </div>
                            <v-list-item three-line v-for="subevent in event.subevents" :key="subevent.id">
                                <v-list-item-content>
                                <v-list-item-title>{{ subevent.subTitle }}</v-list-item-title>
                                <v-list-item-subtitle>
                                </v-list-item-subtitle>
                                <v-list-item-subtitle>
                                    <v-icon>mdi-clock</v-icon>
                                    {{ new Date(subevent.subTimeStart).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }} -
                                    {{ new Date(subevent.subTimeStop).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
                                </v-list-item-subtitle>

                                <v-list-item-subtitle v-if="event.place !== '-'">
                                    <v-icon>mdi-google-maps</v-icon>
                                    {{ event.place }}
                                </v-list-item-subtitle>

                                <v-progress-linear
                                    v-if="subevent.isActive == 1"
                                    color="green"
                                    height="30"
                                    style="margin-bottom: 20px;"
                                    :value="subevent.progress"
                                >
                                  <template>
                                    <div style="border-radius: 10px !important; color:white; font-size: 0.9rem; text-align: left !important;">Идет сейчас</div>
                                  </template>
                                </v-progress-linear>

                                    <v-chip
                                    style="justify-content: center;"
                                        color="grey"
                                        text-color="white"
                                        class="chip"
                                        v-else-if="subevent.isActive == 2"
                                        label
                                        >
                                        Окончено
                                    </v-chip>
                                    <v-chip
                                        style="justify-content: center;"
                                        color="blue"
                                        text-color="white"
                                        class="chip"
                                        v-else-if="subevent.isActive == 0"
                                        label
                                        >
                                        Ожидается
                                    </v-chip>
                                </v-list-item-content>
                            </v-list-item>
                    </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
                </div>
            </v-expand-transition>
            <v-btn
            outlined
            rounded
            width="100%"
            style="margin-top: 10px;"
            @click="$router.push({ path: `/guests/${mainEvent.id}`})"
        >Список участников</v-btn>
        </v-card>
        </v-col>
    </v-row>
    </div>
    </v-container>

</template>

<script>
import axios from 'axios'
import {mapGetters, mapActions} from 'vuex'
    export default {
        data() {
            return {
                mainEvent: {},
                date: [],
                dateFilt: [],
                show: true,
                eventId: '',
                isLoad: false,
                img: '',
                overlay: true,
                bar_date: '',
                bar_date_sub: '',
                value: '',
                subvalue: '',
                progress_arr: [],
                progress_arr_sub: []
            }
        },

        computed: {
          ...mapGetters(['getNow', 'getSubNow']),

          pg_arr() {
            return this.progress_arr
          },

          pg_sub_arr() {
            return this.progress_arr_sub
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

            await axios.get(this.$store.state.getUrl + 'api/getSingleEvent/' + this.$route.params.id)
            .then(async res => {
                this.mainEvent = res.data[0]
                await this.sortEvents()
                this.$emit('update:title', await this.mainEvent.mainTitle)
                this.eventId = this.mainEvent.id
                this.overlay = false
            })

            await this.getBlue()
            // await this.updateBarFunc()
            setInterval(await this.getBlue, 2000)
        },

        methods: {
            ...mapActions(['updateBar', 'updateSubBar']),

            updateBarFunc() {
                this.updateBar([this.bar_date.timeStart, this.bar_date.timeStop])
                this.updateSubBar([this.bar_date_sub.subTimeStart, this.bar_date_sub.subTimeStop])

                this.value = this.getNow
                this.subvalue = this.getSubNow
            },

            timeBar(start, stop) {
                var _start = new Date(start).getTime()
                var _stop = new Date(stop).getTime()
                var now = Date.now()
                return (((now - _start) / (_stop - _start)) * 100)
            },

            getBlue() {
              var pg = []
              var pg_sub = []
                this.mainEvent.events.forEach(d => {
                    if (new Date(d.timeStart) < Date.now() && new Date(d.timeStop) > Date.now()) {
                        d.isActive = 1
                        d.progress = this.timeBar(d.timeStart, d.timeStop)
                        pg.push(d.progress)
                        this.bar_date = d
                        this.bar_date.sub = []
                    }
                    else if (new Date(d.timeStop) < Date.now()) {
                        d.isActive = 2;
                    }
                    else if (new Date(d.timeStart) > Date.now()) {
                        d.isActive = 0;
                    }

                    d.subevents.forEach(d => {
                        if (new Date(d.subTimeStart) < Date.now() && new Date(d.subTimeStop) > Date.now()) {
                            d.isActive = 1
                            d.progress = this.timeBar(d.timeStart, d.timeStop)
                            pg_sub.push(d.progress)
                            this.bar_date_sub = d
                        }
                        else if (new Date(d.subTimeStop) < Date.now()) {
                            d.isActive = 2;
                        }
                        else if (new Date(d.subTimeStart) > Date.now()) {
                            d.isActive = 0;
                        }
                    })
                })
                this.progress_arr = pg;
                this.progress_arr_sub = pg_sub;
            },

            getWeekDay(date) {
                let days = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];
                return days[new Date(date).getDay() + 1];
            },

            async sortEvents() {
                this.mainEvent.events = await this.mainEvent.events.sort(function (a, b) {
                    if (a.timeStart > b.timeStart) {
                        return 1;
                    }
                    if (a.timeStart < b.timeStart) {
                        return -1;
                    }
                    return 0;
                });
            },
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
