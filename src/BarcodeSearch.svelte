<script>
    import { onMount } from 'svelte'
    import Grid from "gridjs-svelte"
    import { SvelteToast, toast } from '@zerodevx/svelte-toast'
    import clipboard from 'clipboardy';
    import { Moon } from 'svelte-loading-spinners';
    import { io } from "socket.io-client";
  
    let base_url = '/' 
    if(import.meta.env.DEV) {
      base_url = 'http://localhost:5000/'
    }
  
    
    //check this might have to be set for the different domains
    const socket = io(base_url);
  
    socket.on("connect", () => {
      console.log(`socket connection established with ID ${socket.id}`);
    });
  
    socket.on('disconnect', reason => {
      console.error(`socket disconnected with reason: ${reason}`)
      toast.push('Counter disconnected', {target: 'disconnected'})
    })
  
    socket.io.on('reconnect', _ => {
      console.log('reconnected')
      toast.pop({target: 'disconnected'})
    })
  
    let searching = false
    
    let printCount = 0
  
    socket.on('increment', _ => {
  
      const today = new Date().toISOString().split('T')[0].replace(/-/g,'')
      let currentCount = localStorage.getItem(today)
      if(currentCount) {
        printCount = Number(currentCount) + 1
        localStorage.setItem(today, printCount.toString())
      }
      else {
        printCount = 1
        localStorage.setItem(today, '1')
      }
    })
  
  
    let tableData = []
  
    const toastOptions = {
      duration: 1000 
    }
  
    const search = {
      locality: null,
      collector: null,
      accession: null,
      fieldnumber: null, 
      day: null,
      month: null,
      year: null,
      family: null, 
      country: null, 
      stateProv: null, 
      taxonname: null
    }
  
    const tableColWidths = [
      {width: '20%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'},
      {width: '10%'}
    ]
  
    let countries = []
    let provinces = []
    let families = []
  
    onMount(_ => {
  
      //get the count from localstorage
      const today = new Date().toJSON().slice(0, 10).replace(/-/g,'')
      const count = localStorage.getItem(today)
      if (count) {
        printCount = Number(count)
      }
  
      fetch(base_url + 'countries').then(res => {
        if (res.ok){
          res.json().then(data => countries = data.filter(x=>x).sort())
        }
        else {
          alert(res.statusText)
        }
      })
  
      fetch(base_url + 'provinces').then(res => {
        if (res.ok){
          res.json().then(data => provinces = data.filter(x=>x).sort())
        }
        else {
          alert(res.statusText)
        }
      })
  
      fetch(base_url + 'families').then(res => {
        if (res.ok){
          res.json().then(data => families = data.filter(x=>x).sort())
        }
        else {
          alert(res.statusText)
        }
      })
    })
  
    const getRecords = async _ => {
      if (search.taxonname || search.collector || search.fieldnumber || search.locality || search.accession) {
        let searchStrings = []
        for (let [key, val] of Object.entries(search)){
          if(val) {
            if(typeof val == 'string') {
              val = val.trim()
            }
            if (val) {
              searchStrings.push(key + '=' + encodeURIComponent(val))
            }
          }
        }
    
        if(search.accession || searchStrings.length >= 2) {//requirement for the db
          if(search.country || search.family) {
            if (search.stateProv){
              if(searchStrings.length == 3) {
                alert('at least one more search param is needed')
                return
              }
            }
            if (searchStrings.length == 2){
              alert('at least one more search param is needed')
              return
            }
          }
          const allsearch = searchStrings.join('&')
          searching = true
          tableData = []
          const res = await fetch(base_url + 'search?' + allsearch)
          if (res.ok) {
            const rawData = await res.json()
            tableData = rawData.map(x => {
              const { Barcode, Accession, FieldNumber, FamilyName, Collector, CalcShortCollectionDate, FullName, AcceptedName, Country, MajorAdmin, LocalityNotes } = x
              return {
                barcode: Barcode, 
                accession: Accession, 
                family: FamilyName,
                name: FullName,
                acceptedname: AcceptedName,
                collector: Collector, 
                collnumber: FieldNumber,
                date: CalcShortCollectionDate,
                locality: LocalityNotes
              }
            })
            searching = false
          }
          else {
            console.log('error getting records: ', res.statusText)
          }
        }
        else {
          alert('we need more search params...')
        }
  
      }
      else {
        alert('search needs at least a taxon name, collector, collector number, locality, or accession number')
      }
  
    }
  
    const handleSearchEnter = e => {
      if(e.keyCode === 13){
        getRecords()
      }
    }
  
    const clearForm = _ => {
      for (const key of Object.keys(search)){
        search[key] = null
      }
      tableData = []
    }
  
    const handleRowClick = (...args) => {
      const barcode = args[0].detail[1].cells[0].data.trim()
      clipboard.write(barcode).then(_ => { 
        toast.push('Copied ' + barcode)
      });
    }
  
    const handleFormCopy = ev => {
      const selection = document.getSelection();
      if (selection.toString().length) {
        toast.push('Copied ' + selection)
      }
    }
  
  
  </script>
  
  <svelte:head>
    <title>Barcode Hunter</title>
  </svelte:head>
  
  <main>

    <SvelteToast options={toastOptions}/>
    <div class="counter">
      <span>Print count: {printCount}</span>
    </div>
    <div class="grid">
      <Grid data={tableData} height="400px" className={{table: "table-border"}} on:rowClick={handleRowClick}/>
    </div>
    <div>
      <form on:keypress={handleSearchEnter} on:copy={handleFormCopy}>
        <div>
          <label>accession no.
            <input bind:value={search.accession}/>
          </label>
        </div>
        <div>
          <label>collector
            <input bind:value={search.collector}/>
          </label>
        </div>
        <div>
          <label>collector no.
            <input bind:value={search.fieldnumber}/>
          </label>
        </div>
        <div>
          <label>year
            <input type="number" min="1700" max="2020" bind:value={search.year}/>
          </label>
        </div>
        <div>
          <label>month
            <input type="number" min="1" max="12" bind:value={search.month}/>
          </label>
        </div>
        <div>
          <label>day
            <input type="number" min="1" max="31" bind:value={search.day}/>
          </label>
        </div>
        <div>
          <label>country
            <select style="width:50%" bind:value={search.country}>
              <option value=''></option>
              {#each countries as country }
                <option value={country}>{country}</option>
              {/each}
            </select>
          </label>
        </div>
        <div>
          <label>province
            <select bind:value={search.stateProv} disabled={!search.country || search.country.trim().toLowerCase() != 'south africa'}>
              <option value=''></option>
              {#each provinces as province }
                <option value={province}>{province}</option>
              {/each}
            </select>
          </label>
        </div>
        <div>
          <label>locality
            <input bind:value={search.locality}/>
          </label>
        </div>
        <div/>
        <div>
          <label>family
            <select bind:value={search.family}>
              <option value=''></option>
              {#each families as family }
                <option value={family}>{family}</option>
              {/each}
            </select>
          </label>
        </div>
        <div >
          <label >taxon name
            <input bind:value={search.taxonname}/>
          </label>
        </div>
      </form>
      <br/>
      <button class="searchbutton" on:click={getRecords} disabled={searching}>
        {#if searching}
          <div class="spinner">
            <Moon size="20" color="#FFFFFF" unit="px" duration="1s" />
          </div>
        {:else}
          Search
        {/if}
      </button>
      <br/>
      <br/>
      <button class="clearbutton" on:click={clearForm} disabled={searching}>clear</button>
    </div>
    <div class="bottom-toast">
      <SvelteToast target="disconnected" options={{initial: 0, reversed: true,  intro: { y: 192 }}}/>
    </div>
  </main>
  
  <style>
  
    @import "https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css";

    main {
      max-width: 1280px;
      margin: 0 auto;
      padding: 2rem;
      padding-top:4rem;
      text-align: center;
      display: flex;
      place-items: center;
      flex-direction: column;
      min-width: 320px;
      min-height: 100vh;
    }
  
    .bottom-toast {
      --toastContainerTop: auto;
      --toastContainerRight: auto;
      --toastContainerBottom: 4rem;
      --toastContainerLeft: 4rem;
    }
  
    .table-border {
      border: '3px solid #ccc';
    }
  
    .counter {
      position: fixed;
      left:10px;
      top: 10px;
      background-color: aliceblue;
      border-radius: 4px;
      padding: 4px;
    }
  
    .grid {
      max-height: 500px;
    }
  
    form {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
    }
  
    label {
      display: flex;
      justify-content: right;
      align-items: center;
    }
  
    input, select {
      padding:5px;
      margin: 5px;
      border-radius: 4px;
      border: 1px solid grey;
    }
  
    .searchbutton {
      width: 400px;
      padding:10px;
      color: white;
      background-color: rgb(105, 177, 105);
    }
  
    .searchbutton:hover {
      border: solid 1px black;
    }
  
    .spinner {
      display: inline-block;
      margin: auto;
    }
    
    .clearbutton {
      background-color: lightgray;
    }
  
  
  
  </style>
  