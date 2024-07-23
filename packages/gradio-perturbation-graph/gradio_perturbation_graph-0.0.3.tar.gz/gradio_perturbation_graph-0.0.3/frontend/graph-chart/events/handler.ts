import { ElementEvent } from 'zrender';

import {
    Selector,
    hoverLigand,
    hoverEdge,
    hoverHistory,
    relatedHoverLigand,
    relatedHoverEdge,
    relatedHoverHistory,
    fateoutElement,
    fadeoutElement,
} from './collection';
import { GraphChart } from '../chart';
import { LigandGroup, EdgeGroup, HistoryGroup } from '../group';
import { Element, EdgeElement, LigandElement, EdgeElementProps, LigandElementProps } from '../element';
import Layout from '../layout';
import Vector from '../layout/vector';
import { HistoryElement, HistoryElementProps } from '../element/history';
import { FEPPair } from '../type';
import emitter, { EVENT_NAME } from './emitter';

class EventsHandler {
    layout: Layout;
    ligandGroup!: LigandGroup;
    edgeGroup!: EdgeGroup;
    historyGroup!: HistoryGroup;
    selector!: Selector;
    hoverEl: Element | null = null;
    historyForce: boolean;

    onClear() {
        this.selector.clear();
    }

    onClick(ev: ElementEvent) {
        if (ev.target) return;
        this.selector.clear();
    }

    onMouseDown(ev: ElementEvent) {
        if (ev.target) return;
        const room = this.ctx.room;
        let { pageX: startX, pageY: startY } = ev.event as MouseEvent;
        const mousemove = (ev: MouseEvent) => {
            const { pageX: endX, pageY: endY } = ev;
            const disX = startX - endX;
            const disY = startY - endY;
            room.move(disX, disY);
            startX = endX;
            startY = endY;
        };
        const mouseup = () => {
            document.removeEventListener('mousemove', mousemove);
            document.removeEventListener('mouseup', mouseup);
        };
        document.addEventListener('mousemove', mousemove);
        document.addEventListener('mouseup', mouseup);
    }

    onMouseWheel(ev: ElementEvent) {
        const { event, wheelDelta } = ev;
        const room = this.ctx.room;
        event.preventDefault();
        if (wheelDelta > 0) {
            room.zoomIn(wheelDelta);
        } else {
            room.zoomOut(wheelDelta);
        }
    }

    onMouseOver(el: Element) {
        this.hoverEl = el;
        hoverEdge.forEach(edge => edge?.onHover());
        hoverHistory.forEach(history => history?.onHover());
        fadeoutElement.forEach(edge => edge?.fadeout());
        relatedHoverEdge.forEach(edge => edge?.onRelatedHover());
        relatedHoverHistory.forEach(history => history?.onRelatedHover());
        hoverLigand.forEach(ligand => ligand?.onHover());
        fateoutElement.forEach(ligand => ligand?.fadeout());
        relatedHoverLigand.forEach(ligand => ligand?.onRelatedHover());
    }

