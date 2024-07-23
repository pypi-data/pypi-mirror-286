import { ElementEvent } from 'zrender';
import emitter, { EVENT_NAME } from './emitter';
import EventsHandler from './handler';
import { GraphChart } from '../chart';
import { Element, EdgeElement, LigandElement } from '../element';
import { HistoryElement } from '../element/history';
let timer: NodeJS.Timeout | null = null;
class Events {
    handler!: EventsHandler;
    isDragging: boolean = false;
    onClick(el: Element, ev: ElementEvent) {
        if (el.type === 'history') {
            if (!timer) {
                timer = setTimeout(() => {
                    clearTimeout(timer!);
                    timer = null;
                }, 300);
                return;
            }
            emitter.emit(EVENT_NAME.SHOW_HISTORY_PARAMS, el);
            clearTimeout(timer!);
            timer = null;
        } else {
            switch (el.type) {
                case 'ligand':
                    this.handler.onLigandClick(el as LigandElement);
                    break;
                case 'edge':
                    this.handler.onEdgeClick(el as EdgeElement);
                    break;
            }
        }
    }
    onMouseover(el: Element) {
        if (this.isDragging) return;
        switch (el.type) {
            case 'ligand':
                this.handler.onLigandMouseOver(el as LigandElement);
                break;
            case 'edge':
                emitter.emit(EVENT_NAME.ON_PAIR_MOUSEOVER, parseInt(el.data.id, 10));
                this.handler.onEdgeMouseOver(el as EdgeElement);
                break;
            case 'history':
                this.handler.onHistoryMouseOver(el as HistoryElement);
        }
    }
    onMouseout() {
        if (this.isDragging) return;
        emitter.emit(EVENT_NAME.ON_PAIR_MOUSEOUT);
        this.handler.onMouseOut();
    }
    onMouseDown(ev: ElementEvent) {
        this.handler.onMouseDown(ev);
    }
    onMouseWheel(ev: ElementEvent) {
        if (this.isDragging) return;
        this.handler.onMouseWheel(ev);
    }
    constructor(public ctx: GraphChart, public historyForce?: boolean) {
        this.handler = new EventsHandler(ctx);
        ctx.renderer.on(EVENT_NAME.CLICK, (...args) => this.handler.onClick(...args));
        ctx.renderer.on(EVENT_NAME.MOUSEDOWN, (...args) => this.onMouseDown(...args));
        ctx.renderer.on(EVENT_NAME.MOUSEWHEEL, (...args) => this.onMouseWheel(...args));
        emitter.on(EVENT_NAME.CLICK, (el, ev) => this.onClick(el, ev));
        emitter.on(EVENT_NAME.MOUSEDOWN, (el, ev) => {
            this.isDragging = true;
            this.handler.onLigandMouseDown(el, ev, () => {
                this.isDragging = false;
            });
        });
        emitter.on(EVENT_NAME.MOUSEOVER, el => this.onMouseover(el));
        emitter.on(EVENT_NAME.MOUSEOUT, () => this.onMouseout());
        emitter.on(EVENT_NAME.DELETE_LIGAND, props => this.handler.onDeleteLigandClick(props));
        emitter.on(EVENT_NAME.ADD_EDGE, props => this.handler.onAddEdgeClick(props));
        emitter.on(EVENT_NAME.ADD_VIRTUAL_EDGE, props => historyForce ? () => { } : this.handler.onAddVirtualEdge(props));
        emitter.on(EVENT_NAME.DELETE_EDGE, ligand => this.handler.onDeleteEdgeClick(ligand));
        emitter.on(EVENT_NAME.ROW_MOUSEENTER, props => this.handler.onRowMouseEnter(props));
        emitter.on(EVENT_NAME.CYCLE_ROW_MOUSEENTER, props => this.handler.onCycleMouseOver(props));
        emitter.on(EVENT_NAME.ADD_EDGES, list => this.handler.onAddEdgeList(list));
        emitter.on(EVENT_NAME.DELETE_EDGES, list => this.handler.onDeleteEdgeList(list));
        emitter.on(EVENT_NAME.SET_EDGE_INFOLIST, infoList => ctx.edgeGroup.updateInfolist(infoList));
        emitter.on(EVENT_NAME.SET_LIGAND_INFOLIST, infoList => ctx.ligandGroup.updateInfolist(infoList));
        emitter.on(EVENT_NAME.TABLE_ADD_LIGANDS, (list, position) => this.handler.onTableAddLigands(list, position));
        emitter.on(EVENT_NAME.TABLE_DELETE_LIGANDS, list => this.handler.onTableDeleteLigands(list));

        emitter.on(EVENT_NAME.ADD_HISTORY, props => this.handler.onAddHistory(props));
        emitter.on(EVENT_NAME.ADD_HISTORIES, list => this.handler.onAddHistoryList(list));
        emitter.on(EVENT_NAME.CLICK_HISTORY, el => this.handler.onHistoryClick(el as HistoryElement));
        emitter.on(EVENT_NAME.CLEAR, () => this.handler.onClear());
        emitter.on(EVENT_NAME.DELETE_HISTORIES, list => this.handler.onDeleteHistoryList(list));
        emitter.on(EVENT_NAME.LIGAND_ROW_MOUSEENTER, props => this.handler.onLigandRowMouseEnter(props));
    }
}

export default Events;
