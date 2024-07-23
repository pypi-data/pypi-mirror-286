<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import Switch from "@smui/switch";
	import { tick } from "svelte";
	import "./index.less";
	import "./index.css";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let label = "Textbox";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let placeholder = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let interactive: boolean;
	export let rtl = false;
	export let max_height;

	let el: HTMLTextAreaElement | HTMLInputElement;
	const container = true;

	// function handle_change(): void {
	// 	gradio.dispatch("change");
	// 	if (!value_is_output) {
	// 		gradio.dispatch("input");
	// 	}
	// }

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			gradio.dispatch("submit");
		}
	}

	$: if (value === null) value = "";

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value;

	const headers = ["LigandA", "LigandB", "Similarity", "Link", "Mapping"];
	let tableData = [];

	let index = 1;

	const init = () => {
		const { pairs } = JSON.parse(placeholder);
		tableData = [...pairs, ...pairs, ...pairs, ...pairs];
		index++;
	};

	$: placeholder, init();
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
	<div class="fep-pair-container" style={max_height ? `max-height: ${max_height}px` : ''}>
		<table border="1" class="fep-pair-table" id="fep-pair-table-update{index}">
			<tr>
				{#each headers as header}
					<th>{header}</th>
				{/each}
			</tr>
			{#each tableData as data, index}
				<tr>
					<td>{data.ligandA}</td>
					<td>{data.ligandB}</td>
					<td>{data.similarity?.toFixed(3)}</td>
					<td>
						<!-- <KSwitch
							id={`${data.ligandA}-${data.ligandB}-${data.link}`}
							bind:value={data.link}
							on:click={(e) => {
								tableData[index].link = !tableData[index].link;
								value = JSON.stringify({
									res: { ...data, link: tableData[index].link },
									type: "Link",
									index,
								});
							}}
						/> -->
						<Switch
							bind:checked={data.link}
							on:SMUISwitch:change={(e) => {
								value = JSON.stringify({
									res: { ...data, link: tableData[index].link },
									type: "Link",
									index,
								});
								gradio.dispatch("change");
							}}
						/>
					</td>
					<td>
						<button
							on:click={() => {
								value = JSON.stringify({
									res: data,
									type: "Mapping",
									index,
								});
								gradio.dispatch("change");
							}}
						>
							<svg
								width="1em"
								height="1em"
								viewBox="0 0 14 14"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M1.75 5.83398C1.75 3.50065 2.91667 2.33398 5.25 2.33398"
									stroke="#A2A5C4"
									stroke-width="1.3"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-dasharray="2 2"
								/>
								<path
									d="M11.6641 8.75C11.6641 11.0833 10.4974 12.25 8.16406 12.25"
									stroke="#A2A5C4"
									stroke-width="1.3"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-dasharray="2 2"
								/>
								<path
									d="M8.16406 5.25065C8.16406 3.63983 9.46991 2.33398 11.0807 2.33398H12.2474V6.41732H8.16406V5.25065Z"
									stroke="#A2A5C4"
									stroke-width="1.3"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M1.75 8.16602H5.83333V9.33268C5.83333 10.9435 4.52748 12.2493 2.91667 12.2493H1.75V8.16602Z"
									stroke="#A2A5C4"
									stroke-width="1.3"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
						</button>
					</td>
				</tr>
			{/each}
		</table>
	</div>
</Block>

<style>
	label {
		display: block;
		width: 100%;
	}

	input {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	.container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	}
	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}

	.fep-pair-table {
		background: #fff;
		color: #000;
		border-color: #000;
		width: 100%;
		/* overflow: auto; */
		/* display: block; */
	}

	.fep-result-img {
		width: 100px;
		height: 100px;
	}

	tr,
	td {
		border-width: 1px !important;
	}
	td {
		text-align: center;
	}
	.fep-pair-container {
		overflow: auto;
	}
</style>