    onMouseOut() {
        this.hoverEl = null;
        hoverEdge.forEach(edge => edge?.onHoverEnd());
        hoverHistory.forEach(history => history?.onHoverEnd());
        fadeoutElement.forEach(edge => edge?.fadein());
        relatedHoverEdge.forEach(edge => edge?.onRelatedHoverEnd());
        relatedHoverHistory.forEach(history => history?.onRelatedHoverEnd());
        hoverLigand.forEach(ligand => ligand?.onHoverEnd());
        fateoutElement.forEach(ligand => ligand?.fadein());
        relatedHoverLigand.forEach(ligand => ligand?.onRelatedHoverEnd());
        hoverLigand.clear();
        fateoutElement.clear();
        relatedHoverLigand.clear();
        hoverEdge.clear();
        hoverHistory.clear();
        fadeoutElement.clear();
        relatedHoverEdge.clear();
        relatedHoverHistory.clear();
    }
    onLigandMouseDown(ligand: LigandElement, ev: ElementEvent, callBack?: () => void) {
        if (ligand.type === 'ligand') {
            let { pageX: startX, pageY: startY } = ev.event as MouseEvent;
            const mousemove = (ev: MouseEvent) => {
                const { pageX: endX, pageY: endY } = ev;
                const { x: posX, y: posY} = ligand.position
                const disX = (startX - endX) / this.layout.room.scale;
                const disY = (startY - endY) / this.layout.room.scale;
                const pos = new Vector(posX - disX, posY - disY)
                this.layout.graph.vertices[ligand.id].pos = pos;
                this.ligandGroup.map.get(`${ligand.id}`)?.moveTo(pos);
                this.edgeGroup.forEach((edge, id) => {
                    if (ligand.edgeMap.has(id)) {
                        edge?.reDraw();
                    }
                });
                this.historyGroup.forEach((history, id) => {
                    if (ligand.historyMap.has(id)) {
                        history?.reDraw();
                    }
                });
                startX = endX;
                startY = endY;
                this.layout.graph.isUpdate = true;
            };
            const mouseup = () => {
                callBack && callBack();
                document.removeEventListener('mousemove', mousemove);
                document.removeEventListener('mouseup', mouseup);
            };
            document.addEventListener('mousemove', mousemove);
            document.addEventListener('mouseup', mouseup);
            return;
        }
        callBack && callBack();
    }
    onLigandMouseOver(ligand: LigandElement) {
        if (this.hoverEl === ligand) return;
        if (ligand.state.firstAdd) {
            ligand.state.firstAdd = false;
        }
        hoverLigand.add(ligand);
        this.ligandGroup.forEach(item => {
            if (ligand === item) return;
            fateoutElement.add(item!);
        });
        this.edgeGroup.forEach((edge, id) => {
            if (ligand.edgeMap.has(id)) {
                fateoutElement.delete(edge!.sourceLigand!);
                fateoutElement.delete(edge!.targetLigand!);
                relatedHoverLigand.add(edge!.sourceLigand!);
                relatedHoverLigand.add(edge!.targetLigand!);
                relatedHoverEdge.add(edge!);
            } else {
                fadeoutElement.add(edge!);
            }
        });
        this.historyGroup.forEach((edge, id) => {
            if (ligand.historyMap.has(id)) {
                fateoutElement.delete(edge!.sourceLigand!);
                fateoutElement.delete(edge!.targetLigand!);
                relatedHoverLigand.add(edge!.sourceLigand!);
                relatedHoverLigand.add(edge!.targetLigand!);
                relatedHoverEdge.add(edge!);
            } else {
                fadeoutElement.add(edge!);
            }
        });
        this.onMouseOver(ligand);
    }

    onEdgeMouseOver(edge: EdgeElement) {
        // 处理sourceLigand bug
        if (this.hoverEl === edge || !edge) return;
        hoverEdge.add(edge);
        this.ligandGroup.forEach(item => {
            if (item === edge.sourceLigand || item === edge.targetLigand) {
                relatedHoverLigand.add(item);
            } else {
                fateoutElement.add(item!);
            }
        });
        this.edgeGroup.forEach(item => {
            if (edge === item) return;
            fadeoutElement.add(item!);
        });
        this.historyGroup.forEach(item => {
            if (item?.sourceLigand === edge.sourceLigand && item?.targetLigand === edge.targetLigand) return;
            fadeoutElement.add(item!);
        });
        this.onMouseOver(edge);
    }


    onHistoryMouseOver(history: HistoryElement) {
        if (this.hoverEl === history) return;
        hoverHistory.add(history);
        this.ligandGroup.forEach(item => {
            if (item === history.sourceLigand || item === history.targetLigand) {
                relatedHoverLigand.add(item);
            } else {
                fateoutElement.add(item!);
            }
        });
        this.edgeGroup.forEach(item => {
            if (item?.sourceLigand === history.sourceLigand && item?.targetLigand === history.targetLigand) return;
            fadeoutElement.add(item!);
        });
        this.historyGroup.forEach(item => {
            if (item?.sourceLigand === history.sourceLigand && item?.targetLigand === history.targetLigand) return;
            fadeoutElement.add(item!);
        });
        this.onMouseOver(history);
    }
    onCycleMouseOver(cycle: number[]) {
        const ligandIds: number[] = [];
        this.historyGroup.forEach(item => {
            if (item?.id && cycle.includes(parseInt(item.id, 10))) {
                ligandIds.push(item.data.ligandA, item.data.ligandB);
                relatedHoverEdge.add(item!);
            } else {
                fateoutElement.add(item!);
            }
        });
        const ligands = Array.from(new Set(ligandIds));
        this.ligandGroup.forEach(item => {
            if (item?.id && ligands.includes(item.id)) {
                relatedHoverLigand.add(item!);
            } else {
                fateoutElement.add(item!);
            }
        });
        this.onMouseOver((null as unknown) as Element);
    }

