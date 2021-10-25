<template>
  <v-card
    color="black"
  >
    <v-container>
      <v-layout row wrap>
        <v-flex class="pa-2" xs12 sm12 md4>
          <v-card>
            <v-container pa-3>
              <v-layout row>
                <v-flex>
                  <v-card-title primary-title>
                    <v-avatar>
                      <v-icon large color="success">mdi-server-network</v-icon>
                    </v-avatar>
                  </v-card-title>
                </v-flex>
                <v-spacer></v-spacer>
                <v-flex>
                  <v-card-title primary-title>
                    <div class="text-right">
                      <div class="grey--text">워커 수</div>
                      <h3 class="headline">{{getTaskCount}}대</h3>
                    </div>
                  </v-card-title>
                </v-flex>

              </v-layout>
              <v-divider light></v-divider>
              <v-card-actions class="pa-2">
                <v-icon small color="primary">update</v-icon>
                <span class="grey--text caption font-italic">&nbsp;</span>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-container>
          </v-card>
        </v-flex>

        <v-flex class="pa-2" xs12 sm12 md4>
          <v-card>
            <v-container pa-3>
              <v-layout row>
                <v-flex>
                  <v-card-title primary-title>
                    <v-avatar>
                      <v-icon large color="success">mdi-run</v-icon>
                    </v-avatar>
                  </v-card-title>
                </v-flex>
                <v-spacer></v-spacer>
                <v-flex>
                  <v-card-title primary-title>
                    <div class="text-right">
                      <div class="grey--text">처리 중</div>
                      <h3 class="headline">0개</h3>
                    </div>
                  </v-card-title>
                </v-flex>

              </v-layout>
              <v-divider light></v-divider>
              <v-card-actions class="pa-2">
                <v-icon small color="primary">update</v-icon>
                <span class="grey--text caption font-italic">&nbsp;</span>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-container>
          </v-card>
        </v-flex>

        <v-flex class="pa-2" xs12 sm12 md4>
          <v-card>
            <v-container pa-3>
              <v-layout row>
                <v-flex>
                  <v-card-title primary-title>
                    <v-avatar>
                      <v-icon large color="success">mdi-comment-question</v-icon>
                    </v-avatar>
                  </v-card-title>
                </v-flex>
                <v-spacer></v-spacer>
                <v-flex>
                  <v-card-title primary-title>
                    <div class="text-right">
                      <div class="grey--text">태스크</div>
                      <h3 class="headline">총 5개</h3>
                    </div>
                  </v-card-title>
                </v-flex>

              </v-layout>
              <v-divider light></v-divider>
              <v-card-actions class="pa-2">
                <v-icon small color="primary">update</v-icon>
                <span class="grey--text caption font-italic">&nbsp;  </span>
<!--                <v-spacer></v-spacer>-->
<!--                <v-btn x-small> 수정 </v-btn>-->
              </v-card-actions>
            </v-container>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "InformationComp",
  computed: {
    getWorkerCount() {
      return this.$store.getters.getWorkerCount;
    },
    getTaskCount() {
      return this.$store.getters.getTaskCount;
    },
  },
  methods: {

  }
}
</script>

<style scoped>

</style>