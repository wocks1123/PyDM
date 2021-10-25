import Vue from 'vue'


const values = {
    $serverUrl: "http://mllibra.sogang.ac.kr",
    $serverPort: "53005",
}


export default {
    $serverUrl: "http://mllibra.sogang.ac.kr",
    $serverPort: "53005",
}


export const Constants = {
    install (Vue) {
        for (const m in values) {
            Vue.prototype[m] = values[m];
        }
    }
}

Vue.use(Constants)