    onLigandRowMouseEnter(id: number) {
        const ligand = this.ligandGroup.map.get(`${id}`);
        if (ligand) {
            this.onLigandMouseOver(ligand);
        }
    }

    onRowMouseEnter(props: { id: number }) {
        if (this.historyForce) {
            const history = this.historyGroup.map.get(`${props.id}`);
            this.onHistoryMouseOver(history!);
            return;
        }
        const edge = this.edgeGroup.map.get(`${props.id}`);
        this.onEdgeMouseOver(edge!);
    }

    onLigandClick(ligand: LigandElement) {
        if (ligand.state.selected) {
            return this.selector.delete(ligand);
        }
        return this.selector.add(ligand);
    }

    onEdgeClick(edge: EdgeElement) {
        const { sourceLigand, targetLigand, id } = edge;
        this.selector.replaceByEdge(sourceLigand!, targetLigand!, id);
    }
    onHistoryClick(history: HistoryElement) {
        if (history.state.selected) {
            return this.selector.deselectHistory(history);
        }
        return this.selector.selectHistory(history);
    }

    onDeleteLigandClick(ligand: LigandElement) {
        const ctx = this.ctx;
        this.selector.delete(ligand);
        ligand.edgeMap.forEach(edge => {
            const edgeProps = ctx.edgeGroup.delete(edge);
            ctx.layout.deleteEdge(edgeProps as EdgeElement);
        });
        const ligandProps = ctx.ligandGroup.delete(ligand);
        ctx.layout.deleteLigand(ligandProps as LigandElement);
        this.onMouseOut();
        ctx.layout.reRun();
    }

    onAddVirtualEdge(props: FEPPair) {
        if (this.historyForce || (props.id !== 0 && this.edgeGroup.map.has(`${props.id}`))) return;
        const ctx = this.ctx;
        const edge = ctx.edgeGroup.add(({
            ...props,
            virtual: true,
            source: { id: props.ligandA },
            target: { id: props.ligandB },
        } as unknown) as EdgeElementProps);
        ctx.layout.addEdge(({
            ...props,
            source: `${props.ligandA}`,
            target: `${props.ligandB}`,
        } as unknown) as EdgeElement);
        ctx.layout.reRun();
        return edge;
    }

    onAddEdgeClick(props: EdgeElementProps) {
        const edge = this.ctx.edgeGroup.map.get(`${props.id}`)!;
        edge.updateProps(props);
        edge.toRealistic();
        edge.reDraw();
        this.selector.updateSelected();
    }

    onAddEdgeList(list: Array<EdgeElementProps>) {
        if (!list.length) return;
        const add = list.length > 0 && this.ctx.edgeGroup.map.size === 0;
        const ctx = this.ctx;
        list.forEach(props => {
            const edge = ctx.edgeGroup.add(props);
            ctx.layout.addEdge(edge);
        });
        this.selector.updateSelected();
        ctx.layout.reRun();
        if (!this.historyForce && add && ctx.layout.initTimes < 2) {
            ctx.layout.initTimes++;
        }
    }
    onAddHistory(props: HistoryElementProps) {
        const history = this.ctx.historyGroup.map.get(`${props.id}`)!;
        history.updateProps(props);
        history.toRealistic();
        history.reDraw();
        this.selector.updateSelected();
    }

