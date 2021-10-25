<template>
  <v-app>
    <span class="bg"></span>
    <v-main app>
      <main-page></main-page>
    </v-main>
  </v-app>
</template>

<script>
import MainPage from "@/components/MainPage";


export default {
  name: 'App',

  components: {
    MainPage
  },

  data: () => ({
    //
  }),
  mounted() {
    const host = "http://mllibra.sogang.ac.kr:53005";
    this.$get(
        host + "/workers"
    ).then((response) => {
      console.log("/workers[GET] response", response.data);
      this.$store.state.workers = response.data;
    }).catch((ex) => {
      console.log("AXIOS ERR : ", ex)
    });

    this.$get(
        host + "/tasks"
    ).then((response) => {
      console.log("/tasks response", response);
      this.$store.state.tasks = response;
    }).catch((ex) => {
      console.log("AXIOS ERR : ", ex)
    });

    //////////////////////////////////////////////////////////////////////////////
    // 실시간 갱신
    this.$socket.on("TASK", (data) => {
      console.log("Task data", data);
    });
    this.$socket.on("TASK_START", (data) => {
      console.log("TASK_START data", data);
      this.$store.commit("updateRunningListState", data);
    });
    this.$socket.on("TASK_END", (data) => {
      console.log("RESULT_UPDATE data", data);
      this.$store.commit("addResult", data);
    });

    this.$socket.on("MONITOR_INIT", (data) => {
      console.log("MONITOR_INIT", data);
    });
    this.$socket.on("INSERT", (data) => {
      console.log("INSERT", data);
    });
    this.$socket.on("UPDATE", (data) => {
      console.log("UPDATE", data);
    });
    this.$socket.on("DELETE", (data) => {
      console.log("DELETE", data);
    });

  }
};
</script>

<style>
.bg {
  width: 100%;
  height: 32.5%;
  position: absolute;
  top: 0;
  left: 0;
  background-size: cover;
  background-color: #c1d5e0;
  transform: scale(1.1);
}
</style>