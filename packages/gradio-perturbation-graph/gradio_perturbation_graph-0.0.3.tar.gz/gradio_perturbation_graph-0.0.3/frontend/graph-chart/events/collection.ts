import emitter, { EVENT_NAME } from './emitter';
import { EdgeElement, LigandElement } from '../element';
import { HistoryElement } from '../element/history';

export class Selector {
    edge: EdgeElement | null = null;
    list: Array<LigandElement> = [];
    deleteList: Array<LigandElement | EdgeElement> = [];
    histories: Array<HistoryElement> = [];

    add(ligand: LigandElement) {
        if (this.historyForce) {
            this.deleteList.push(...this.list.map(item => item));
            this.list = [ligand];
            this.update();
            return;
        }
        this.checkVirtualEdge();
        if (this.list.length > 1) {
            this.deleteList.push(this.list.shift()!);
            if (this.edge) {
                this.deleteList.push(this.edge);
                this.edge = null;
            }
        }
        this.list.push(ligand);
        if (this.list.length === 2) {
            this.selectAEdge(this.list[0], this.list[1]);
        }
        this.update();
    }

    delete(ligand: LigandElement) {
        const idx = this.list.indexOf(ligand);
        if (idx < 0) return;
        this.checkVirtualEdge();
        if (idx) {
            this.deleteList.push(this.list.pop()!);
        } else {
            this.deleteList.push(this.list.shift()!);
        }
        if (this.edge) {
            this.deleteList.push(this.edge);
            this.edge = null;
        }
        this.update();
    }

    replaceByEdge(sourceLigand: LigandElement, targetLigand: LigandElement, id: string) {
        this.checkVirtualEdge();
        this.deleteList = this.list;
        this.list = [sourceLigand, targetLigand];
        if (this.edge && this.edge.id !== id) {
            this.deleteList.push(this.edge);
            this.edge = null;
        }
        this.selectAEdge(sourceLigand, targetLigand);
        this.update();
    }

    selectAEdge(sourceLigand: LigandElement, targetLigand: LigandElement) {
        const idList = [...sourceLigand.edgeMap.keys()];
        let edge: EdgeElement | undefined;
        targetLigand.edgeMap.forEach(item => {
            if (!item.data.virtual) {
                if (idList.includes(`${item.data.id}`) && ((item.data.source.id === sourceLigand.id && item.data.target.id === targetLigand.id) || (item.data.source.id === targetLigand.id && item.data.target.id === sourceLigand.id))) {
                    edge = item;
                }
            } else {
                emitter.emit(EVENT_NAME.DELETE_EDGE, item);
            }
        });
        if (!edge) {
            edge = emitter.emit(EVENT_NAME.SELECT_VIRTUAL_EDGE, {
                id: edge ? (edge as EdgeElement).id : 0,
                source: sourceLigand.id,
                target: targetLigand.id,
                ligandA: sourceLigand.data.name,
                ligandB: targetLigand.data.name,
            });
        }
        this.edge = edge!;
    }


    selectHistory(history: HistoryElement) {
        this.histories.push(history);
        this.update();
    }
    deselectHistory(history: HistoryElement) {
        this.histories = this.histories.filter(item => item.id !== history.id);
        this.deleteList.push(history);
        this.update();
    }
    checkVirtualEdge() {
        if (!this.edge || !this.edge.state.virtual) return;
        emitter.emit(EVENT_NAME.DELETE_EDGE, this.edge);
        this.edge = null;
    }

    clear() {
        this.checkVirtualEdge();
        this.deleteList = this.list.slice();
        if (this.edge) {
            this.deleteList.push(this.edge);
            this.edge = null;
        }
        this.list = [];
        this.update();
    }

    updateSelected() {
        const selected = [
            ['empty', null],
            ['ligand', this.list[0]],
            ['edge', this.edge],
        ][this.list.length];
        emitter.emit(EVENT_NAME.SELECTOR_CHANGE, selected[0], selected[1]);
    }

    update() {
        this.deleteList.forEach(item => {
            item.onSelectedEnd();
        });
        this.list.forEach((item, idx) => {
            item.onSelected(idx);
        });
        this.histories.forEach((item, idx) => {
            item.onSelected(idx);
        });
        this.edge && this.edge.onSelected();
        this.deleteList = [];
        this.updateSelected();
    }

    constructor(public ligandMap: Map<string, LigandElement>, public edgeMap: Map<string, EdgeElement>, public historyForce: boolean) {}
}

export const hoverLigand = new Set<LigandElement>();
export const hoverEdge = new Set<EdgeElement>();
export const hoverHistory = new Set<HistoryElement>();
export const relatedHoverLigand = new Set<LigandElement>();
export const relatedHoverEdge = new Set<EdgeElement>();
export const relatedHoverHistory = new Set<HistoryElement>();
export const fateoutElement = new Set<LigandElement | EdgeElement>();
export const fadeoutElement = new Set<LigandElement | EdgeElement>();
