<template>
    <v-container>

            <v-row align="center" justify="center" style="margin-top: 10px;">
                <v-img max-width="500px" src="/images/unnamed.png"></v-img>
            </v-row>
            <v-card-text>
                Цель создания Военного инновационного технополиса ЭРА — обеспечить поиск, развитие и внедрение прорывных технологий в оборонной сфере. 
                Пристальное внимание уделено образовательным программам для молодых ученых в рядах Российской Армии. 
                Расположение Технополиса на морском побережье создает комфортные условия для работы и жизни.
            </v-card-text>
            <v-list disabled>
            <v-subheader>Основная информация</v-subheader>
            <v-list-item-group color="primary">
                <v-list-item
                v-for="(item, i) in items"
                :key="i"
                >
                <v-list-item-icon>
                    <v-icon v-text="item.icon"></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                    <v-list-item-title v-text="item.text"></v-list-item-title>
                </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
            </v-list>
            <v-subheader>Обратная связь</v-subheader>
            <v-container><v-form>
                <v-text-field
                v-model="subject"
                    :counter="200"
                    label="Тема обращения"
                    required
                ></v-text-field>
                <v-textarea
                v-model="body"
                    label="Сообщение"
                    required
                ></v-textarea>
                <v-btn
                    style="margin-bottom: 20px;"
                    @click="feedback"
                >
                    Отправить
                </v-btn>
            </v-form></v-container>
        <!-- </v-card> -->

        <!-- <GoogleMap /> -->
    </v-container>
</template>


<!-- AIzaSyDwV-pw8AvDaeecQNg1-Wfmg_T__z99kNM -->

<script>
// import GoogleMap from "../components/GoogleMap";
import axios from 'axios'
export default {
    data() {
        return {
            item: 0,
            items: [
                { text: '353456, Краснодарский край, г.Анапа, Пионерский пр., 41', icon: 'mdi-google-maps' },
                { text: 'Пн…Пт с 09:00 до 18:00', icon: 'mdi-clock' },
                { text: '+7(495)693-30-98', icon: 'mdi-phone' },
                { text: '+7(495)693-30-91', icon: 'mdi-phone' },
            ],

            subject: '',
            body: ''
        }
    },
    mounted() {

        document.title = 'Технополис "ЭРА" | Контакты';
        this.$emit('update:title', 'Контакты')
    },
    components: {
        // GoogleMap
    },

    methods: {
        feedback() {
            axios.post(this.$store.state.getUrl + 'api/createFeedback', {
                subject: this.subject,
                body: this.body,
                user_id: JSON.parse(localStorage.getItem('user')).user_id
            })
            .then(res => {
                if (res.data == "Success") {
                    this.$fire({
                        title: "Уведомление",
                        text: "Успешно отправлено!",
                        type: "success",
                        time: "2000"
                    })
                }
                else {
                    this.$fire({
                        title: "Уведомление",
                        text: "Ошибка!",
                        type: "error",
                        time: "2000"
                    })
                }
            })
            .catch(err => {
                this.$fire({
                        title: "Уведомление",
                        text: "Ошибка!" + err,
                        type: "error",
                        time: "2000"
                    })
            })

            this.subject = ""
            this.body = ""
        }
    }
}
</script>