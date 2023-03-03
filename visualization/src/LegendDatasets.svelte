<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from 'svelte-icons-pack/Icon.svelte';
  import IoCheckbox from 'svelte-icons-pack/io/IoCheckbox';
  import IoCheckboxOutline from 'svelte-icons-pack/io/IoCheckboxOutline';
  import { PALETTE } from './style';
  import { CSV_FILES } from './config';

  const dispatch = createEventDispatcher();

  let state = CSV_FILES.reduce((s, file) => {
    s[file] = true; 
    return s;
  }, {});

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
        <button on:click={toggle(file)}>
          {#if state[file]}
            <Icon color={PALETTE[idx]} src={IoCheckbox} />
          {:else}
            <Icon color={PALETTE[idx]} src={IoCheckboxOutline} />
          {/if}
        </button>

        <span class="label">{file}</span>
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

  :global(.legend.by-dataset li svg) {
    font-size: 24px;
    padding-right: 8px;
    vertical-align: text-bottom;
  }
</style>