    onAddHistoryList(list: Array<HistoryElementProps>) {
        if (!list.length) return;
        const ctx = this.ctx;
        const add = list.length > 0 && ctx.historyGroup.map.size === 0;
        list.forEach(props => {
            if (ctx.ligandGroup.map.has(props.ligandA.toString()) && ctx.ligandGroup.map.has(props.ligandB.toString())) {
                const history = ctx.historyGroup.add(props);
                ctx.layout.addHistory(history);
            }
        });
        this.selector.updateSelected();
        ctx.layout.reRun();
        if (this.historyForce && add && ctx.layout.initTimes < 2) {
            ctx.layout.initTimes++;
        }
    }
    onDeleteHistory(history: HistoryElement) {
        const ctx = this.ctx;
        if (!history.state.virtual) {
            this.selector.clear();
        }
        ctx.layout.deleteHistory(history);
        ctx.historyGroup.delete(history);
        this.onMouseOut();
        ctx.layout.reRun();
    }

    onDeleteEdgeClick(edge: EdgeElement) {
        const ctx = this.ctx;
        if (!edge.state.virtual) {
            this.selector.clear();
        }
        const edgeProps = ctx.edgeGroup.delete(edge);
        ctx.layout.deleteEdge(edgeProps as EdgeElement);
        this.onMouseOut();
        ctx.layout.reRun();
    }

    onDeleteEdgeList(list: Array<EdgeElementProps>) {
        if (!list.length) return;
        const ctx = this.ctx;
        list.forEach(props => {
            const edge = ctx.edgeGroup.map.get(`${props.id}`);
            if (this.selector.edge === edge) {
                this.selector.clear();
            }
            ctx.ligandGroup.map.get(`${props.source.id}`)?.edgeMap.delete(`${props.id}`)
            ctx.ligandGroup.map.get(`${props.target.id}`)?.edgeMap.delete(`${props.id}`)
            ctx.edgeGroup.delete(edge!);
            ctx.layout.deleteEdge(edge!);
        });
        this.onMouseOut();
        ctx.layout.reRun();
    }

    onDeleteHistoryList(list: Array<HistoryElementProps>) {
        if (!list.length) return;
        const ctx = this.ctx;
        list.forEach(props => {
            const history = ctx.historyGroup.map.get(`${props.id}`);
            // if (this.selector.history === history) {
            //     this.selector.clear();
            // }
            ctx.historyGroup.delete(history!);
            ctx.layout.deleteHistory(history!);
        });
        this.onMouseOut();
        ctx.layout.reRun();
    }

    onTableAddLigands(list: Array<LigandElementProps>, position?: { [key: number]: { x: number; y: number } }) {
        const ctx = this.ctx;
        const add = list.length > 0 && this.ctx.ligandGroup.map.size === 0;
        let resetPosition = false;
        list.forEach(props => {
            // ctx.ligandGroup.add({ ...props, firstAdd: true });
            ctx.ligandGroup.add(props);
            ctx.layout.addLigand(props, position ? position[props.id] : undefined);
            if (position && position[props.id]) {
                resetPosition = true;
            }
        });
        if (position && add && !resetPosition) {
            ctx.layout.initTimes = 2;
            ctx.layout.isCalc = true;
            ctx.layout.reRun();
        } else {
            ctx.layout.reRun();
            if (add && ctx.layout.initTimes < 2) {
                ctx.layout.initTimes++;
            }
        }
    }

    onTableDeleteLigands(list: Array<LigandElementProps>) {
        const ctx = this.ctx;
        list.forEach(props => {
            const ligand = ctx.ligandGroup.map.get(`${props.id}`)!;
            this.selector.delete(ligand);
            ligand.edgeMap.forEach(edge => {
                const edgeProps = ctx.edgeGroup.delete(edge);
                ctx.layout.deleteEdge(edgeProps as EdgeElement);
            });
            const ligandProps = ctx.ligandGroup.delete(ligand);
            ctx.layout.deleteLigand(ligandProps as LigandElement);
        });
        ctx.layout.reRun();
    }

    constructor(public ctx: GraphChart) {
        const { ligandGroup, edgeGroup, historyGroup, layout, historyForce } = this.ctx;
        this.ligandGroup = ligandGroup;
        this.edgeGroup = edgeGroup;
        this.historyGroup = historyGroup;
        this.layout = layout;
        this.historyForce = historyForce;
        this.selector = new Selector(ligandGroup.map, edgeGroup.map, historyForce);
    }
}

export default EventsHandler;
