<template>
  <div>
    <nav class="navbar ">
      <div class="navbar-brand">
        <a class="navbar-item" href="http://bulma.io">
          <img src="http://bulma.io/images/bulma-logo.png" alt="Bulma: a modern CSS framework based on Flexbox" width="112" height="28">
        </a>
      </div>
  
      <div id="navMenuExample" class="navbar-menu">
        <div class="navbar-start">
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link  is-active" href="/documentation/overview/start/">
              Docs
            </a>
            <div class="navbar-dropdown ">
              <a class="navbar-item " href="/documentation/overview/start/">
                Overview
              </a>
              <a class="navbar-item " href="http://bulma.io/documentation/layout/container/">
                Layout
              </a>
              <hr class="navbar-divider">
              <div class="navbar-item">
                <div>
                  <p class="is-size-6-desktop">
                    <strong class="has-text-info">0.5.0</strong>
                  </p>
                  <small>
                    <a class="view-all-versions" href="/versions">View all versions</a>
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="field is-grouped">
              <p class="control">
                <a class="button is-primary" :href="`/clan/${encodeURIComponent(tag)}.xlsx`">
                  <span class="icon">
                    <i class="fa fa-download"></i>
                  </span>
                  <span>Export</span>
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </nav>
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
            {{ column.now.toLocaleString() }}
            <b v-if="column.delta != 0" :class="{up: column.delta > 0, down: column.delta < 0}">{{ Math.abs(column.delta).toLocaleString() }}</b>
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
    this.fetchData();
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

thead {
  background-color: #00d1b2;

  & th {
    color: #fff;
  }

  & tr:hover {
    background-color: #00d1b2;
  }
}

.up {
  &::before {
    content: '+';
  }
  color: #23d160;
}

.down {
  &::before {
    content: '-';
  }
  color: #ff3860;
}
</style>
