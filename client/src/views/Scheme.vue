<template>
    <v-container>
        <v-card v-for="(item, id) in items" :key="id" style="margin-bottom: 20px;" outlined>
            <v-card-title>
                {{ item.title }}
            </v-card-title>
            <v-card-text>
                <v-img :src="item.url"></v-img>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            items: [
                {
                    title: '1 территория',
                    url: '/images/slide-3.jpg'
                },
                {
                    title: '2 территория',
                    url: '/images/slide-3.jpg'
                }
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
        
        document.title = 'Технополис "ЭРА" | Схемы технополиса';
        this.$emit('update:title', "Схемы технополиса")
    }
}
</script>