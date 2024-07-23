import { LIGAND_WIDTH } from '../constant';
import Element from './element';
import emitter, { EVENT_NAME } from '../events/emitter';
import { EdgeSubElement } from './subElement';
import { LigandElement } from './ligand';
import { getTextPosition, getEdgePoint, moveByRotation } from '../helper';
import HistoryEdgeArrowElement from './subElement/historyEdgeArrow';
import HistoryEdgeLineElement from './subElement/historyEdgeLine';
import HistoryEdgeTextElement from './subElement/historyEdgeText';
import HistoryEdgeChargeElement from './subElement/historyEdgeCharge';
import { FEPPair } from '../type';
import { Text as ZrText } from 'zrender';

export interface HistoryElementProps extends FEPPair {
    confidence?: number;
    info?: Array<string>;
    virtual?: boolean;
    ligandMap?: Map<string, LigandElement>;
    order?: number;
    historyForce: boolean;
}

export class HistoryElement extends Element {
    id = '';
    source = '';
    target = '';
    confidence = 0;
    order = 0;
    sourceLigand!: LigandElement;
    targetLigand!: LigandElement;
    type = 'history';
    info: Array<string> = [];
    infoEl: any;
    historyForce: boolean;

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
        // const info = this.info;
        const virtual = this.state.virtual;
        const { originX: sX, originY: sy } = this.sourceLigand!.position;
        const { originX: tX, originY: ty } = this.targetLigand!.position;
        const { x1, y1, x2, y2, offsetVec } = getEdgePoint({ x: sX, y: sy }, { x: tX, y: ty }, LIGAND_WIDTH);
        const { x, y, rotation } = getTextPosition(x1, y1, x2, y2, 4);
        this.subElements.forEach(element => {
            (element as EdgeSubElement).draw({ x1, y1, x2, y2, x, y, rotation, confidence: this.confidence, virtual, order: this.order, offsetVec, historyForce: this.historyForce, data: this.data });
        });
    }

    updateInfo(info: Array<string>) {
        this.info = info;
        this.reDraw();
    }

    updateProps(props: HistoryElementProps) {
        this.data = props;
        this.reDraw();
    }

    onHover() {
        super.onHover();
        this.infoEl.el.children().forEach((child: ZrText) => {
            child.invisible = false;
            child.update();
        })
        const chargeImg = [...this.subElements.values()].find(item => item.type === 'historyEdgeCharge')
        if (chargeImg) {
            const res = moveByRotation(chargeImg.el.originX, chargeImg.el.originY, chargeImg.el.rotation, 60)
            chargeImg.el.attr({
                originX: res.x,
                originY: res.y,
                style: {
                    x: res.x,
                    y: res.y,
                },
            })
        }
        emitter.emit(EVENT_NAME.GRAPH_EDGE_HOVER, this.data);
    }

    onHoverEnd() {
        super.onHoverEnd();
        this.infoEl.el.children().forEach((child: ZrText) => {
            child.invisible = true;
            child.update();
        })
        const chargeImg = [...this.subElements.values()].find(item => item.type === 'historyEdgeCharge')
        if (chargeImg) {
            const res = moveByRotation(chargeImg.el.originX, chargeImg.el.originY, chargeImg.el.rotation, -60)
            chargeImg.el.attr({
                originX: res.x,
                originY: res.y,
                style: {
                    x: res.x,
                    y: res.y,
                },
            })
        }
        emitter.emit(EVENT_NAME.GRAPH_EDGE_HOVEREND, this.data);
    }

    constructor(props: HistoryElementProps) {
        super();
        const { id, source, target, confidence, info, virtual = false, ligandMap, order, historyForce } = props;
        this.id = `${id}`;
        this.source = `${source.id}`;
        this.target = `${target.id}`;
        this.confidence = confidence || 0;
        this.order = order || 0;
        this.data = props;
        this.info = info!;
        this.state.virtual = virtual;
        this.historyForce = historyForce || false;
        this.sourceLigand = ligandMap!.get(`${source.id}`)!;
        this.targetLigand = ligandMap!.get(`${target.id}`)!;
        this.sourceLigand!.addHistory(this);
        this.targetLigand!.addHistory(this);

        const bezierLine = new HistoryEdgeLineElement();
        const bezierArrow = new HistoryEdgeArrowElement();
        const infoText = new HistoryEdgeTextElement();
        this.subElements.add(bezierLine);
        this.subElements.add(bezierArrow);
        this.subElements.add(infoText);
        if (props.chargeChange) {
            const charge = new HistoryEdgeChargeElement(`https://cdn.dp.tech/hermite/web/Charged.png`);
            this.subElements.add(charge);
        }
        this.subElements.forEach(element => {
            this.el.add(element.el);
        });
        this.infoEl = infoText;
        this.updateStyle();

        this.el.on('click', ev => emitter.emit('click', this, ev));
        this.el.on('mouseover', ev => emitter.emit('mouseover', this, ev));
        this.el.on('mouseout', ev => emitter.emit('mouseout', this, ev));
    }
}
