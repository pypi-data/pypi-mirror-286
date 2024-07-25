<script lang="ts">
  import { onMount } from "svelte";
  import type { Gradio } from "@gradio/utils";
  import { Block, BlockTitle } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";

  export let label = "machine";
  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let value: string | number;
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

  // cpu/gpu
  export let machineType: string;
  let machineTypeOptions: string[] = ["CPU", "GPU"];

  let cookieMap = new Map();
  function setCookieMap() {
    document.cookie.split(";").forEach((cookie) => {
      const [key, value] = cookie.trim().split("=");
      cookieMap.set(key, value);
    });
  }

  // 机型
  let cpuList: [string, number][] = [];
  let gpuList: [string, number][] = [];
  let machineList: [string, number][] = [];
  async function getMachines() {
    const accessKey = cookieMap.get('appAccessKey');
    const xAppKey = cookieMap.get('clientName');
    const req = (type) =>
      fetch(
        `https://openapi.dp.tech/openapi/v1/open/sku/list?chooseType=${type}`,
        {
          headers: {
            accessKey,
            "x-app-key": xAppKey,
          },
        }
      );

    const [cpuRes, gpuRes] = await Promise.all([req("cpu"), req("gpu")]);
    const resolve = async (res, isCpu: boolean) => {
      if (res.ok) {
        const data = await res.json();
        const list = data.data.items.map((machine) => [
          machine.skuName,
          machine.skuId,
        ]);
        if (isCpu) {
          cpuList = list;
        } else {
          gpuList = list;
        }
      }
    };
    resolve(cpuRes, true);
    resolve(gpuRes, false);
  }
  onMount(() => {
    setCookieMap();
    getMachines();
  });

  // 校验
  let isError = false;
  export let errMsg = "Please select a machine";
  export function validate() {
    isError = !value;
    return isError;
  }

  // 联动
  $: if (machineType === "CPU") {
    machineList = cpuList;
  } else {
    machineList = gpuList;
  }
  $: machineType, (value = undefined), handle_change();

  function handle_change(): void {
    gradio.dispatch("change");
  }

  // When the value changes, dispatch the change event via handle_change()
  // See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
  $: value, validate(), handle_change();
</script>

<Block
  {visible}
  {elem_id}
  {elem_classes}
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

  <div>
    <BlockTitle {show_label} info={undefined}>{label}</BlockTitle>
    <select
      class="dp_machine-type"
      bind:value={machineType}
    >
      {#each machineTypeOptions as item}
        <option>{item}</option>
      {/each}
    </select>
    <div class="dp_machine-container">
      <select class="dp_machine-sku" bind:value>
        {#each machineList as item}
          <option value={item[1]}>{item[0]}</option>
        {/each}
      </select>
      {#if isError}
        <div class="dp_machine--error">{errMsg}</div>
      {/if}
    </div>
  </div>
</Block>

<style>
  .dp_machine-container {
    display: inline-block;
    vertical-align: top;
  }

  .dp_machine-type {
    width: 80px;
    margin-left: 8px;
    margin-right: 8px;
  }

  .dp_machine-sku {
    width: 220px;
  }

  .dp_machine--error {
    color: #ff4747;
  }

  select {
    --ring-color: transparent;
    display: inline-block;
    position: relative;
    outline: none !important;
    box-shadow:
      0 0 0 var(--shadow-spread) var(--ring-color),
      var(--shadow-inset);
    border: var(--input-border-width) solid var(--border-color-primary);
    border-radius: var(--radius-lg);
    background-color: var(--input-background-base);
    padding: var(--size-2-5);
    /* width: 100%; */
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
</style>
