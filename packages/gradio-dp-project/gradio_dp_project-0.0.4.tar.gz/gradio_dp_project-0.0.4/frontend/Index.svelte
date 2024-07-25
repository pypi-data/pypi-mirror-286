<script lang="ts">
  import { onMount } from "svelte";
  import type { Gradio } from "@gradio/utils";
  import { Block, BlockTitle } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let value: string | number;
  export let value_is_output = false;
  export let choices: [string, string | number][];
  export let label = "project";
  export let placeholder = "Select a project";
  export let show_label: boolean;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let loading_status: LoadingStatus;
  export let gradio: Gradio<{
    change: string;
    input: never;
    clear_status: LoadingStatus;
  }>;
  export let interactive: boolean;

  // 校验
  let isError = false;
  export let errMsg = 'Please select a project';
  export function validate() {
    isError = !value;
    return isError;
  }

  let cookieMap = new Map;
  function setCookieMap() {
    document.cookie.split(';').forEach(cookie => {
      const [key, value] = cookie.trim().split('=');
      cookieMap.set(key, value);
    });
  }

  const container = true;
  let options: [string, string | number][] = [];
  async function getOptions() {
    const accessKey = cookieMap.get('appAccessKey');
    const xAppKey = cookieMap.get('clientName');
    const res = await fetch('https://openapi.dp.tech/openapi/v1/open/user/project/list', {
      headers: {
        accessKey,
        'x-app-key': xAppKey,
      }
    });

    if (res.ok) {
      const data = await res.json();
      options = data.data.items.map((item: any) => [item.project_name, item.project_id]);
    }
  }

  onMount(() => {
    setCookieMap();
    getOptions();
  });

  function handle_change(): void {
    gradio.dispatch("change");
    if (!value_is_output) {
      gradio.dispatch("input");
    }
  }

  // When the value changes, dispatch the change event via handle_change()
  // See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
  $: value, validate(), handle_change();
</script>

<Block
  {visible}
  {elem_id}
  {elem_classes}
  padding={container}
  allow_overflow={false}
  {scale}
  {min_width}
>
  {#if loading_status}
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...loading_status}
      on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
    />
  {/if}

  <label class:container>
    <BlockTitle {show_label} info={undefined}>{label}</BlockTitle>
    <select placeholder={placeholder} bind:value>
      {#each options as item}
        <option value={item[1]}>{item[0]}</option>
      {/each}
    </select>

    {#if isError}
      <span class="dp_project--error">{errMsg}</span>
    {/if}
  </label>
</Block>

<style>
  select {
    --ring-color: transparent;
    display: block;
    position: relative;
    outline: none !important;
    box-shadow:
      0 0 0 var(--shadow-spread) var(--ring-color),
      var(--shadow-inset);
    border: var(--input-border-width) solid var(--border-color-primary);
    border-radius: var(--radius-lg);
    background-color: var(--input-background-base);
    padding: var(--size-2-5);
    width: 100%;
    color: var(--color-text-body);
    font-size: var(--scale-00);
    line-height: var(--line-sm);
  }

  select:focus {
    --ring-color: var(--color-focus-ring);
    border-color: var(--input-border-color-focus);
  }

  select::placeholder {
    color: var(--color-text-placeholder);
  }

  select[disabled] {
    cursor: not-allowed;
    box-shadow: none;
  }

  .dp_project--error {
    color: #ff4747;
  }
</style>
