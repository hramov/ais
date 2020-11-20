<template>
    <v-expansion-panels>
        <v-expansion-panel
        v-for="(item,id) in items"
        :key="id"
        >
        <v-expansion-panel-header>{{ item.position }}</v-expansion-panel-header>
        <v-expansion-panel-content>
            <v-card-text>
                <p v-if="item.rank">{{ item.rank }}</p>
                <p style="font-size: 120%">{{item.name}}</p>
                <p style="font-size: 120%">{{item.regal}}</p>
            </v-card-text>
            <!-- <v-img style="margin-top: -20px;" :src="item.image"></v-img> -->
        </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
export default {
    data() {
        return {
            items: [
                {
                    name: 'Ивановский Владимир Сергеевич',
                    rank: 'Генерал-лейтенант',
                    regal: 'Доктор технических наук, профессор, Почетный строитель России, Заслуженный деятель науки Российской Федерации',
                    position: 'Начальник Военного инновационного технополиса «ЭРА»',
                    image: '/images/chieff/Vladimir_Ivanovsky.jpg',
                    data: []
                },
                {
                    name: 'Морозов Андрей Владимирович',
                    rank: 'Полковник',
                    regal: 'Доктор технических наук, профессор',
                    position: 'Заместитель начальника технополиса (по научной и образовательной деятельности)',
                    image: '',
                    data: []
                },
                {
                    name: 'Баранчук Николай Александрович',
                    rank: 'Полковник',
                    regal: 'Доктор педагогических наук',
                    position: 'Заместитель начальника технополиса по военно-политической деятельности',
                    image: '',
                    data: []
                },
                {
                    name: 'ФИСУН Александр Яковлевич',
                    rank: 'Генерал-майор',
                    regal: 'Заслуженный врач Российской Федерации, доктор медицинских наук, профессор, член-корреспондент РАН (2016)',
                    position: 'Заместитель начальника технополиса по медико-биологической деятельности',
                    image: '',
                    data: []
                },
                {
                    name: 'Воронько Дмитрий Васильевич',
                    rank: 'Полковник',
                    regal: 'Кандидат технических наук',
                    position: 'Заместитель начальника технополиса (по материально-техническому обеспечению)',
                    image: '',
                    data: []
                },
                {
                    name: 'НАДТОЧИЙ Ярослав Александрович',
                    regal: 'Кандидат технических наук',
                    position: 'Заместитель начальника технополиса по инновационному развитию',
                    image: '',
                    data: []
                },
            ]
        }
    },

    mounted() {

        if (!this.$store.state.user || Object.keys(this.$store.state.user).length == 0) {
            this.$fire({
                title: "Уведомление",
                text: "Необходимо авторизоваться!",
                type: "error",
            })
            .then(this.$router.push('/howtouse'));
        }

        document.title = 'Технополис "ЭРА" | Руководство';
        this.$emit('update:title', 'Руководство')
    }
}
</script>
