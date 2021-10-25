import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex);


export const store = new Vuex.Store({
    state: {
        workers: [],
        tasks: []
    },
    mutations: {

    },
    getters: {
        getWorkerCount: function (state) {
            return state.workers.length;
        },
        getTaskCount: function (state) {
            return state.tasks.length;
        }

    },
    actions: {

    }
});
