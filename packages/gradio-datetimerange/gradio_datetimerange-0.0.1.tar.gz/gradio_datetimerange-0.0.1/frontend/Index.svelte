<script context="module" lang="ts">
	export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { Block, BlockTitle } from "@gradio/atoms";
	import DateTime from "@gradio/datetime";

	export let gradio: Gradio<{
		change: undefined;
	}>;
	export let label = "Time";
	export let show_label = true;
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: [string, string] = ["", ""];
	let old_value = value;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let include_time = true;
	export let quick_ranges: string[] = [];
	let range_history: [string, string][] = [value];

	$: if (value[0] !== old_value[0] || value[1] !== old_value[1]) {
		old_value = value;
		range_history = [...range_history, value];
	}

	const back_in_history = (): void => {
		range_history.pop();
		const last_range = range_history.pop();
		if (last_range === undefined) {
			value = ["", ""];
			range_history = [];
		} else {
			value = last_range;
			gradio.dispatch("change");
			range_history = [...range_history];
		}
	};
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	<div class="label-content">
		<BlockTitle {show_label} {info}>{label}</BlockTitle>
		{#if show_label}
			<div class="quick-ranges">
				<button
					class="quick-range"
					style:display={range_history.length <= 1 ? "none" : "block"}
					on:click={back_in_history}>Back</button
				>

				{#each quick_ranges as quick_range}
					<button
						class="quick-range"
						on:click={() => {
							value = ["now - " + quick_range, "now"];
						}}>Last {quick_range}</button
					>
				{/each}
			</div>
		{/if}	</div>
	<div class="times">
		<DateTime show_label={false} bind:value={value[0]} {include_time} {gradio} on:gradio></DateTime>
		<DateTime show_label={false} bind:value={value[1]} {include_time} {gradio} on:gradio></DateTime>
	</div>
</Block>

<style>
	.times {
		display: flex;
		gap: 10px;
	}
	.times > :global(.block) {
		margin: 0;
		padding: 0;
	}
	.label-content {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
	}
	.quick-ranges {
		display: inline-flex;
		gap: var(--size-3);
	}
	button {
		color: var(--body-text-color-subdued);
	}
	button:hover {
		color: var(--body-text-color);
	}
</style>
