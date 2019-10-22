import axios from 'axios'

export function getEnvdata(url, params, callback, failure) {
  axios.get(url, { params: params }).then((response) => {
    var ret = response.data
    if (ret.status) {
      var data = {
        temp: [],
        pres: [],
        humd: [],
        labels: []
      }
      ret.data.forEach((d) => {
        data.temp.push(d.temp)
        data.pres.push(d.pres)
        data.humd.push(d.humd)
        data.labels.push(d.date.short)
      })
      ret.parsed = data
    }
    callback(ret)
  }).catch(failure)
}
