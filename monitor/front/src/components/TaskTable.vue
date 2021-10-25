<template>
  <v-card>
    <v-data-table
        :headers="headers"
        :items="mytask"
        :items-per-page="5"
        class="elevation-1"
    ></v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "TaskTable",
  data () {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Worker Name', value: 'worker_name' },
        { text: 'Parameters', value: 'parameters' },
        { text: 'Result', value: 'result' },
        { text: 'State', value: 'state' },
        { text: 'Start', value: 'start' },
        { text: 'End', value: 'end' },
      ],
      mytask: [
        {
          end: "2021-09-17 00:08:17",
          id: 1,
          parameters: "1,10,13",
          result: "24",
          start: "2021-09-17 00:08:15",
          state: "none",
          worker_name: "worker1",
        },
        {
          end: "2021-09-17 00:08:17",
          id: 2,
          parameters: "2,4,8",
          result: "14",
          start: "2021-09-17 00:08:15",
          state: "none",
          worker_name: "worker1",
        },
        {
          end: "2021-09-17 00:08:17",
          id: 3,
          parameters: "1,1,1,1,1",
          result: "5",
          start: "2021-09-17 00:08:15",
          state: "none",
          worker_name: "worker1",
        },
        {
          end: "2021-09-17 00:08:17",
          id: 4,
          parameters: "3,7",
          result: "10",
          start: "2021-09-17 00:08:15",
          state: "none",
          worker_name: "worker1",
        },
        {
          end: "2021-09-17 00:08:17",
          id: 5,
          parameters: "1,2,3,4,5",
          result: "15",
          start: "2021-09-17 00:08:15",
          state: "none",
          worker_name: "worker1",
        }
      ]
    }
  },
  computed: {
    tasks() {
      return this.$store.state.tasks;
    },
  },

}
</script>

<style scoped>

</style>