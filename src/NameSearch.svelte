<script>
  import { onMount } from 'svelte';
  import clipboard from 'clipboardy';
  import { SvelteToast, toast } from '@zerodevx/svelte-toast'

  let base_url = '/' 
  if(import.meta.env.DEV) {
    base_url = 'http://localhost:5000/'
  }

  let searchInput
  let searchText = ''
  let source
  let names = []
  let fetching = false
  let error = false
  let copyNameOnly = false

  let bodatsaextractdate = null

  onMount(async _ => {

    const response = await fetch(base_url + `bodatsaextractdate`)
      if (response.ok){
        const data = await response.json()
        if (data.length) {
          bodatsaextractdate = data[0].value
        }
      }
      else {
        error = true
        console.error(response.message)
      }

  })

  let timer;
  const debounce = e => {
  clearTimeout(timer);
      timer = setTimeout(() => {
      searchText = e.target.value.trim().replace(/\s+/g, ' ') //just sanitize here, the server adds the asterisks needed
      }, 500);
  }

  const getNames = async _ => {
    if (searchText && searchText.trim() && searchText.trim().split(' ').length > 1) {
      error = false
      names = []
      fetching = true
      const response = await fetch(base_url + `namesearch?search_string=${searchText}&source=${source}`)
      if (response.ok){
        names = await response.json()
        console.log(names[0])
        fetching = false
      }
      else {
        error = true
        fetching = false
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
    
    let values = [
      name.fullName,
      name.source,
      
    ]

    if (!copyNameOnly) {
      values = [...values, name.identifier, name.status, name.acceptedName]
    }
    
    let copyString = values.join('\t').trim()

    clipboard.write(copyString).then(_ => { 
      toast.push('Name copied')
    });
    
  }

  const clear = _ => {
    source = "SANBI"
    searchText = ''
    searchInput.value = ''
  }

</script>

<svelte:head>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
</svelte:head>

<SvelteToast options={toastOptions}/>

<main>
  <h2>Taxon name search</h2>
  {#if bodatsaextractdate}
  <p class="extractdate">SANBI checklist date: {bodatsaextractdate}</p>
  {/if}
  <div class="search">
    <div class="fields">
      <div style="display:flex; justify-content:flex-end;">
        <div>
          <input type="checkbox" id="names-only" style="width:fit-content;"  bind:value={copyNameOnly}>
          <label for="names-only">copy name only</label><br>
        </div>
      </div>
      <div style="position:relative;">
        <select bind:value={source} on:change={getNames}>
          <option value="SANBI">SANBI</option>
          <option value="WFO">WFO</option>
        </select>
        <input placeholder="Add partial taxon names here, e.g. 'wel mir', and press enter.. " on:input={debounce} bind:this={searchInput}/>
        <span class="material-symbols-outlined refresh" on:click={clear}>
          refresh
          </span>
        <div>
      </div>
        {#if fetching}
          <p>Fetching names...</p>
        {:else if error}
          <p>Oops, something went wrong, please see the console</p>
        {:else if names.length}
          {#each names as name}
          <div class="nameitem">
            <span class="material-symbols-outlined" style="color: gray;" on:click={copyName(name)}>
              content_copy
            </span>
            {name.fullName}</div>
          {/each}
        {:else}
          <p>No names found</p>
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

  h2 {
    margin-bottom: 0;
  }

  .extractdate {
    font-size: 0.8em;
    margin-top: 0;
    margin-bottom:3em;
  }

  .search {
    display: flex;
    width: 100%;
    justify-content: center;
  }

  .fields {
    position: relative;
  }

  .refresh {
    position: absolute;
    top: 7px;
    right: 5px;
    color: gray; 
    transform: scaleX(-1);
  }

  input {
    width: 400px;
  }
  
  select {
    width: 150px;
  }

  input, select {   
    padding: 10px;
    border: lightgray solid 1px;
    border-radius: 5px;
    margin-bottom: 1em;
  }

  input:focus, select:focus {
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