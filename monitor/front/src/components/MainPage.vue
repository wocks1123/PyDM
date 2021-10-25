<template>
  <v-container
      class="pa-0"
  >
    <v-card>
      <v-toolbar
          color="black"
          dark
      >
<!--        <v-app-bar-nav-icon></v-app-bar-nav-icon>-->

        <v-toolbar-title> PyDM </v-toolbar-title>

      </v-toolbar>
      <v-card
          color="black"
          class="rounded-0"
      >
        <information-comp></information-comp>
      </v-card>

      <v-tabs
          v-model="tabs"
          centered
          grow
          dark
      >
        <v-tab>검출 결과</v-tab>
        <v-tab>벤치마크</v-tab>
      </v-tabs>

      <v-tabs-items v-model="tabs">
        <v-tab-item>
          <v-card>
            <task-table></task-table>
          </v-card>
        </v-tab-item>
        <v-tab-item>
          <worker-table></worker-table>
        </v-tab-item>
<!--        <v-tab-item>-->
<!--          <worker-monitor-view></worker-monitor-view>-->
<!--        </v-tab-item>-->
        <!--        <v-tab-item>-->
        <!--          <worker-list></worker-list>-->
        <!--        </v-tab-item>-->
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
import InformationComp from "@/components/InformationComp";
import TaskTable from "@/components/TaskTable";
import WorkerTable from "@/components/WorkerTable";


export default {
  name: "MainPage",
  components: {InformationComp, TaskTable, WorkerTable},
  data() {
    return {
      tabs: null,
    }
  },
}
</script>

<style scoped>

</style>