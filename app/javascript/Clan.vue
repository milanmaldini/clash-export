<template>
  <div>
    <div class="has-text-centered" v-if="loading">Please wait...</div>
    <table class="table is-narrow is-fullwidth is-striped" v-if="clan">
      <thead>
        <tr>
          <th v-for="header in clan[0]">
            {{ header }}
          </th>
        </tr>
      </thead>
      <tfoot>
        <tr>
          <th v-for="header in clan[0]">
            {{ header }}
          </th>
        </tr>
      </tfoot>
      <tbody>
        <tr v-for="row in clan.slice(1)">
          <th>{{ row[0] }}</th>
          <td v-for="column in row.slice(1)">
            {{ column.toLocaleString() }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  props: ['tag'],
  data() {
    return {
      loading: false,
      clan: null,
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const response = await fetch(`/clan/${encodeURIComponent(this.tag)}.json`);
      this.clan = await response.json();
      this.loading = false;
    }
  }
}
</script>

<style scoped>
table {
  font-size: 90%;
}
</style>
