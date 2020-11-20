<template>
    <v-container>
        <v-card-title>Регистрация</v-card-title>
        <v-card-text>
            <p>Выберите файл с участниками</p>
            <form enctype="multipart/form-data" @submit.prevent>
                <v-file-input
                    v-model="file"
                    label="Файл с участниками"
                    filled
                    prepend-icon="mdi-account-multiple-outline"
                    id="file-input"
                    accept=".xlsx"
                ></v-file-input>
                <v-btn color="purple darken-4" tile class="button" @click="onSubmitUsers" :disabled="!file">Загрузить</v-btn>
            </form>
            <v-row>
                <v-col cols="3">
                    <v-btn color="purple darken-4" tile class="button" @click="deleteUsers">Удалить всех</v-btn>
                </v-col>
                <v-col cols="3">
                    <v-btn color="purple darken-4 mt-3" v-if="isUploaded" tile :href="fileUrl" class="button">Скачать файл</v-btn>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-title>Добавление мероприятий</v-card-title>
        <v-card-text>
            <p>Выберите файл с мероприятиями</p>
            <form enctype="multipart/form-data" @submit.prevent>
                <v-file-input
                    v-model="fileEvents"
                    label="Файл с мероприятиями"
                    filled
                    prepend-icon="mdi-folder-multiple"
                    id="file-input"
                    accept=".xlsx"
                ></v-file-input>
                <v-btn color="purple darken-4" tile class="button" @click="onSubmitEvents" :disabled="!fileEvents">Загрузить</v-btn>
            </form>
        </v-card-text>

        <v-card-title>Редактировать мероприятие</v-card-title>
        <v-card-text>
            <v-simple-table>
                <template v-slot:default>
                <thead>
                    <tr>
                    <th class="text-left">Мероприятие</th>
                    <th class="text-left">ID</th>
                    <th class="text-left">Действие</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, id) in events" :key="id">
                    <td>{{ item.mainTitle }}</td>
                    <td>{{ item.id }}</td>
                    <td>
                        <v-btn text @click="showEdit = true; event = item; getEventData()"><v-icon>mdi-tooltip-edit</v-icon></v-btn>
                        <v-btn @click="deleteEvent(item.id)" text><v-icon>mdi-delete</v-icon></v-btn>
                    </td>
                    </tr>
                </tbody>
                </template>
            </v-simple-table>

            <v-dialog v-model="showEdit" persistent max-width="600px">
                <v-card>
                    <v-card-title>
                    <span class="headline">Редактировать {{ event.mainTitle }}</span>
                    </v-card-title>
                    <v-card-text>
                    <v-container>
                        <v-row>
                        <v-col cols="12" sm="12" md="12" rows="20">
                            <v-textarea label="Описание" v-model="upEvent.title" required></v-textarea>
                        </v-col>
                        <v-col cols="12" sm="12" md="12">
                            <v-text-field label="Ссылка на изображение" v-model="upEvent.image" hint="В папке проекта"></v-text-field>

                            <v-file-input
                                v-model="file_img"
                                label="Изображение"
                                filled
                                prepend-icon="mdi-account-multiple-outline"
                                id="file-input"
                            ></v-file-input>

                        </v-col>
                        <v-col>
                            <v-checkbox v-for="(user,id) in getUsers" :key="id" v-model="selected" :label="user.last_name + ' ' + user.name" :value="user.id"></v-checkbox>
                        </v-col>
                        </v-row>
                    </v-container>
                    </v-card-text>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showEdit = false">Закрыть</v-btn>
                    <v-btn color="blue darken-1" text @click="showEdit = false; editEvent(event.id)">Обновить</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

        </v-card-text>
    </v-container>
</template>

