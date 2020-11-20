<template>
    <v-expansion-panels>
        <v-expansion-panel
        v-for="(item, id) in items"
        :key="id"
        >
        <v-expansion-panel-header> {{ item.title }} </v-expansion-panel-header>
        <v-expansion-panel-content>
           {{ item.description }}

           <v-card-text>
               Начальник: {{ item.chieff }}
               <v-img :src="item.images.chieff"></v-img>
               <br />
               Сотрудники:
               <v-list-item two-line v-for="(emp, id) in item.employee" :key="id">
                <v-list-item-content>
                    <v-list-item-title>{{ emp.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ emp.position }}</v-list-item-subtitle>
                </v-list-item-content>
                </v-list-item>
           </v-card-text>
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
                    title: 'Военно-политический отдел',
                    description: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
                    employee: [
                        {
                            name: 'Бобров Даниил Русланович',
                            position: 'Бог'
                        }
                    ],
                    chieff: 'п-к Баранчук Н.А.',
                    workTime: 'Всегда',
                    images: {
                        chieff: 'https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTQ3NTI2OTA4NzY5MjE2MTI4/drake_photo_by_prince_williams_wireimage_getty_479503454.jpg',
                        employee: [
                            {
                                name: '',
                                url: ''
                            }
                        ]
                    }
                },
            ]
        }
    },

    mounted() {

        if (Object.keys(this.$store.state.user).length == 0) {
            this.$fire({
                title: "Уведомление",
                text: "Необходимо авторизоваться!",
                type: "error",
            })
            .then(this.$router.push('/'));
        }

        this.$emit('update:title', 'Структура')
        document.title = 'Технополис "ЭРА" | Структура';
    },
}
</script>
