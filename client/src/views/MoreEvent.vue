<template>
	<v-container>
		<v-overlay :value="overlay">
      		<v-progress-circular indeterminate size="64"></v-progress-circular>
    	</v-overlay>

    	<div v-if="getMoreEvent[0]">
				<div style="font-size: 0rem;">{{ pg_arr }}</div>
			<v-expansion-panels popout>
			    <v-expansion-panel
			      v-for="event in getMoreSubEvent"
			      :key="event.id"
			      style="margin-bottom: 10px; border-radius: 5px;"
			    >

			    <div v-if="event.isActive == 1">
			      	<v-expansion-panel-header>
			      		{{ new Date(event.timeStart).toLocaleDateString() }}	|	{{ event.title.split(':')[0] }}
			      	</v-expansion-panel-header>

			      	<v-progress-linear
			      		:value="event.progress"
			      	>
			      	</v-progress-linear>
			    </div>

			    <div v-if="event.isActive == 2">
			      	<v-expansion-panel-header style="background-color: grey; border-radius: 5px;">
			      		{{ new Date(event.timeStart).toLocaleDateString() }}	|	{{ event.title.split(':')[0] }}
			      	</v-expansion-panel-header>
			    </div>

			    <div v-if="event.isActive == 0">
			      	<v-expansion-panel-header style="background-color: #29B6F6; border-radius: 5px;">
			      {{ new Date(event.timeStart).toLocaleDateString() }}	|	{{ event.title.split(':')[0] }}
			      	</v-expansion-panel-header>
			    </div>

			      	<v-expansion-panel-content>
			        {{ event.title.split(':')[1]}}
			        <p><v-icon>mdi-clock</v-icon>{{ new Date(event.timeStart).toLocaleTimeString().substr(0, new Date(event.timeStart).toLocaleTimeString().length - 3) }}
								-
								{{ new Date(event.timeStop).toLocaleTimeString().substr(0, new Date(event.timeStop).toLocaleTimeString().length - 3) }}</p>
			        <p v-if="event.place !== '-'"><v-icon>mdi-google-maps</v-icon> {{ event.place }}</p>
			      	</v-expansion-panel-content>
			    </v-expansion-panel>
			</v-expansion-panels>

			<v-btn
				width="100%"
				outlined
				style="margin-top: 10px;"
				@click="$router.push(`/event/${getMoreEvent[0].main_id}`)"
			>Вся программа</v-btn>

		</div>
	</v-container>
</template>

<script>
	import { mapGetters, mapActions} from 'vuex'
	export default {
		data() {
			return {
				overlay: true,
				progress_arr: []
			}
		},

		async mounted() {

			if (!localStorage.getItem('user') || Object.keys(this.getUser).length == 0) {
				this.$fire({
						title: "Уведомление",
						text: "Необходимо авторизоваться!",
						type: "error",
				})
				.then(this.$router.push('/'));
			}

			await this.get_more_event(this.$route.params.id)
			await this.sortEvents()
			await this.getBlue()

			this.overlay = false

			document.title = 'Технополис "ЭРА" | ' + this.getMoreEvent[0].title;
      		this.$emit('update:title', this.getMoreEvent[0].title)

			setInterval(this.getBlue, 2000)
		},

		methods: {
			...mapActions(['get_more_event', 'updateBar']),

			async sortEvents() {
                this.getMoreSubEvent = await this.getMoreSubEvent.sort(function (a, b) {
                    if (a.timeStart > b.timeStart) {
                        return 1;
                    }
                    if (a.timeStart < b.timeStart) {
                        return -1;
                    }
                    return 0;
                });
            },

            getBlue() {
							var pg = []
                this.getMoreSubEvent.forEach(d => {
                    if (new Date(d.timeStart) < Date.now() && new Date(d.timeStop) > Date.now()) {
                        d.isActive = 1
												d.progress = this.timeBar(d.timeStart, d.timeStop)
												pg.push(d.progress)
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

            updateBarFunc() {
            	this.getBlue()
                this.updateBar([this.bar_date.timeStart, this.bar_date.timeStop])

                this.value = this.getNow
            },

						timeBar(start, stop) {
			        var _start = new Date(start).getTime()
			        var _stop = new Date(stop).getTime()
			        var now = Date.now()
			        return (((now - _start) / (_stop - _start)) * 100)
			      },

		},

		computed: {
			...mapGetters(['getMoreEvent', 'getMoreSubEvent', 'getUser']),

			pg_arr() {
				return this.progress_arr
			}
		}
	}
</script>
