import { Group } from 'zrender';
import { LigandElement, EdgeElement, LigandElementProps, EdgeElementProps } from './element';
import { HistoryElement, HistoryElementProps } from './element/history';

const ligandMap = new Map<string, LigandElement>();
const edgeMap = new Map<string, EdgeElement>();
const historyMap = new Map<string, HistoryElement>();

export class LigandGroup {
    group = new Group();
    map = ligandMap;
    infoList = ['name'];
    add(props: LigandElementProps) {
        const info = this.infoList.map(n => (props as any)[n]).filter(s => s !== undefined);
        const ligand = new LigandElement({ ...props, info });
        ligandMap.set(`${props.id}`, ligand);
        this.group.add(ligand.el);
    }
    delete(ligand: LigandElement) {
        const { id } = ligand;
        ligandMap.delete(`${id}`);
        this.group.remove(ligand.el);
        return { id };
    }
    forEach(cb: (edge?: LigandElement, id?: string) => void) {
        this.map.forEach(cb);
    }
    updateInfolist(infoList: Array<string> = this.infoList) {
        this.infoList = infoList;
        this.map.forEach(ligand => {
            // const info = infoList.map(n => ligand.data[n]).filter(s => s !== undefined);
            ligand.updateInfo(infoList);
        });
    }
    clear() {
        this.map.clear();
        this.group.removeAll();
    }
    constructor(ligands: Array<LigandElementProps>) {
        ligands.forEach(props => this.add(props));
    }
}

export class EdgeGroup {
    group = new Group();
    map = edgeMap;
    infoList = ['simScore'];
    add(props: EdgeElementProps) {
        const info = this.infoList.map(n => (props as any)[n]).filter(s => s !== undefined);
        const edge = new EdgeElement({ ...props, info, ligandMap });
        edgeMap.set(`${props.id}`, edge);
        this.group.add(edge.el);
        return edge;
    }
    delete(edge: EdgeElement) {
        const { id, source, target } = edge;
        edgeMap.delete(`${id}`);
        this.group.remove(edge.el);
        return { id, source, target };
    }
    forEach(cb: (edge?: EdgeElement, id?: string) => void) {
        this.map.forEach(cb);
    }
    reDraw() {
        this.forEach((edge?: EdgeElement) => edge!.reDraw());
    }
    updateInfolist(infoList: Array<string> = this.infoList) {
        this.infoList = infoList;
        this.map.forEach(edge => {
            const info = infoList.filter(n => Object.keys(edge.data).includes(n));
            edge.updateInfo(info);
        });
    }
    init(edges: Array<EdgeElementProps>) {
        edges.forEach(props => this.add(props));
    }
    clear() {
        this.map.clear();
        this.group.removeAll();
    }
    constructor(edges: Array<EdgeElementProps>) {
        this.init(edges);
    }
}


export class HistoryGroup {
    group = new Group();
    map = historyMap;
    infoList = ['simi_score'];
    add(props: HistoryElementProps) {
        const history = new HistoryElement({ ...props, ligandMap, historyForce: this.historyForce });
        historyMap.set(`${props.id}`, history);
        this.group.add(history.el);
        return history;
    }
    delete(history: HistoryElement) {
        const { id, source, target } = history;
        historyMap.delete(id);
        this.group.remove(history.el);
        return { id, source, target };
    }
    forEach(cb: (history?: HistoryElement, id?: string) => void) {
        this.map.forEach(cb);
    }
    reDraw() {
        this.forEach((history?: HistoryElement) => history!.reDraw());
    }
    updateInfolist(infoList: Array<string> = this.infoList) {
        this.infoList = infoList;
        this.map.forEach(history => {
            const info = infoList.filter(n => Object.keys(history.data).includes(n));
            history.updateInfo(info);
        });
    }
    init(histories: Array<HistoryElementProps>) {
        histories.forEach(props => this.add(props));
    }
    clear() {
        this.map.clear();
        this.group.removeAll();
    }
    constructor(histories: Array<HistoryElementProps>, public historyForce: boolean) {
        this.init(histories);
    }
}