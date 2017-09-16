<template>
    <q-layout ref="layout" view="hHr lpr fFf" :class="stolen">
        <q-toolbar slot="header" color="tertiary">
            <q-toolbar-title>
                <span class="text-light">
                    Kradený?
                </span>
            </q-toolbar-title>
        </q-toolbar>
        <div class="row justify-center">
            <div>
                <div class="appIcon">
                    <img src="statics/KradeneBG.png" />
                </div>
            </div>
        </div>
        <div class="row justify-center">
            <div>
                <label class="q-btn row inline flex-center q-focusable q-hoverable relative-position q-btn-rectangle q-btn-big bg-negative text-white">
                    <q-icon name="add_a_photo"></q-icon>&nbsp;<span class="mobile-only"> Vyfoť auto nebo&nbsp;</span>
                    nahraj fotku <input id="selector" type="file" @change="newPicture">
                </label>
            </div>
        </div>
        <div class="row justify-center">

        </div>

        <div class="resultCard row justify-center">
            <div>
                <img :src="imgSrc" id="carImg" class="center"/>
            </div>
                <div id="result" class="center" v-html="result" :class="stolen">

                </div>
        </div>

    </q-layout>
</template>
<script>
    import axios from 'axios'
    import { QLayout, QBtn, QToolbar, QToolbarTitle, QIcon, Alert, Toast } from 'quasar'

    export default {
        data: function () {
            return {
                url: 'http://api.kradeny.cz/upload',
                uploaded: false,
                imgSrc: '',
                stolen: 'neutral',
                newlyFound: false,
                nChecked: 0,
                result: ''
            }
        },
        methods: {
            newPicture: function (event) {
                var file = event.target.files[0]
                this.upload(file)
                this.displayAsImage(file)
            },
            displayAsImage: function(file) {
                var imgURL = URL.createObjectURL(file)
                this.imgSrc = imgURL
                this.stolen = 'neutral'
                this.result = ''
            },
            upload: function (file) {
                var form = new FormData()
                form.append('file', file)
                var vm = this
                Toast.create.info({
                    html: "Nahrávám fotku na server, to může chvíli trvat",
                    timeout: 2500
                })
                axios.post('http://api.kradeny.cz/upload', form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(
                    function (response) {
                        if (response.status === 200) {
                            // console.log(response)
                            vm.runRecognize(response['data'])
                        } else {
                            vm.showError('Nepodařilo se nahrát fotku')
                        }
                    }
                )
                .catch(function () {
                    vm.showError('Nepodařilo se nahrát fotku')
                })
            },
            runRecognize: function (data) {
                Toast.create.info({
                    html: "Rozpoznávám značku, chvilinku to může trvat...",
                    timeout: 2500
                })
                var vm = this
                axios.get('http://api.kradeny.cz/recognize', {params: {filename: data['filename']}})
                .then(
                    function (response) {
                        if (response.status === 200 && response['data']['value'] === 'ok') {
                            var top = Math.min(response['data']['output']['results'][0]['candidates'].length, 2)
                            vm.newlyFound = false
                            vm.nChecked = 0
                            Toast.create.info({
                                html: "Porovnávám značku s policejní databází",
                                timeout: 1500
                            })
                            for (var i = 0; i < top; i++){
                                vm.policeCheck(response['data']['output']['results'][0]['candidates'][i]['plate'])
                                vm.result = vm.result + " " + response['data']['output']['results'][0]['candidates'][i]['plate']
                                // console.log(response['data']['output']['results'][0]['candidates'][i]['plate'])
                            }
                        } else {
                            vm.showError('Nepodařilo se zjistit značku, zkuste jiné foto')
                            vm.stolen = 'unknown'
                        }
                    }
                )
                .catch(function () {
                    vm.showError('Nepodařilo se zjistit značku, zkuste jiné foto')
                    vm.stolen = 'unknown'
                })

            },
            checkFound: function () {
                // console.log('qqq')
                // console.log(this.nChecked)
                if (!this.newlyFound) {
                    if (this.nChecked > 0) {
                        this.stolen = 'ok'
                        this.result = 'Podle všeho je to ok!'
                    } else {
                        this.stolen = 'unknown'
                        this.result = "?"
                        this.showError('Nepodařilo se značky ověřit na Policii')
                    }
                }
            },
            policeCheck: function(plate) {
                var vm = this
                axios.get('http://api.kradeny.cz/policecheck', {
                    params: {spz: plate}
                })
                .then(
                    function (response) {
                        // console.log(response)
                        if (response.status === 200) {
                            vm.nChecked++
                            // console.log(vm.nChecked)
                            if (response['data']['value'] === 'found') {
                                vm.stolen = 'stolen'
                                vm.result = 'Kradený!'
                                vm.newlyFound = true
                            }
                        }
                        vm.checkFound()
                    }
                )
                .catch(function (e) {
                    // Alert.create( {
                    //     html: e
                    // })
                    // console.log(e)
                })
            },
            showError: function (e) {
                Alert.create( {
                    html: e
                })
                // console.log(e)
            }

        },

        components: {
            QLayout,
            QBtn,
            QToolbar,
            QToolbarTitle,
            QIcon,
            Alert
        }
    }
</script>

<style>
    #selector {
        display: none;
    }
    #img-container {
        max-width: 30%;
        max-height: 40%;
    }
    .stolen {
        background-color: red;
    }
    .neutral {
        background-color: white;
    }
    .ok {
        background-color: green;
    }
    .unknown {
        background-color: gray;
    }
    .center {
        text-align: center;
        margin: 0 auto;
        max-width: 50%;
        max-height: 40%;
        /*border: 3px solid green;*/
        margin: 10px;
        border-radius: 10px;
        border: 10px solid #eee;
    }
    .resultCard {
        text-align: center;
    }
    #result {
        border: none;
        background: white;

        position: absolute;
        bottom: 1em;
        font-size: 3em;
        padding: .25em 1em;
        font-weight: bold;
    }
    .appIcon img {
        max-width: 500px;
        height: auto;
        position: relative;
        left: 56px;
    }
</style>