<script>
import axios from 'axios'
import 'vue-datetime/dist/vue-datetime.css'
import { mapGetters } from 'vuex'
    export default {

        computed: {
            ...mapGetters(['isAdmin', 'getUsers'])
        },

        data() {
            return {
                showEdit: '',
                event: '',
                selected: [],
                upEvent: {
                    title: null,
                    image: null,
                    guests: null
                },

                file: null,
                isUploaded: false,
                fileUrl: '',
                file_img: null,
                fileEvents: null,

                events: []
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

            if (!this.isAdmin) {
                this.$router.push('/')
            }
            await this.$emit('update:title', 'Настройки')
            await this.$store.dispatch('getRecentEvents')

            await axios.get(this.$store.state.getUrl + 'api/getEvents')
            .then(res => {
                console.log(res.data)
                this.events = res.data
            })

        },

        methods: {
            async deleteUsers() {
                await axios.get('/api/deleteUsers')
                .then(res => {
                    if (res.data == "Success") {
                        this.$fire({
                            title: "Уведомление",
                            text: "Пользователи успешно удалены!",
                            type: "success",
                            timer: 2000
                        });
                    } else {
                        this.$fire({
                            title: "Уведомление",
                            text: "Ошибка!",
                            type: "error",
                            timer: 2000
                        });
                    }
                })
            },

            async getEventData() {
                await axios.get(this.$store.state.getUrl + 'api/getCustomEvent/'+ this.event.id)
                .then(res => {
                    console.log(res)
                    this.upEvent.title = res.data.data[0].description
                    this.upEvent.image = res.data.data[0].image
                    this.upEvent.guests = res.data.guests

                })
                console.log(this.upEvent.guests)
                await this.$store.dispatch('getUsers')
            },

            async editEvent(id) {

                const formData = new FormData()
                formData.append('file', this.file_img)
                formData.append('data', JSON.stringify(this.upEvent))
                formData.append('id', id)
                formData.append('guests', JSON.stringify(this.selected))

                await axios.post(this.$store.state.getUrl + "api/updateEvent", formData)
                .then(async res => {
                    console.log(res)
                    if (res.data == "Success") {
                        this.$fire({
                            title: "Уведомление",
                            text: "Мероприятие успешно обновлено!",
                            type: "success",
                            timer: 2000
                        });
                    }
                })

                await axios.get(this.$store.state.getUrl + 'api/getEvents')
                .then(res => {
                    console.log(res)
                    console.log(res.data)
                    this.events = res.data
                })
            },

            async deleteEvent(id) {
                await axios.get(this.$store.state.getUrl + 'api/deleteEvent/' + id)
                .then(res => console.log(res))

                await axios.get(this.$store.state.getUrl + 'api/getEvents')
                .then(res => {
                    if (res.data.result == "Empty") {
                        this.events = []
                    }
                    else {
                        this.events = res.data
                    }
                })

                await this.$fire({
                    title: "Уведомление",
                    text: "Мероприятие успешно удалено!",
                    type: "success",
                    timer: 2000
                });
            },

            async onSubmitUsers() {
                const formData = new FormData()
                formData.append('file', this.file)

                await axios.post(this.$store.state.getUrl + 'api/upload', formData)
                .then(res => {
                    console.log(res)
                    this.isUploaded = true
                    this.fileUrl = res.data
                })
            },

            async onSubmitEvents() {
                const formData = new FormData()
                formData.append('file', this.fileEvents)

                await axios.post(this.$store.state.getUrl + 'api/uploadEvents', formData)

                this.$fire({
                    title: "Уведомление",
                    text: "Мероприятия успешно добавлены! Теперь в панели управления добавьте описание и ссылку на изображение",
                    type: "success",
                    timer: 2000
                });

                this.fileEvents = []

                await axios.get(this.$store.state.getUrl + 'api/getEvents')
                .then(res => {
                    console.log(res.data)
                    this.events = res.data
                })
            },
        }
    }
</script>

<style scoped>
   .button {color: #fff;}

   .datetime {
       border: 1px solid grey;
       width: 200px;
       padding: 5px;
   }
</style>
