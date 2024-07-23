import FRLayout from './FRLayout';
import Graph from './graph';
import { getInitialPos } from '../helper';
import Room from '../room';
import { LigandGroup, EdgeGroup, HistoryGroup } from '../group';
import Vertex from './vertex';
import { EdgeProps } from './graph';
import { EdgeElement, LigandElement, LigandElementProps, EdgeElementProps } from '../element';
import { LIGAND_WIDTH } from '../constant';
import { HistoryElement } from '../element/history';

class Layout {
    width = 0;
    height = 0;
    graph!: Graph;
    initTimes: number = 0;
    isCalc: boolean = false;
    state = 0;
    layoutAlgorithm!: FRLayout;
    updateGraphics() {
        const ligandMap = this.ligandGroup.map;
        this.graph.forEachVertex(vertex => {
            const { pos, id } = vertex!;
            const ligand = ligandMap.get(id);
            ligand && ligand.moveTo(pos);
        });
        this.edgeGroup.reDraw();
        this.historyGroup.reDraw();
    }

    step() {
        this.layoutAlgorithm?.updatePhysics(this.isCalc);
        this.updateGraphics();
    }

    run(selfCall?: boolean) {
        window.requestAnimationFrame(() => {
            if (!selfCall) {
                this.state = 0;
            }
            this.step();
            if (this.layoutAlgorithm?.isDone()) {
                if (this.initTimes >= 2) {
                    this.isCalc = true;
                }
                this.state = 1;
                // 微扰图位置更新
                this.graph.isUpdate = true;
                return;
            }
            this.state = 0;
            this.run(true);
        });
    }
    reRun() {
        this.state = 0;
        this.layoutAlgorithm?.reset();
        this.run();
    }
    addEdge(edge: EdgeElement) {
        if (!this.historyForce) {
            this.graph.addEdge(edge.source, edge.target);
        }
    }
    deleteEdge(edge: EdgeElement) {
        if (!this.historyForce) {
            this.graph.deleteEdge(edge.source, edge.target);
        }
    }
    addHistory(history: HistoryElement) {
        if (this.historyForce) {
            this.graph.addEdge(history.source, history.target);
        }
    }
    deleteHistory(history: HistoryElement) {
        if (this.historyForce) {
            this.graph.deleteEdge(history.source, history.target);
        }
    }
    addLigand(ligand: { id: number }, position?: { x: number; y: number }) {
        const { x: posX, y: posY } = position || getInitialPos(this.width, this.height, true);
        this.graph.addVertex(`${ligand.id}`, posX, posY);
    }
    deleteLigand(ligand: { id: number }) {
        this.graph.deleteVertex(`${ligand.id}`);
    }

    initPos(width: number, height: number) {
        this.ligandGroup.forEach((ligand, id) => {
            const v = this.graph.getVertex(id!);
            const { x, y } = getInitialPos(width, height, !!ligand!.edgeMap.size);
            v.pos.setValues(x, y);
        });
    }

    initViewerRoom() {
        const { width, height } = this.room;
        this.width = width - LIGAND_WIDTH;
        this.height = height - LIGAND_WIDTH;
    }

    initGraph(ligands: Array<Vertex>, edges: Array<EdgeProps>) {
        this.graph = new Graph(ligands, edges);
    }

    init(ligands: Array<LigandElementProps>, edges: Array<EdgeElementProps>) {
        this.initViewerRoom();
        this.graph = new Graph((ligands as unknown) as Array<Vertex>, edges.map(edge => { return { source: `${edge.source.id}`, target: `${edge.target.id}` } }));
        this.initPos(this.width, this.height);
        this.layoutAlgorithm = new FRLayout(this.width, this.height, this.graph);
    }

    resize() {
        this.initViewerRoom();
        this.layoutAlgorithm.resize(this.width, this.height, this.graph);
        this.run();
    }

    constructor(public room: Room, public ligandGroup: LigandGroup, public edgeGroup: EdgeGroup, public historyGroup: HistoryGroup, public historyForce: boolean) { }
}

export default Layout;
