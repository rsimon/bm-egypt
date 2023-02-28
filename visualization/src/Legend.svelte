<script>
  import { PALETTE } from './style';
  import { COORDINATE_SOURCES } from './config';
</script>

<div class="legend">
  <ul>
    {#each COORDINATE_SOURCES as source, idx}
      <li>
        <span class="dot" style={`background-color: ${PALETTE[idx]}`}></span> <span class="label">{source}</span>
      </li>
    {/each}
  </ul>
  <p class="hint">
    For places with matches in multiple databases, coordinates are chosen according to the list order.
    First match ({COORDINATE_SOURCES.join(', ')}) defines location.
  </p>
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

  .dot {
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    height: 20px;
    width: 20px;
  }

  p {
    background-color: #efefef;
    border-top: 1px solid #e2e2e2;
    color: #343434;
    font-size: 14px;
    line-height: 150%;
    margin: 0;
    max-width: 40ch;
    padding: 20px;
  }
</style>