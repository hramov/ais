<template>
    <v-container>
        <v-expansion-panels
            v-model="panel"
            :disabled="disabled"
            multiple
            flat
            tile
        >
            <v-expansion-panel>
                <v-expansion-panel-header>Как войти в систему?</v-expansion-panel-header>
                <v-expansion-panel-content>
                    Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа
                    <v-row align="center" justify="center" style="margin-top: 10px;">
                        <v-img max-width="200" src="https://pro-markirovku.ru/wp-content/uploads/2019/12/pro-markirovku-290.png"></v-img>
                        <!-- <v-img src="../assets/shem_ras.svg"></v-img> -->
                    </v-row>
                </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
                <v-expansion-panel-header>Что такое АИСС?</v-expansion-panel-header>
                <v-expansion-panel-content>
                    Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа
                </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
                <v-expansion-panel-header>Что такое технополис</v-expansion-panel-header>
                <v-expansion-panel-content>
                    Чтобы войти в систему необходимо отсканировать QR код с оборотной стороны бэйджа
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>

<script>
    export default {
        data() {
            return {
                panel: [0],
                disabled: false,
            }
        },

        mounted() {
            document.title = 'Технополис "ЭРА" | Информация';
            this.$emit('update:title', 'Информация')
        }
    }
</script>