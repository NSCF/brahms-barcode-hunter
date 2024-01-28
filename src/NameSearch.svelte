<script>
  import clipboard from 'clipboardy';
  import { SvelteToast, toast } from '@zerodevx/svelte-toast'

  let base_url = '/' 
  if(import.meta.env.DEV) {
    base_url = 'http://localhost:5000/'
  }

  let searchText = ''
  let names = []
  let fetching = false

  let timer;
  const debounce = e => {
  clearTimeout(timer);
      timer = setTimeout(() => {
      searchText = e.target.value.trim().replace(/\s+/g, ' ') //just sanitize here, the server adds the asterisks needed
      }, 500);
  }

  const getNames = async _ => {
    if (searchText && searchText.trim() && searchText.trim().split(' ').length > 1) {
      names = []
      fetching = true
      const response = await fetch(base_url + `namesearch?search_string=${searchText}`)
      if (response.ok){
        const json = await response.json()
        fetching = false
        names = json.data.taxonNameSuggestion
      }
      else {
        console.error(response.message)
      }
    }
    else {
      names = []
    }
  }

  // run it
  $: searchText, getNames()

  const toastOptions = {
    duration: 1000 
  }

  const copyName = name => {
    let copyString = Object.values(name).join('\t')
    clipboard.write(copyString).then(_ => { 
      toast.push('Name copied')
    });
  }


</script>

<svelte:head>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
</svelte:head>

<SvelteToast options={toastOptions}/>

<main>
  <h2>Taxon name search</h2>
  <div class="search">
    <div>

      <input placeholder="Add partial taxon names here, e.g. 'wel mir', and press enter.. " on:input={debounce}/>
      <div>
        {#if fetching}
          <p>Fetching names...</p>
        {:else}
          {#each names as name}
          <div class="nameitem">
            <span class="material-symbols-outlined" style="color: gray;" on:click={copyName(name)}>
              content_copy
            </span>
            {name.fullNameStringPlain}</div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
  

</main>


<style>
  @import "https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css";

  main {
    
    width: 100%;

  }

  .search {
    display: flex;
    width: 100%;
    justify-content: center;
  }

  input {
    
    width: 800px;
    padding: 10px;
    border: lightgray solid 1px;
    border-radius: 5px;
    margin-bottom: 1em;
  }

  input:focus {
    outline: rgb(105, 177, 105) solid 3px;
  }

  .nameitem {
    display: flex;
    align-items: center;
    width: 100%;
    font-size: small;
    text-align: left;
    margin-bottom: 1em;
    padding: 10px;
  }

  span {
    cursor: pointer;
  }

  

</style>