<template>
  <div>
    <div class="has-text-centered" v-if="loading">Please wait...</div>
    <table class="table is-narrow is-fullwidth is-striped" v-if="!loading">
      <thead>
        <tr>
          <th v-for="header in header">
            {{ header }}
          </th>
        </tr>
      </thead>
      <tfoot>
        <tr>
          <th v-for="header in header">
            {{ header }}
          </th>
        </tr>
      </tfoot>
      <tbody>
        <tr v-for="row in tableData">
          <th>{{ row.name }}</th>
          <td v-for="column in row.data">
            {{ column.now.toLocaleString() }} ({{ column.delta }})
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import zip from 'lodash/zip'

export default {
  props: ['tag'],
  data() {
    return {
      loading: false,
      clan: null,
      previousData: null,
    }
  },
  created() {
    this.fetchData()
  },
  computed: {
    tableData() {
      const clanRows = this.clan.slice(1);

      // Map by user -> columns      
      const previousPlayers = {};
      this.previousData.slice(1).forEach(row => {
        const [name, ...columns] = row;
        previousPlayers[name] = columns;
      });

      return clanRows.map(row => {
        const [name, ...columns] = row;
        const previousColumns = previousPlayers[name]; // look up by player name

        const zippedRow = zip(columns, previousColumns);
        const data = zippedRow.map(item => {
          const [now, previous] = item;

          return { now, delta: now - previous, previous };
        });

        return { name, data };
      });
    },
    header() {
      return this.clan[0];
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const nowPromise = fetch(`/clan/${encodeURIComponent(this.tag)}.json`);
      const previousPromise = fetch(`/clan/${encodeURIComponent(this.tag)}.json?daysAgo=${3}`);

      const nowResponse = await nowPromise;
      const previousResponse = await previousPromise;

      this.clan = await nowResponse.json();
      this.previousData = await previousResponse.json();

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
