<template lang="pug">
  b-container.home
    DataView(ref="dataview")
</template>

<script>
import DataView from '@/components/DataView.vue'

export default {
  name: 'dataview',
  components: {
    DataView
  }
}
</script>
