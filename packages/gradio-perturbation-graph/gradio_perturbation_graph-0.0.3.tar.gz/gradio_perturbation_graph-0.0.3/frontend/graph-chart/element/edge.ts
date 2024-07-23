import { LIGAND_WIDTH } from '../constant';
import Element from './element';
import emitter, { EVENT_NAME } from '../events/emitter';
import { EdgeSubElement, EdgeLineElement, EdgeTextElement, EdgeArrowElement } from './subElement';
import { LigandElement } from './ligand';
import { getTextPosition, getEdgePoint } from '../helper';
import { FEPPair } from '../type';
import EdgeChargeElement from './subElement/edgeCharge';

export interface EdgeElementProps extends FEPPair {
    info?: Array<string>;
    virtual?: boolean;
    ligandMap?: Map<string, LigandElement>;
}

export class EdgeElement extends Element {
    id = '';
    source = '';
    target = '';
    sourceLigand!: LigandElement;
    targetLigand!: LigandElement;
    type = 'edge';
    info: Array<string> = [];

    state = {
        virtual: false,
        selected: false,
        hover: false,
        relatedHover: false,
    };

    toRealistic() {
        this.state.virtual = false;
        this.updateStyle();
    }

    reDraw() {
        const data = this.data;
        const info = this.info.filter(n => Object.keys(data).includes(n));
        const virtual = this.state.virtual;
        const { originX: sX, originY: sy } = this.sourceLigand!.position;
        const { originX: tX, originY: ty } = this.targetLigand!.position;
        const { x1, y1, x2, y2 } = getEdgePoint({ x: sX, y: sy }, { x: tX, y: ty }, LIGAND_WIDTH);
        const { x, y, rotation } = getTextPosition(x1, y1, x2, y2, info.length);

        this.subElements.forEach(element => {
            (element as EdgeSubElement).draw({ x1, y1, x2, y2, x, y, rotation, info, virtual, data });
        });
    }

    updateInfo(info: Array<string>) {
        this.info = info;
        this.reDraw();
    }

    updateProps(props: EdgeElementProps) {
        this.data = props;
        this.reDraw();
    }

    onHover() {
        super.onHover();
        emitter.emit(EVENT_NAME.GRAPH_EDGE_HOVER, this.data);
    }

    onHoverEnd() {
        super.onHoverEnd();
        emitter.emit(EVENT_NAME.GRAPH_EDGE_HOVEREND, this.data);
    }

    constructor(props: EdgeElementProps) {
        super();
        const { id, source, target, info, virtual = false, ligandMap } = props;
        this.id = `${id}`;
        this.source = `${source.id}`;
        this.target = `${target.id}`;
        this.data = props;
        this.info = info!;
        this.state.virtual = virtual;
        this.sourceLigand = ligandMap!.get(`${source.id}`)!;
        this.targetLigand = ligandMap!.get(`${target.id}`)!;
        this.sourceLigand!.addEdge(this);
        this.targetLigand!.addEdge(this);
        const line = new EdgeLineElement();
        // const arrow = new EdgeArrowElement();
        const text = new EdgeTextElement();
        this.subElements.add(line);
        this.subElements.add(text);
        // this.subElements.add(arrow);
        if (props.chargeChange) {
            const charge = new EdgeChargeElement(`https://cdn.dp.tech/hermite/web/Charged.png`);
            this.subElements.add(charge);
        }
        this.subElements.forEach(element => {
            this.el.add(element.el);
        });
        this.updateStyle();

        this.el.on('click', ev => emitter.emit('click', this, ev));
        this.el.on('mouseover', ev => emitter.emit('mouseover', this, ev));
        this.el.on('mouseout', ev => emitter.emit('mouseout', this, ev));
    }
}
