<template>
    <div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'
import {mapGetters} from 'vuex'
import axios from 'axios'
    export default {
        components: {
        },
        data() {
            return {
            }
        },
        async created() {
            this.$emit('update:title', 'Кабинет')
            if (!localStorage.getItem('user')) {

                await axios.get(this.$store.state.getUrl + 'api/auth/' + this.$route.params.id)
                    .then(resp => {
                        if (resp.data) {
                            resp.data.isLoggedIn = true
                            localStorage.setItem('user', JSON.stringify(resp.data))
                            this.$store.commit('add_user', resp.data)
                        }
                    })
                    .catch(err => {
                        console.log(err)
                        localStorage.removeItem('user')
                    })

                await this.$store.dispatch('login', this.$route.params.id)
                // this.$fire({
                //     title: "Уведомление",
                //     text: "Добро пожаловать, " + this.getUser.name + " " + this.getUser.second_name,
                //     type: "success",
                //     timer: 2000
                // });

                Swal.fire({
                    title: '<strong>Добро пожаловать, <p>' + this.getUser.name + ' ' + this.getUser.second_name + '</p></strong>',
                    imageUrl: './images/logo.png',
                    imageHeight: 200,
                    imageAlt: 'Логотип',
                    timer: 2500,
                    showConfirmButton: false,
                })
            }
            this.$router.push('/')
        },
        computed: {
            ...mapGetters(['getUser', 'getRecentEvents']),
        }
    }
</script>

<style scoped>
    .initials {display: block; margin: 0 auto; line-height: 72px;}
    @media (max-width: 600px) {
        .text {text-align: center;}
    }
</style>
