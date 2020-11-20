<template>
  <v-container>
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>

    <div v-if="!overlay">
      <div style="font-size: 0rem;">{{ pg_arr }}</div>
      <div v-if="isData">

        <v-carousel
          height="auto"
          hide-delimiters
          show-arrows-on-hover
          >
          <v-carousel-item
            v-for="mainEvent in getRecentEventss"
            :key="mainEvent.id"
            :src="'/images/' + mainEvent.image"
            cycle
            @click="$router.push({ path: `/event/${mainEvent.id}` })"
          >
          </v-carousel-item>
        </v-carousel>

      <v-row style="margin-top: 20px;">
        <v-col
          :lg="12 / getRecentEventss[0].events.length"
          sm="12"
          md="6"
          v-for="(event,id) in getRecentEventss[0].events"
          :key="id"
        >
          <v-card
          style="margin-bottom: 20px;"
          >
          <router-link :to="'/event/' + event.main_id">
            <v-img
              class="white--text align-end"
              height="200px"
              :src="image[id]"
            >
            </v-img>
          </router-link>
            <v-card-text>
              <p style="font-size:1rem !important;">
              {{new Date(event.timeStart).toLocaleDateString('en-GB')}} | {{ event.title }}</p>
              <v-progress-linear
              color="green"
              height="30"
              style="margin-bottom: 20px;"
              :value="event.progress"
              v-if="event.isActive == 1"
            ><template>
              <div class="timeInfo">
                 {{ new Date(event.timeStart).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
                 -
                 {{ new Date(event.timeStop).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
               </div>
            </template>
            </v-progress-linear>
            <!-- <div v-else> -->
              <div v-else class="timeInfo"><v-icon>mdi-clock</v-icon>
                 {{ new Date(event.timeStart).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
                 -
                 {{ new Date(event.timeStop).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) }}
               </div>
            <!-- </div> -->
            <p style="margin-top: 10px;" v-if="event.place !== '-'">
              <v-icon size="20">mdi-google-maps</v-icon>{{ event.place }}
            </p>
            </v-card-text>

            	<v-row>
            		<v-col v-if="event.subevents.length > 0">
		                <v-container @click="showMore = true; $router.push(`/more_event/${event.id}`)" class="text-center" align="center"
		                  style="padding: 5px; width: 120px; font-size: 0.726rem; cursor: pointer; color: blue"
		                >
		                ПОДРОБНЕЕ
		                </v-container>
		            </v-col>
		            <v-col>
		            	<router-link :to="'/event/' + event.main_id">
			                <v-container class="text-center" align="center"
			                  style="padding: 5px; width: 120px; font-size: 0.726rem; color:blue"
			                >
			                ПРОГРАММА МЕРОПРИЯТИЯ
			                </v-container>
			            </router-link>
		            </v-col>
		        </v-row>
            </v-card>
        </v-col>
      </v-row>
    </div>
  <div v-else>
    <v-card-title>Пока нет мероприятий</v-card-title>
  </div>
</div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
// import axios from 'axios'
  export default {
    data () {
      return {
        image: [
          '/images/era.jpg',
          '/images/2.jpg',
          '/images/3.jpg',
        ],
        overlay: true,
        value: '',
        isData: false,
        main_events: '',
        showMore: false,
        bar_date: [],
        progress_arr: []
      }
    },

    async mounted() {

      	// if (!localStorage.getItem('user') || Object.keys(this.getUser).length == 0) {
        // 	this.$fire({
        //     	title: "Уведомление",
        //     	text: "Необходимо авторизоваться!",
        //     	type: "error",
        // 	})
        // 	.then(this.$router.push('/howtouse'));
      	// }

      	document.title = 'Технополис "ЭРА" | Главная';
      	this.$emit('update:title', 'Главная')
      	await this.getRecEvents()
      	console.log(this.main_event_get)

      	if (this.main_event_get.length > 0) {
      		this.isData = true
			    this.overlay = false
			    await this.getBlue()
          await setInterval(this.getBlue, 2000)
      		await this.updateBarFunc()
      		await setInterval(this.updateBarFunc, 500)
      	} else {
      		this.isData = false
      		this.overlay = false
      	}
    },

    computed: {
       ...mapGetters(['getRecentEventss', 'getUser', 'getNow']),
       main_event_get() {
       	return this.main_events
      },

      pg_arr() {
        return this.progress_arr
      }
    },

    methods: {
      ...mapActions(['updateBar', 'getRecentEvents']),

      async getRecEvents() {
      	this.main_events = await this.getRecentEvents()
      },

      timeBar(start, stop) {
        var _start = new Date(start).getTime()
        var _stop = new Date(stop).getTime()
        var now = Date.now()
        return (((now - _start) / (_stop - _start)) * 100)
      },

      async updateBarFunc() {
        this.getBlue()
        if(await this.updateBar([this.bar_date.timeStart, this.bar_date.timeStop]) == 1) {
          console.log("Change")
          this.getBlue()
        }
        this.value = this.getNow
      },

      getBlue() {
        var pg = []
        this.getRecentEventss[0].events.forEach(d => {
            if (new Date(d.timeStart) < Date.now() && new Date(d.timeStop) > Date.now()) {
                d.isActive = 1
                d.progress = this.timeBar(d.timeStart, d.timeStop)
                pg = d.progress
                this.bar_date = d
            }
            else if (new Date(d.timeStop) < Date.now()) {
                d.isActive = 2;
            }
            else if (new Date(d.timeStart) > Date.now()) {
                d.isActive = 0;
            }
        })
        this.progress_arr = pg
      },
    }
  }
</script>

<style scoped>
  .text--primary {height: 150px; overflow: hidden;}
  .transparent {
   /* position: relative; */
   position:absolute;
   width: 100%;
   bottom: 0;
   right:0;
   background-color: white!important;
   opacity: 0.7;
   border-color: transparent!important;
   border-radius: 0px !important;
 }
 .chip {
   width: 100%;
 }
 .timeInfo {
  font-size: 1rem;
 }

</style>
