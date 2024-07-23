<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";
	import graphChart, { emitter, EVENT_NAME } from "./graph-chart";
	import { debounce } from "lodash";
	import "./index.css";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		clear_status: LoadingStatus;
		like: never;
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
	export let load_fn;
	window.process = {
		env: {
			NODE_ENV: "production",
			LANG: "",
		},
	};
	let pairId = 0;

	let el: HTMLTextAreaElement | HTMLInputElement;
	const container = true;

	function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			gradio.dispatch("submit");
		}
	}

	let ligands = new Map();
	const ligandIdToName = new Map();
	$: ligands;

	let pairs = new Map();
	const uniqueIdToSimScore = new Map();
	$: pairs;

	let selectedState = 0;
	$: selectedState;

	let zoomInDisabled = false;
	$: zoomInDisabled;
	let zoomOutDisabled = false;
	$: zoomOutDisabled;

	const deleteLigand = () => {
		const selectedLigand = [...graphChart.ligandGroup.map.values()].filter(
			(item) => item.state.selected,
		);
		ligands.delete(selectedLigand[0].data.name);
		graphChart.resetLigands([...ligands.values()]);
		selectedState = 0;
	};
	const deleteLine = () => {
		const selected = [...graphChart.edgeGroup.map.values()].filter(
			(item) => item.state.selected,
		);
		const uniqueId = selected[0].data.uniqueId;
		if (pairs.has(uniqueId)) {
			pairs.delete(uniqueId);
			const res = [];
			pairs = pairs;
			[...pairs.values()].forEach((item) => {
				res.push({
					ligandA: item.source.name,
					ligandB: item.target.name,
				});
			});
			value = JSON.stringify({ res });
			graphChart.resetEdges([...pairs.values()]);
			selectedState = 0;
		}
	};

	const addLine = () => {
		let idA;
		let idB;
		let source;
		let target;
		let sourceItem;
		let targetItem;
		[...graphChart.ligandGroup.map.values()].forEach((item) => {
			if (item.state.selected) {
				if (item.idx === 1) {
					idA = item.data.id;
					source = item.data;
					sourceItem = item;
				} else {
					idB = item.data.id;
					target = item.data;
					targetItem = item;
				}
			}
		});
		const uniqueId = `${idA}-${idB}`;
		const uniqueId1 = `${idB}-${idA}`;
		if (!pairs.has(uniqueId) && !pairs.has(uniqueId1)) {
			let id = pairIdMap.get(uniqueId) ?? pairIdMap.get(uniqueId1) ?? pairId++
			pairIdMap.set(uniqueId, id)
			pairIdMap.set(uniqueId1, id)
			pairs.set(uniqueId, {
				id,
				uniqueId,
				simScore: uniqueIdToSimScore.get(uniqueId) ?? uniqueIdToSimScore.get(uniqueId1),
				ligandA: source.id,
				ligandB: target.id,
				source,
				target,
			});
			pairs = pairs;
			const res = [];
			[...pairs.values()].forEach((item) => {
				res.push({
					ligandA: item.source.name,
					ligandB: item.target.name,
				});
			});
			value = JSON.stringify({ res });
			graphChart.resetEdges([...pairs.values()]);
			graphChart.events.handler.selector.selectAEdge(sourceItem, targetItem);
			graphChart.events.handler.selector.update();
		}
	};
	const init = () => {
		if (!graphChart.layout) {
			graphChart.init(
				document.getElementById("graph-chart-parent"),
				document.getElementById("graph-chart-dom"),
				false,
			);
			const resizeObserver = new ResizeObserver(
				debounce(() => {
					graphChart.resize();
				}, 1000),
			);
			window.graphChart = graphChart;
			resizeObserver.observe(
				document.getElementById("graph-chart-parent"),
			);

			emitter.on(EVENT_NAME.SELECTOR_CHANGE, (type, selector) => {
				const selectedEdge = [
					...graphChart.edgeGroup.map.values(),
				].filter((item) => item.state.selected);
				const selectedLigand = [
					...graphChart.ligandGroup.map.values(),
				].filter((item) => item.state.selected);
				if (!selectedEdge.length && !selectedLigand.length) {
					selectedState = 0;
					return;
				}
				if (selectedEdge.length) {
					selectedState = 3;
					return;
				}
				if (!selectedEdge.length) {
					selectedState = selectedLigand.length;
					return;
				}
			});
			emitter.on(EVENT_NAME.ZOOM_CHANGE, (scale, minScale, maxScale) => {
				if (scale === minScale) {
					zoomOutDisabled = true;
				} else {
					zoomOutDisabled = false;
				}
				if (scale === maxScale) {
					zoomInDisabled = true;
				} else {
					zoomInDisabled = false;
				}
			});
		}
		handle_data_change();
		return () => graphChart.dispose();
	};

	const interval = setInterval(() => {
		if (document.getElementById("graph-chart-dom")) {
			clearInterval(interval);
			init();
		}
	}, 1000);

	const onZoomOutClick = () => {
		if (zoomOutDisabled) return;
		graphChart.room.zoomOut(-10);
	};

	const onZoomInClick = () => {
		if (zoomInDisabled) return;
		graphChart.room.zoomIn(10);
	};

	let ligandInfoVisible = false;
	$: ligandInfoVisible;
	let ligandInfo = ["name"];

	let pairInfoVisible = false;
	$: pairInfoVisible;
	let pairInfo = ["simScore"];

	let pairIdMap = new Map()

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value, handle_change();

	const handle_data_change = () => {
		if (!graphChart.layout) return;
		setTimeout(() => {
			ligands = new Map();
			const data = JSON.parse(placeholder);
			data.ligands.forEach((item) => {
				const { name } = item;
				if (!ligands.has(name)) {
					ligands.set(name, {
						id: ligands.size,
						...item,
					});
					ligandIdToName.set(ligands.size - 1, name);
				}
			});
			let res = [];
			pairs = new Map();
			data.pairs.forEach((item) => {
				const { ligandA, ligandB, similarity, link } = item;
				const source = ligands.get(ligandA);
				const target = ligands.get(ligandB);
				const uniqueId = `${source.id}-${target.id}`;
				if (link && !pairs.has(uniqueId)) {
					let id = pairIdMap.get(`${source.id}-${target.id}`) ?? pairIdMap.get(`${target.id}-${source.id}`) ?? pairId++
					pairIdMap.set(`${source.id}-${target.id}`, id)
					pairIdMap.set(`${target.id}-${source.id}`, id)
					pairs.set(uniqueId, {
						id,
						uniqueId,
						simScore: similarity,
						ligandA: source.id,
						ligandB: target.id,
						source,
						target,
					});
					res.push({
						ligandA: source.name,
						ligandB: target.name,
					});
				}
				uniqueIdToSimScore.set(uniqueId, similarity);
			});
			// value = JSON.stringify({ res });
			graphChart.resetLigands([...ligands.values()]);
			graphChart.resetEdges([...pairs.values()]);
			setTimeout(() => {
				graphChart.resize();
			}, 200);
		}, 100);
	};
	$: placeholder, handle_data_change();
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
	<div
		id="graph-chart-parent"
		on:click={() => {
			ligandInfoVisible = false;
			pairInfoVisible = false;
		}}
	>
		<div id="graph-chart-dom"></div>
		{#if ligandInfoVisible}
			<form class="ligand-info" on:click={(e) => e.stopPropagation()}>
				<div>
					<input
						type="checkbox"
						name="ligand"
						value="name"
						checked={ligandInfo.includes("name")}
					/>
					Ligand Name
				</div>
				<div>
					<input
						type="checkbox"
						name="ligand"
						value="expDG"
						checked={ligandInfo.includes("expDG")}
					/>
					<span class="base">
						<span>Δ</span>
						<span style="font-style: 'italic'">G</span>
						<span class="subsup">
							<sub class="sub">Exp</sub>
						</span>
					</span>
				</div>
				<div>
					<input
						type="checkbox"
						name="ligand"
						value="predDG"
						checked={ligandInfo.includes("predDG")}
					/>
					<span class="base">
						<span>Δ</span>
						<span style="font-style: 'italic'">G</span>
						<span class="subsup">
							<sub class="sub">FEP</sub>
						</span>
					</span>
				</div>
				<div>
					<input
						type="checkbox"
						name="ligand"
						value="predDGErr"
						checked={ligandInfo.includes("predDGErr")}
					/>
					<span class="base">
						<span>σ(Δ</span>
						<span style="font-style: 'italic'">G</span>
						<span class="subsup">
							<sub class="sub">FEP</sub>
						</span>
					</span>
				</div>
				<button
					class="perturbation-setting-btn"
					on:click={() => {
						emitter.emit(EVENT_NAME.SET_LIGAND_INFOLIST, ["name"]);
						ligandInfoVisible = false;
						ligandInfo = ["name"];
					}}>Reset</button
				>
				<button
					class="perturbation-setting-btn"
					type="button"
					on:click={(e) => {
						const checkboxes = document.querySelectorAll(
							'input[name="ligand"]:checked',
						);
						let selected = [];
						checkboxes.forEach((checkbox) => {
							selected.push(checkbox.value);
						});
						emitter.emit(EVENT_NAME.SET_LIGAND_INFOLIST, selected);
						ligandInfoVisible = false;
						ligandInfo = selected;
					}}>Submit</button
				>
			</form>
		{/if}
		{#if pairInfoVisible}
			<form class="pair-info" on:click={(e) => e.stopPropagation()}>
				<div>
					<input
						type="checkbox"
						name="pair"
						value="simScore"
						checked={pairInfo.includes("simScore")}
					/>
					Similarity
				</div>
				<div>
					<input
						type="checkbox"
						name="pair"
						value="expDDG"
						checked={pairInfo.includes("expDDG")}
					/>
					<span class="base">
						<span>Δ</span>
						<span>Δ</span>
						<span style="font-style: 'italic'">G</span>
						<span class="subsup">
							<sub class="sub">Exp</sub>
						</span>
					</span>
				</div>
				<button
					class="perturbation-setting-btn"
					on:click={() => {
						emitter.emit(EVENT_NAME.SET_EDGE_INFOLIST, [
							"simScore",
						]);
						pairInfoVisible = false;
						pairInfo = ["simScore"];
					}}>Reset</button
				>
				<button
					class="perturbation-setting-btn"
					type="button"
					on:click={(e) => {
						const checkboxes = document.querySelectorAll(
							'input[name="pair"]:checked',
						);
						let selected = [];
						checkboxes.forEach((checkbox) => {
							selected.push(checkbox.value);
						});
						emitter.emit(EVENT_NAME.SET_EDGE_INFOLIST, selected);
						pairInfoVisible = false;
						pairInfo = selected;
					}}>Submit</button
				>
			</form>
			<!-- <div class="pair-info">
				<div>
					<input type="checkbox">
					Similarity
				</div>
				<div>
					<input type="checkbox">
					<span class="base">
						<span>Δ</span>
						<span>Δ</span>
						<span style="font-style: 'italic'">G</span>
						<span class="subsup">
							<sub class="sub">Exp</sub>
						</span>
					</span>
				</div>
			</div> -->
		{/if}
		<div
			class="perturbation_container"
			on:click={(e) => e.stopPropagation()}
		>
			<div class="perturbation_wrapper">
				<!-- Ligand Info -->
				<svg
					class="icon"
					width="1em"
					height="1em"
					viewBox="0 0 20 20"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
					on:click={(e) => {
						e.stopPropagation();
						ligandInfoVisible = !ligandInfoVisible;
						pairInfoVisible = !ligandInfoVisible && pairInfoVisible;
					}}
				>
					<path
						d="M14.5 16.5L15.1451 17.714"
						stroke="#A2A5C4"
						stroke-linecap="round"
					/>
					<path
						d="M2 10L3 10"
						stroke="#A2A5C4"
						stroke-linecap="round"
					/>
					<path
						d="M3.2959 9.66584L5.03523 6.8087C5.10424 6.69532 5.23521 6.625 5.37733 6.625L8.83027 6.625C8.97238 6.625 9.10335 6.69532 9.17236 6.8087L10.9117 9.66584C10.9774 9.77371 10.9774 9.90486 10.9117 10.0127L9.17236 12.8699C9.10335 12.9832 8.97238 13.0536 8.83027 13.0536L5.37733 13.0536C5.23521 13.0536 5.10424 12.9832 5.03523 12.8699L3.2959 10.0127C3.23023 9.90486 3.23023 9.77371 3.2959 9.66584Z"
						stroke="#A2A5C4"
						stroke-width="1.3"
					/>
					<path
						d="M8.76465 13.0408L10.504 10.1837C10.573 10.0703 10.704 10 10.8461 10L14.299 10C14.4411 10 14.5721 10.0703 14.6411 10.1837L16.3804 13.0408C16.4461 13.1487 16.4461 13.2799 16.3804 13.3877L14.6411 16.2449C14.5721 16.3583 14.4411 16.4286 14.299 16.4286L10.8461 16.4286C10.704 16.4286 10.573 16.3583 10.504 16.2449L8.76465 13.3877C8.69898 13.2799 8.69898 13.1487 8.76465 13.0408Z"
						stroke="#A2A5C4"
						stroke-width="1.3"
					/>
					<path
						d="M8.76465 6.61213L10.504 3.75499C10.573 3.64161 10.704 3.57129 10.8461 3.57129L14.299 3.57129C14.4411 3.57129 14.5721 3.64161 14.6411 3.75499L16.3804 6.61213C16.4461 6.72 16.4461 6.85115 16.3804 6.95902L14.6411 9.81616C14.5721 9.92954 14.4411 9.99986 14.299 9.99986L10.8461 9.99986C10.704 9.99986 10.573 9.92954 10.504 9.81616L8.76465 6.95902C8.69898 6.85115 8.69898 6.72 8.76465 6.61213Z"
						stroke="#A2A5C4"
						stroke-width="1.3"
					/>
					<path
						d="M15.7852 2.28613L14.4976 3.81268"
						stroke="#A2A5C4"
						stroke-linecap="round"
					/>
				</svg>
				<!-- Pair Info -->
				<svg
					class="icon"
					width="1em"
					height="1em"
					viewBox="0 0 16 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
					on:click={() => {
						pairInfoVisible = !pairInfoVisible;
						ligandInfoVisible =
							!pairInfoVisible && ligandInfoVisible;
					}}
				>
					<path
						d="M16 0H0V16H16V0Z"
						fill="white"
						fill-opacity="0.01"
					/>
					<path
						d="M12.5404 14.2067L14.2071 12.5401L14.6667 12.9997L14.2071 13.4593L12.5404 11.7926C12.5102 11.7624 12.4833 11.7296 12.4596 11.6941C12.4358 11.6586 12.4158 11.6212 12.3995 11.5817C12.3832 11.5423 12.3708 11.5017 12.3625 11.4598C12.3542 11.418 12.35 11.3757 12.35 11.333C12.35 11.2903 12.3542 11.2481 12.3625 11.2062C12.3708 11.1643 12.3832 11.1237 12.3995 11.0843C12.4158 11.0448 12.4358 11.0074 12.4596 10.9719C12.4833 10.9364 12.5102 10.9036 12.5404 10.8734C12.5706 10.8432 12.6034 10.8163 12.6389 10.7926C12.6744 10.7688 12.7118 10.7488 12.7513 10.7325C12.7907 10.7162 12.8313 10.7038 12.8732 10.6955C12.9151 10.6872 12.9573 10.683 13 10.683C13.0427 10.683 13.085 10.6872 13.1268 10.6955C13.1687 10.7038 13.2093 10.7162 13.2487 10.7325C13.2882 10.7488 13.3256 10.7688 13.3611 10.7926C13.3966 10.8163 13.4294 10.8432 13.4596 10.8734L15.1263 12.5401C15.1565 12.5702 15.1834 12.6031 15.2071 12.6386C15.2308 12.674 15.2509 12.7115 15.2672 12.7509C15.2835 12.7904 15.2959 12.831 15.3042 12.8729C15.3125 12.9147 15.3167 12.957 15.3167 12.9997C15.3167 13.0424 15.3125 13.0846 15.3042 13.1265C15.2959 13.1683 15.2835 13.209 15.2672 13.2484C15.2509 13.2878 15.2308 13.3253 15.2071 13.3608C15.1834 13.3963 15.1565 13.4291 15.1263 13.4593L13.4596 15.126C13.4294 15.1561 13.3966 15.1831 13.3611 15.2068C13.3256 15.2305 13.2882 15.2505 13.2487 15.2669C13.2093 15.2832 13.1687 15.2955 13.1268 15.3038C13.085 15.3122 13.0427 15.3163 13 15.3163C12.9573 15.3163 12.9151 15.3122 12.8732 15.3038C12.8313 15.2955 12.7907 15.2832 12.7513 15.2669C12.7118 15.2505 12.6744 15.2305 12.6389 15.2068C12.6034 15.1831 12.5706 15.1561 12.5404 15.126C12.5102 15.0958 12.4833 15.0629 12.4596 15.0275C12.4358 14.992 12.4158 14.9545 12.3995 14.9151C12.3832 14.8757 12.3708 14.835 12.3625 14.7931C12.3542 14.7513 12.35 14.709 12.35 14.6663C12.35 14.6237 12.3542 14.5814 12.3625 14.5395C12.3708 14.4977 12.3832 14.457 12.3995 14.4176C12.4158 14.3782 12.4358 14.3407 12.4596 14.3052C12.4833 14.2697 12.5102 14.2369 12.5404 14.2067ZM13.65 14.6663C13.65 14.709 13.6458 14.7513 13.6375 14.7931C13.6292 14.835 13.6169 14.8757 13.6005 14.9151C13.5842 14.9545 13.5642 14.992 13.5405 15.0275C13.5167 15.0629 13.4898 15.0958 13.4596 15.126C13.4294 15.1561 13.3966 15.1831 13.3611 15.2068C13.3256 15.2305 13.2882 15.2505 13.2487 15.2669C13.2093 15.2832 13.1687 15.2955 13.1268 15.3038C13.085 15.3122 13.0427 15.3163 13 15.3163C12.9573 15.3163 12.9151 15.3122 12.8732 15.3038C12.8313 15.2955 12.7907 15.2832 12.7513 15.2669C12.7118 15.2505 12.6744 15.2305 12.6389 15.2068C12.6034 15.1831 12.5706 15.1561 12.5404 15.126C12.5102 15.0958 12.4833 15.0629 12.4596 15.0275C12.4358 14.992 12.4158 14.9545 12.3995 14.9151C12.3832 14.8757 12.3708 14.835 12.3625 14.7931C12.3542 14.7513 12.35 14.709 12.35 14.6663C12.35 14.6237 12.3542 14.5814 12.3625 14.5395C12.3708 14.4977 12.3832 14.457 12.3995 14.4176C12.4158 14.3782 12.4358 14.3407 12.4596 14.3052C12.4833 14.2697 12.5102 14.2369 12.5404 14.2067C12.5706 14.1765 12.6034 14.1496 12.6389 14.1259C12.6744 14.1022 12.7118 14.0821 12.7513 14.0658C12.7907 14.0495 12.8313 14.0372 12.8732 14.0288C12.9151 14.0205 12.9573 14.0163 13 14.0163C13.0427 14.0163 13.085 14.0205 13.1268 14.0288C13.1687 14.0372 13.2093 14.0495 13.2487 14.0658C13.2882 14.0821 13.3256 14.1022 13.3611 14.1259C13.3966 14.1496 13.4294 14.1765 13.4596 14.2067C13.4898 14.2369 13.5167 14.2697 13.5405 14.3052C13.5642 14.3407 13.5842 14.3782 13.6005 14.4176C13.6169 14.457 13.6292 14.4977 13.6375 14.5395C13.6458 14.5814 13.65 14.6237 13.65 14.6663ZM13.65 11.333C13.65 11.3757 13.6458 11.418 13.6375 11.4598C13.6292 11.5017 13.6169 11.5423 13.6005 11.5817C13.5842 11.6212 13.5642 11.6586 13.5405 11.6941C13.5167 11.7296 13.4898 11.7624 13.4596 11.7926C13.4294 11.8228 13.3966 11.8497 13.3611 11.8735C13.3256 11.8972 13.2882 11.9172 13.2487 11.9335C13.2093 11.9499 13.1687 11.9622 13.1268 11.9705C13.085 11.9788 13.0427 11.983 13 11.983C12.9573 11.983 12.9151 11.9788 12.8732 11.9705C12.8313 11.9622 12.7907 11.9499 12.7513 11.9335C12.7118 11.9172 12.6744 11.8972 12.6389 11.8735C12.6034 11.8497 12.5706 11.8228 12.5404 11.7926C12.5102 11.7624 12.4833 11.7296 12.4596 11.6941C12.4358 11.6586 12.4158 11.6212 12.3995 11.5817C12.3832 11.5423 12.3708 11.5017 12.3625 11.4598C12.3542 11.418 12.35 11.3757 12.35 11.333C12.35 11.2903 12.3542 11.2481 12.3625 11.2062C12.3708 11.1643 12.3832 11.1237 12.3995 11.0843C12.4158 11.0448 12.4358 11.0074 12.4596 10.9719C12.4833 10.9364 12.5102 10.9036 12.5404 10.8734C12.5706 10.8432 12.6034 10.8163 12.6389 10.7926C12.6744 10.7688 12.7118 10.7488 12.7513 10.7325C12.7907 10.7162 12.8313 10.7038 12.8732 10.6955C12.9151 10.6872 12.9573 10.683 13 10.683C13.0427 10.683 13.085 10.6872 13.1268 10.6955C13.1687 10.7038 13.2093 10.7162 13.2487 10.7325C13.2882 10.7488 13.3256 10.7688 13.3611 10.7926C13.3966 10.8163 13.4294 10.8432 13.4596 10.8734C13.4898 10.9036 13.5167 10.9364 13.5405 10.9719C13.5642 11.0074 13.5842 11.0448 13.6005 11.0843C13.6169 11.1237 13.6292 11.1643 13.6375 11.2062C13.6458 11.2481 13.65 11.2903 13.65 11.333Z"
						fill="#A2A5C4"
					/>
					<path
						d="M1.97813 2.66634C1.97813 2.85503 2.04485 3.01609 2.17828 3.14953C2.31171 3.28296 2.47277 3.34968 2.66146 3.34968C2.85015 3.34968 3.01122 3.28296 3.14465 3.14953C3.27808 3.01609 3.3448 2.85503 3.3448 2.66634C3.3448 2.47764 3.27808 2.31658 3.14465 2.18315C3.01122 2.04972 2.85015 1.98301 2.66146 1.98301C2.47277 1.98301 2.31171 2.04972 2.17827 2.18315C2.04485 2.31658 1.97813 2.47764 1.97813 2.66634ZM0.678131 2.66634C0.678131 2.11866 0.871766 1.65118 1.25904 1.26391C1.64631 0.876641 2.11378 0.683006 2.66146 0.683006C3.20914 0.683006 3.67662 0.876641 4.06389 1.26391C4.45116 1.65118 4.6448 2.11866 4.6448 2.66634C4.6448 3.21402 4.45116 3.68149 4.06389 4.06877C3.67662 4.45604 3.20914 4.64968 2.66146 4.64968C2.11378 4.64968 1.64631 4.45604 1.25903 4.06877C0.871766 3.68149 0.678131 3.21402 0.678131 2.66634Z"
						fill="#A2A5C4"
					/>
					<path
						d="M14.6667 13.6503H9.33334C8.78566 13.6503 8.31819 13.4567 7.93092 13.0694C7.54364 12.6821 7.35001 12.2147 7.35001 11.667V4.00032C7.35001 3.81163 7.28329 3.65057 7.14986 3.51714C7.01643 3.38371 6.85537 3.31699 6.66668 3.31699H4.00001C3.95733 3.31699 3.91506 3.31283 3.8732 3.3045C3.83134 3.29617 3.79069 3.28385 3.75126 3.26751C3.71183 3.25118 3.67437 3.23116 3.63889 3.20745C3.6034 3.18373 3.57057 3.15679 3.54039 3.12661C3.51021 3.09643 3.48326 3.0636 3.45955 3.02811C3.43584 2.99262 3.41582 2.95517 3.39948 2.91573C3.38315 2.8763 3.37082 2.83566 3.3625 2.7938C3.35417 2.75194 3.35001 2.70967 3.35001 2.66699C3.35001 2.62431 3.35417 2.58204 3.3625 2.54018C3.37082 2.49832 3.38315 2.45768 3.39948 2.41825C3.41582 2.37882 3.43584 2.34136 3.45955 2.30587C3.48326 2.27038 3.51021 2.23755 3.54039 2.20737C3.57057 2.17719 3.6034 2.15025 3.63889 2.12654C3.67437 2.10282 3.71183 2.0828 3.75126 2.06647C3.79069 2.05014 3.83134 2.03781 3.8732 2.02948C3.91506 2.02115 3.95733 2.01699 4.00001 2.01699H6.66668C7.21435 2.01699 7.68182 2.21063 8.0691 2.59789C8.45637 2.98517 8.65001 3.45264 8.65001 4.00032V11.667C8.65001 11.8557 8.71672 12.0167 8.85016 12.1502C8.98359 12.2836 9.14465 12.3503 9.33334 12.3503H14.6667C14.7094 12.3503 14.7516 12.3545 14.7935 12.3628C14.8354 12.3711 14.876 12.3835 14.9154 12.3998C14.9549 12.4161 14.9923 12.4362 15.0278 12.4599C15.0633 12.4836 15.0961 12.5105 15.1263 12.5407C15.1565 12.5709 15.1834 12.6037 15.2071 12.6392C15.2308 12.6747 15.2509 12.7121 15.2672 12.7516C15.2835 12.791 15.2959 12.8316 15.3042 12.8735C15.3125 12.9154 15.3167 12.9576 15.3167 13.0003C15.3167 13.043 15.3125 13.0853 15.3042 13.1271C15.2959 13.169 15.2835 13.2096 15.2672 13.2491C15.2509 13.2885 15.2308 13.326 15.2071 13.3615C15.1834 13.397 15.1565 13.4298 15.1263 13.46C15.0961 13.4901 15.0633 13.5171 15.0278 13.5408C14.9923 13.5645 14.9549 13.5846 14.9154 13.6009C14.876 13.6172 14.8354 13.6295 14.7935 13.6378C14.7516 13.6461 14.7094 13.6503 14.6667 13.6503ZM15.3167 13.0003C15.3167 13.043 15.3125 13.0853 15.3042 13.1271C15.2959 13.169 15.2835 13.2096 15.2672 13.2491C15.2509 13.2885 15.2308 13.326 15.2071 13.3615C15.1834 13.397 15.1565 13.4298 15.1263 13.46C15.0961 13.4901 15.0633 13.5171 15.0278 13.5408C14.9923 13.5645 14.9549 13.5846 14.9154 13.6009C14.876 13.6172 14.8354 13.6295 14.7935 13.6378C14.7516 13.6461 14.7094 13.6503 14.6667 13.6503C14.624 13.6503 14.5817 13.6461 14.5399 13.6378C14.498 13.6295 14.4574 13.6172 14.4179 13.6009C14.3785 13.5846 14.341 13.5645 14.3055 13.5408C14.27 13.5171 14.2372 13.4901 14.207 13.46C14.1769 13.4298 14.1499 13.397 14.1262 13.3615C14.1025 13.326 14.0824 13.2885 14.0661 13.2491C14.0498 13.2096 14.0375 13.169 14.0292 13.1271C14.0209 13.0853 14.0167 13.043 14.0167 13.0003C14.0167 12.9576 14.0209 12.9154 14.0292 12.8735C14.0375 12.8316 14.0498 12.791 14.0661 12.7516C14.0824 12.7121 14.1025 12.6747 14.1262 12.6392C14.1499 12.6037 14.1769 12.5709 14.207 12.5407C14.2372 12.5105 14.27 12.4836 14.3055 12.4599C14.341 12.4362 14.3785 12.4161 14.4179 12.3998C14.4574 12.3835 14.498 12.3711 14.5399 12.3628C14.5817 12.3545 14.624 12.3503 14.6667 12.3503C14.7094 12.3503 14.7516 12.3545 14.7935 12.3628C14.8354 12.3711 14.876 12.3835 14.9154 12.3998C14.9549 12.4161 14.9923 12.4362 15.0278 12.4599C15.0633 12.4836 15.0961 12.5105 15.1263 12.5407C15.1565 12.5709 15.1834 12.6037 15.2071 12.6392C15.2308 12.6747 15.2509 12.7121 15.2672 12.7516C15.2835 12.791 15.2959 12.8316 15.3042 12.8735C15.3125 12.9154 15.3167 12.9576 15.3167 13.0003ZM4.65001 2.66699C4.65001 2.70967 4.64584 2.75194 4.63752 2.7938C4.62919 2.83566 4.61686 2.8763 4.60053 2.91573C4.58419 2.95517 4.56417 2.99262 4.54046 3.02811C4.51675 3.0636 4.4898 3.09643 4.45963 3.12661C4.42945 3.15679 4.39661 3.18373 4.36113 3.20745C4.32564 3.23116 4.28818 3.25118 4.24875 3.26751C4.20932 3.28385 4.16867 3.29617 4.12682 3.3045C4.08496 3.31283 4.04269 3.31699 4.00001 3.31699C3.95733 3.31699 3.91506 3.31283 3.8732 3.3045C3.83134 3.29617 3.79069 3.28385 3.75126 3.26751C3.71183 3.25118 3.67437 3.23116 3.63889 3.20745C3.6034 3.18373 3.57057 3.15679 3.54039 3.12661C3.51021 3.09643 3.48326 3.0636 3.45955 3.02811C3.43584 2.99262 3.41582 2.95517 3.39948 2.91573C3.38315 2.8763 3.37082 2.83566 3.3625 2.7938C3.35417 2.75194 3.35001 2.70967 3.35001 2.66699C3.35001 2.62431 3.35417 2.58204 3.3625 2.54018C3.37082 2.49832 3.38315 2.45768 3.39948 2.41825C3.41582 2.37882 3.43584 2.34136 3.45955 2.30587C3.48326 2.27038 3.51021 2.23755 3.54039 2.20737C3.57057 2.17719 3.6034 2.15025 3.63889 2.12654C3.67437 2.10282 3.71183 2.0828 3.75126 2.06647C3.79069 2.05014 3.83134 2.03781 3.8732 2.02948C3.91506 2.02115 3.95733 2.01699 4.00001 2.01699C4.04269 2.01699 4.08496 2.02115 4.12682 2.02948C4.16867 2.03781 4.20932 2.05014 4.24875 2.06647C4.28818 2.0828 4.32564 2.10282 4.36113 2.12654C4.39661 2.15025 4.42945 2.17719 4.45963 2.20737C4.4898 2.23755 4.51675 2.27038 4.54046 2.30587C4.56417 2.34136 4.58419 2.37882 4.60053 2.41825C4.61686 2.45768 4.62919 2.49832 4.63752 2.54018C4.64584 2.58204 4.65001 2.62431 4.65001 2.66699Z"
						fill="#A2A5C4"
					/>
				</svg>
				<!-- ZoomIn -->
				<svg
					class="icon"
					on:click={() => onZoomInClick()}
					width="1em"
					height="1em"
					viewBox="0 0 16 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M7.0026 12.6663C10.1322 12.6663 12.6693 10.1293 12.6693 6.99967C12.6693 3.87007 10.1322 1.33301 7.0026 1.33301C3.873 1.33301 1.33594 3.87007 1.33594 6.99967C1.33594 10.1293 3.873 12.6663 7.0026 12.6663Z"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linejoin="round"
					/>
					<path
						d="M7 5V9"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M5.00781 7.0052L9.00261 7"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M11.0703 11.0742L13.8987 13.9027"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
				<!-- ZoomOut -->
				<svg
					class="icon"
					on:click={() => onZoomOutClick()}
					width="1em"
					height="1em"
					viewBox="0 0 16 16"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M7.0026 12.6663C10.1322 12.6663 12.6693 10.1293 12.6693 6.99967C12.6693 3.87007 10.1322 1.33301 7.0026 1.33301C3.873 1.33301 1.33594 3.87007 1.33594 6.99967C1.33594 10.1293 3.873 12.6663 7.0026 12.6663Z"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M5 7H9"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
					<path
						d="M11.0703 11.0742L13.8987 13.9027"
						stroke="#A2A5C4"
						stroke-width="1.3"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</div>
			{#if selectedState !== 0 && selectedState !== 1}
				<div
					class="perturbation_wrapper"
					on:click={(e) => e.stopPropagation()}
				>
					<!-- Add Edge -->
					{#if selectedState === 2}
						<svg
							class="icon"
							on:click={() => addLine()}
							width="1em"
							height="1em"
							viewBox="0 0 20 20"
							fill="#A2A5C4"
							xmlns="http://www.w3.org/2000/svg"
						>
							<g clip-path="url(#clip0_9307_6332)">
								<path
									d="M2.99626 6.15365L0 13.99H1.37191L2.08531 12.0254H5.36692L6.08032 13.99H7.45223L4.45597 6.15365H2.99626ZM2.46944 10.9718L3.70965 7.53654H3.75355L4.98279 10.9718H2.46944Z"
									fill="#A2A5C4"
								/>
								<path
									d="M12.1465 6V9.09503C11.6745 8.46944 11.1148 8.16213 10.4563 8.16213C9.64412 8.16213 8.99657 8.45847 8.53561 9.05113C8.0966 9.5999 7.88807 10.2913 7.88807 11.1255C7.88807 11.9925 8.10757 12.7059 8.54659 13.2547C9.01852 13.8473 9.67704 14.1437 10.5221 14.1437C11.2685 14.1437 11.8392 13.8912 12.2343 13.3864V13.99H13.3977V6H12.1465ZM10.7526 9.17186C11.1477 9.17186 11.488 9.33649 11.7514 9.66575C12.0367 10.017 12.1904 10.4999 12.1904 11.1035V11.1913C12.1904 11.7401 12.0697 12.201 11.8392 12.5523C11.5758 12.9364 11.1916 13.1339 10.7087 13.1339C10.149 13.1339 9.74289 12.9364 9.49046 12.5413C9.27096 12.212 9.17218 11.7401 9.17218 11.1255C9.17218 10.5108 9.28193 10.0499 9.51241 9.7316C9.77582 9.35844 10.1819 9.17186 10.7526 9.17186Z"
									fill="#A2A5C4"
								/>
								<path
									d="M18.7488 6V9.09503C18.2769 8.46944 17.7171 8.16213 17.0586 8.16213C16.2464 8.16213 15.5989 8.45847 15.1379 9.05113C14.6989 9.5999 14.4904 10.2913 14.4904 11.1255C14.4904 11.9925 14.7099 12.7059 15.1489 13.2547C15.6209 13.8473 16.2794 14.1437 17.1245 14.1437C17.8708 14.1437 18.4415 13.8912 18.8366 13.3864V13.99H20V6H18.7488ZM17.355 9.17186C17.7501 9.17186 18.0903 9.33649 18.3537 9.66575C18.6391 10.017 18.7927 10.4999 18.7927 11.1035V11.1913C18.7927 11.7401 18.672 12.201 18.4415 12.5523C18.1781 12.9364 17.794 13.1339 17.3111 13.1339C16.7513 13.1339 16.3452 12.9364 16.0928 12.5413C15.8733 12.212 15.7745 11.7401 15.7745 11.1255C15.7745 10.5108 15.8843 10.0499 16.1147 9.7316C16.3781 9.35844 16.7842 9.17186 17.355 9.17186Z"
									fill="#A2A5C4"
								/>
							</g>
							<defs>
								<clipPath id="clip0_9307_6332">
									<rect width="20" height="20" fill="white" />
								</clipPath>
							</defs>
						</svg>
					{/if}
					<!-- Delete Edge/Ligand -->
					{#if selectedState === 3}
						<svg
							class="icon"
							on:click={() =>
								// selectedState === 1
								// 	? deleteLigand() :
								deleteLine()}
							width="1em"
							height="1em"
							viewBox="0 0 20 20"
							fill="none"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M2 6.15358V13.9864H4.86326C6.13582 13.9864 7.09024 13.6354 7.74846 12.9333C8.37377 12.2641 8.69191 11.3096 8.69191 10.07C8.69191 8.81938 8.37377 7.86496 7.74846 7.20674C7.09024 6.50464 6.13582 6.15358 4.86326 6.15358H2ZM3.28353 7.25062H4.62191C5.59827 7.25062 6.31135 7.47003 6.76113 7.91981C7.19995 8.35863 7.41935 9.08267 7.41935 10.07C7.41935 11.0354 7.19995 11.7485 6.76113 12.2092C6.31135 12.659 5.59827 12.8894 4.62191 12.8894H3.28353V7.25062Z"
								fill="#A2A5C4"
							/>
							<path
								d="M12.1994 8.16116C11.3547 8.16116 10.6855 8.44639 10.2028 9.02782C9.69819 9.59828 9.45684 10.3004 9.45684 11.1451C9.45684 12.0885 9.72013 12.8236 10.2467 13.3611C10.7404 13.8767 11.4096 14.14 12.2543 14.14C13.0112 14.14 13.6365 13.9206 14.1412 13.4927C14.5361 13.1417 14.7994 12.6919 14.931 12.1653H13.6804C13.5268 12.4835 13.3623 12.7139 13.1758 12.8565C12.9344 13.032 12.6273 13.1198 12.2433 13.1198C11.7935 13.1198 11.4425 12.9771 11.2011 12.7029C10.9598 12.4286 10.8172 12.0227 10.7733 11.4961H15.0188C15.0188 10.4759 14.7884 9.67507 14.3386 9.10461C13.845 8.46833 13.1319 8.16116 12.1994 8.16116ZM12.2323 9.1814C13.11 9.1814 13.6036 9.63119 13.7133 10.5527H10.7952C10.872 10.1029 11.0256 9.76283 11.256 9.53245C11.4973 9.29111 11.8155 9.1814 12.2323 9.1814Z"
								fill="#A2A5C4"
							/>
							<path
								d="M16.12 6V13.9864H17.3707V6H16.12Z"
								fill="#A2A5C4"
							/>
						</svg>
					{/if}
				</div>
			{/if}
		</div>
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
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
		border-radius: 4px;
	}
	.perturbation_container > input {
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
	input:checked {
		background: #6063f0;
	}

	.perturbation-setting-btn {
		border: 0;
	}

	#graph-chart-parent {
		flex-grow: 1;
		flex: 3;
		position: relative;
		overflow: hidden;
		width: 100%;
		height: 100%;
		min-height: 500px;
		background: #f2f5fa;
	}
	#graph-chart-dom {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background-color: #f2f5f9;
	}

	.perturbation_container {
		position: absolute;
		right: 20px;
		top: 32px;
		z-index: 9;
	}

	.perturbation_wrapper {
		background: #ffffff;
		box-shadow:
			0px 6px 10px rgba(183, 192, 231, 0.1),
			0px 8px 12px 1px rgba(170, 181, 223, 0.05);
		border-radius: 4px;
		padding: 0 4px;
		display: flex;
		flex-direction: column;
		margin-bottom: 8px;
	}

	.icon {
		margin-top: 8px;
		margin-bottom: 8px;
		font-size: 16px;
		cursor: pointer;
		color: #a2a5c4 !important;
	}

	.icon.disabled {
		color: #d6d8ef;
	}
	.icon:hover {
		color: #555878 !important;
	}
	.icon:hover.disabled {
		color: #d6d8ef;
		cursor: not-allowed;
	}

	.base {
		display: inline-block !important;
		position: relative;
		white-space: nowrap;
		width: min-content;
		text-indent: 0;
		text-rendering: auto;
		line-height: 1.2;
		font-size: 12px;
	}
	.subsup {
		display: inline-block;
	}
	.sup {
		display: block;
		transform: translateY(-2px) scale(0.7);
	}
	.sub {
		transform: scale(0.7);
		display: block;
	}

	.pair-info {
		position: absolute;
		display: flex;
		flex-direction: column;
		top: 32px;
		right: 48px;
		color: #000000;
		background: #ffffff;
		border-radius: 4px;
		padding: 16px;
		box-shadow:
			0px 6px 10px rgba(183, 192, 231, 0.1),
			0px 8px 12px 1px rgba(170, 181, 223, 0.05);
	}

	.ligand-info {
		position: absolute;
		display: flex;
		flex-direction: column;
		top: 32px;
		right: 48px;
		color: #000000;
		background: #ffffff;
		border-radius: 4px;
		padding: 16px;
		box-shadow:
			0px 6px 10px rgba(183, 192, 231, 0.1),
			0px 8px 12px 1px rgba(170, 181, 223, 0.05);
	}
</style>
