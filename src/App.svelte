<script>
  import Router from 'svelte-spa-router'
  import {location} from 'svelte-spa-router'
  import BarcodeSearch from './BarcodeSearch.svelte'
  import NameSearch from './NameSearch.svelte';

  const routes = {
    '/': BarcodeSearch,
    '/names': NameSearch
  }

</script>
{#if $location != '/names'}
<a href="#/names">Name search</a>
{/if}
<Router {routes}/>

<style>
  a {
    color: gray;
    font-weight: 600;
    position: fixed;
    right: 10px;
    top: 10px;
    padding: 5px;
    border: gray solid 1px;
    border-radius: 10px;
  }

  a:hover {
    color:whitesmoke;
    background-color: slategray;
  }
</style>