<template>
	<v-container>

        <v-overlay :value="overlay">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>

        <div v-if="!overlay">
            <!-- <v-simple-table>
                <template v-slot:default>
                <thead>
                    <tr>
                    <th class="text-left">ФИО</th>
                    <th class="text-left">Роль</th>
                    <th class="text-left">Прибыл</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, id) in guests_today" :key="id">
                    <td>{{ item.last_name }} {{ item.name }} {{ item.second_name }}</td>
                    <td>{{ item.status }}</td>
                    <td v-if="item.isLoggedIn == 1" style="color: green;"><v-checkbox readonly color="green" v-model="ch1"></v-checkbox></td>
                    <td v-else style="color: red;"><v-checkbox readonly color="red" v-model="ch2"></v-checkbox></td>
                    </tr>
                </tbody>
                </template>
            </v-simple-table> -->

						<v-data-table
					    :headers="headers"
					    :items="guests_today"
					    :items-per-page="5"
					    class="elevation-1"
					  >
							<template v-slot:item.isLoggedIn="{ item }">
				        <v-checkbox v-if="item.isLoggedIn == 0" :success="success" readonly v-model="ch1"></v-checkbox>
								<v-checkbox readonly :error="error" style="color:red !important;" v-model="ch2" v-if="item.isLoggedIn == 1"></v-checkbox>
				      </template>
						</v-data-table>

            <br>
        </div>

        <!-- <div v-else>
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
                <template v-slot:actions>
                  <v-btn
                    color="primary"
                    text
                  >
                    Обновить информацию
                  </v-btn>
                </template>
              </v-banner>
            </v-container>
        </div> -->
    </v-container>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
	data() {
		return {
			ch1: true,
			search: '',
      ch2: false,
      overlay: true,
			success: true,
			error: true,
			headers: [
          { text: 'ФИО', value: 'name_all' },
          { text: 'Статус', value: 'isLoggedIn' },
        ],
		}
	},

	async mounted() {
		this.$emit('update:title', 'Гости')
		document.title = 'Технополис "ЭРА" | Гости';

		if (!localStorage.getItem('user') || Object.keys(this.getUser).length == 0) {
			this.$fire({
					title: "Уведомление",
					text: "Необходимо авторизоваться!",
					type: "error",
			})
			.then(this.$router.push('/'));
		}

		await this.$store.dispatch('guests_today')
        this.overlay = false
	},

	computed: mapGetters(['guests_today', 'getUser']),
}
</script>
