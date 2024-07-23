import { init, ZRenderType, registerPainter } from 'zrender';
import CanvasPainter from 'zrender/lib/canvas/Painter';
registerPainter('canvas', CanvasPainter);
import { LigandGroup, EdgeGroup, HistoryGroup } from './group';
import Room from './room';
import Layout from './layout';
import Events from './events';
import emitter, { EventEmitter, EVENT_NAME } from './events/emitter';
import { LigandElementProps, EdgeElementProps } from './element';
import { HistoryElementProps } from './element/history';
import { debounce } from 'lodash';

export class GraphChart {
    renderer!: ZRenderType;
    room!: Room;
    ligandGroup!: LigandGroup;
    edgeGroup!: EdgeGroup;
    historyGroup!: HistoryGroup;
    layout!: Layout;
    events!: Events;
    emitter!: EventEmitter;
    historyForce!: boolean;
    savePosition = debounce(() => {
        emitter.emit(EVENT_NAME.SAVE_POSITION);
    }, 1000);

    initRoom(parent: HTMLElement, dom: HTMLElement, len: number) {
        this.room = new Room(parent, dom);
        this.room.init(len);
    }

    initGroup(ligands: Array<LigandElementProps>, edges: Array<EdgeElementProps>, histories: Array<HistoryElementProps>) {
        this.ligandGroup = new LigandGroup(ligands);
        this.edgeGroup = new EdgeGroup(edges);
        this.historyGroup = new HistoryGroup(histories, this.historyForce);
        this.renderer.add(this.ligandGroup.group);
        this.renderer.add(this.edgeGroup.group);
        this.renderer.add(this.historyGroup.group);
    }

    initLayout(ligands: Array<LigandElementProps>, edges: Array<EdgeElementProps>) {
        this.layout = new Layout(this.room!, this.ligandGroup!, this.edgeGroup!, this.historyGroup!, this.historyForce!);
        this.layout.init(ligands, edges);
        this.layout.run();
    }

    initEvents() {
        this.events = new Events(this);
        this.emitter = emitter;
    }

    init(parent: HTMLElement, dom: HTMLElement, historyForce?: boolean) {
        this.historyForce = historyForce || false;
        this.initRoom(parent, dom, 0);
        // this.renderer = init(dom, { devicePixelRatio: 2 });
        // this.renderer = init(dom, { renderer: "vml" });
        // this.renderer = init(dom, { renderer: 'svg' });
        this.renderer = init(dom);
        this.renderer.dom?.addEventListener('mouseleave', this.savePosition);

        this.initGroup([], [], []);
        this.initLayout([], []);
        this.initEvents();
    }

    resetLigands(ligands: Array<LigandElementProps>, position?: { [key: number]: { x: number; y: number } }) {
        if (!Array.isArray(ligands)) return;
        this.resize(ligands.length);
        const cach = new Set();
        const ligandsMap = this.ligandGroup.map;
        const deleteList: Array<LigandElementProps> = [];
        const updateList: Array<LigandElementProps> = [];
        const addList: Array<LigandElementProps> = [];
        ligands.forEach(props => {
            cach.add(props.id);
            if (ligandsMap.has(`${props.id}`)) {
                updateList.push(props);
            } else {
                addList.push(props);
            }
        });
        ligandsMap.forEach(ligand => {
            if (cach.has(ligand.id)) return;
            deleteList.push(ligand);
        });
        updateList.forEach(props => {
            const ligand = ligandsMap.get(`${props.id}`)!;
            ligand.updateProps(props);
        });
        this.ligandGroup.updateInfolist();
        emitter.emit(EVENT_NAME.TABLE_DELETE_LIGANDS, deleteList);
        emitter.emit(EVENT_NAME.TABLE_ADD_LIGANDS, addList, position);
        this.layout.run();
    }

    resetEdges(edges: Array<EdgeElementProps>) {
        if (!Array.isArray(edges)) return;
        const cach = new Set();
        const edgesMap = new Map([...this.edgeGroup.map.entries()].map(([_, edge]) => {
            return [edge.data.uniqueId, edge];
        }));
        const deleteList: Array<EdgeElementProps> = [];
        const addList: Array<EdgeElementProps> = [];
        edges.forEach(props => {
            cach.add(`${props.uniqueId}`);
            cach.add(`${props.ligandB}-${props.ligandA}`);
            const edge = edgesMap.get(`${props.uniqueId}`) ?? edgesMap.get(`${props.ligandB}-${props.ligandA}`);
            // if (edge && !edgesMap.has(`${props.uniqueId}`)) {
            //     console.log('Reset Edges', props, edge)
            //     debugger;
            // }
            if (edge?.state.virtual) {
                return emitter.emit(EVENT_NAME.ADD_EDGE, props);
            }
            if (edge) return edge.updateProps(props);
            addList.push(props);
        });
        edgesMap.forEach(edge => {
            if (cach.has(edge.data.uniqueId)) return;
            if (edge.state.virtual) return;
            deleteList.push(edge.data);
        });
        emitter.emit(EVENT_NAME.DELETE_EDGES, deleteList);
        emitter.emit(EVENT_NAME.ADD_EDGES, addList);
        this.edgeGroup.updateInfolist();
        this.layout.run();
    }
    resetHistories(histories: Array<HistoryElementProps>) {
        if (!Array.isArray(histories)) return;
        const cach = new Set();
        const historiesMap = this.historyGroup.map;
        const deleteList: Array<HistoryElementProps> = [];
        const addList: Array<HistoryElementProps> = [];
        histories.forEach(props => {
            cach.add(props.id);
            const history = historiesMap.get(`${props.id}`);
            if (history?.state.virtual) {
                return emitter.emit(EVENT_NAME.ADD_HISTORY, props);
            }
            if (history) return history.updateProps(props);
            addList.push(props);
        });
        const idList = histories.map(item => item.id.toString());
        historiesMap.forEach(history => {
            if (idList.includes(history.id)) return;
            deleteList.push(history.data);
        });
        emitter.emit(EVENT_NAME.DELETE_HISTORIES, deleteList);
        emitter.emit(EVENT_NAME.ADD_HISTORIES, addList);
        // this.historyGroup.updateInfolist();
        this.layout.run();
    }
    initEdges(edges: Array<EdgeElementProps>) {
        this.edgeGroup.init(edges);
    }

    clearEdges() {
        const list: Array<EdgeElementProps> = [];
        this.edgeGroup.forEach(edge => {
            list.push(edge!.data);
        });
        emitter.emit(EVENT_NAME.DELETE_EDGES, list);
    }

    resize(size = this.edgeGroup.map.size) {
        this.room.init(size);
        if (this.renderer.painter && this.renderer.handler) {
            this.renderer?.resize();
        }
        this.layout?.resize();
    }

    dispose() {
        if (!this.renderer) return;
        this.renderer.dom?.removeEventListener('mouseleave', this.savePosition);
        this.ligandGroup.clear();
        this.edgeGroup.clear();
        this.historyGroup.clear();
        this.renderer.dispose();
    }
}

export default new GraphChart();
