<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from 'svelte-icons-pack/Icon.svelte';
  import ImCheckboxChecked from 'svelte-icons-pack/im/ImCheckboxChecked';
  import ImCheckboxUnchecked from 'svelte-icons-pack/im/ImCheckboxUnchecked';
  import { PALETTE } from './style';
  import { CSV_FILES } from './config';

  const dispatch = createEventDispatcher();

  let state = CSV_FILES.reduce((s, file) => {
    s[file] = true; 
    return s;
  }, {});

  const format = filename => 
    filename.substring(0, filename.indexOf('.')).replaceAll('_', ' ')

  const toggle = layer => () => {
    const visible = !state[layer];

    state[layer] = visible;

    dispatch('change', { layer, visible })
  }
</script>

<div class="legend by-dataset">
  <ul>
    {#each CSV_FILES as file, idx}
      <li>
        <button on:click={toggle(file)} style={`--color: ${PALETTE[idx]}`}>
          {#if state[file]}
            <Icon src={ImCheckboxChecked} />
          {:else}
            <Icon src={ImCheckboxUnchecked} />
          {/if}
          
          <span class="label">{format(file)}</span>
        </button>
      </li>
    {/each}
  </ul>
</div>

<style>
  .legend {
    background-color: #fff;
    border: 1px solid #e2e2e2;
    border-radius: 3px;
    box-shadow: 2px 2px 28px 0 rgba(0, 0, 0, 0.18);
    font-family: Arial, Helvetica, sans-serif;
    left: 20px;
    position: absolute;
    top: 20px;
  }

  ul {
    list-style-type: none;
    margin: 0;
    padding: 10px 30px 10px 20px;
  }

  li {
    align-items: center;
    display: flex;
    padding: 8px 0;
  }

  button {
    all: unset;
    cursor: pointer;
  }

  .label {
    text-transform: capitalize;
  }

  :global(.legend.by-dataset li svg) {
    font-size: 22px;
    padding-right: 8px;
    vertical-align: text-bottom;
  }

  :global(.legend.by-dataset li svg path) {
    fill: var(--color);
  }
</style>