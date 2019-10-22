<template lang="pug">
  .dataView
    b-form.mb-3(@submit.prevent="getData")
      b-form-group(label="file: ")
        b-form-select(v-model="form.file", :options="filelist", required)
      b-form-group(label="hours: ")
        b-form-input(v-model="form.hours", type="number")
      b-button(type="submit", variant="primary") Refresh
    .tempdata
      graph.graph.tg(:chart-data="tempdata", :options="options")
    .presdata
      graph.graph.pg(:chart-data="presdata", :options="options")
    .humddata
      graph.graph.hg(:chart-data="humddata", :options="options")
</template>

<script>
import Graph from '@/components/Graph.js'
import { getEnvdata } from '@/envdata.js'

export default {
  name: 'DataView',
  components: {
    Graph
  },
  data() {
    return {
      form: {
        file: 'envdata.bin',
        hours: 6
      },
      filelist: [],
      tempdata: null,
      presdata: null,
      humddata: null,
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  methods: {
    getInfo() {
      this.$axios.get('/envdata/api/v1/info').then((response) => {
        if (response.data.status) {
          this.filelist = response.data.files
        }
      }).catch((error) => {
        window.alert(String(error))
      })
    },
    getData() {
      getEnvdata('/envdata/api/v1/data/' + this.form.file + '/latest', {
        hours: this.form.hours
      }, (res) => {
        if (res.status) {
          this.tempdata = {
            labels: res.parsed.labels,
            datasets: [{
              label: 'Temperature',
              borderColor: '#50c896',
              fill: false,
              lineTension: 0,
              data: res.parsed.temp
            }]
          }
          this.presdata = {
            labels: res.parsed.labels,
            datasets: [{
              label: 'Pressure',
              borderColor: '#c8c83c',
              fill: false,
              lineTension: 0,
              data: res.parsed.pres
            }]
          }
          this.humddata = {
            labels: res.parsed.labels,
            datasets: [{
              label: 'Humidity',
              borderColor: '#5096c8',
              fill: false,
              lineTension: 0,
              data: res.parsed.humd
            }]
          }
        } else {
          window.alert(res.message)
        }
      }, (error) => {
        window.alert(String(error))
      })
    }
  },
  mounted() {
    this.getInfo()
    this.getData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  .graph {
    height: 50%;
    position: relative;
    //float: left;
  }
</style>
