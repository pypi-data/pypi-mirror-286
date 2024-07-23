import { LIGAND_WIDTH_HALF } from '../constant';
import Element from './element';
import emitter from '../events/emitter';
import {
    LigandSubElement,
    MoveToParams,
    LigandRectElement,
    LigandImageElement,
    LigandOrderElement,
    LigandBgRectElement,
    LigandNameElement,
    LigandExpTextElement,
    LigandCalcTextElement,
} from './subElement';
import { EdgeElement } from './edge';
import { HistoryElement } from './history';
import { FEPLigand } from '../type';
// import {getLigand2DImage} from "@services/api/ligands";

export interface LigandElementProps extends FEPLigand {
    info?: Array<string>;
    firstAdd?: boolean;
}

export class LigandElement extends Element {
    id: number;
    name = '';
    edgeMap = new Map();
    historyMap = new Map();
    type = 'ligand';
    info: Array<string> = [];
    status;
    idx;

    state = {
        selected: false,
        hover: false,
        relatedHover: false,
        firstAdd: false,
    };
    order: LigandOrderElement | null = null;
    position = {
        x: 0,
        y: 0,
        originX: 0,
        originY: 0,
    };

    onSelected(i?: number): void {
        const { x, y } = this.position;
        const idx = i! + 1;
        if (this.order) {
            this.order!.updateIdx(idx);
        } else {
            const hover = this.state.hover;
            this.order = new LigandOrderElement({ idx, x, y, hover, z: this.z });
            this.subElements.add(this.order);
            this.el.add(this.order.el);
        }
        this.idx = idx
        super.onSelected();
    }

    onSelectedEnd() {
        if (this.order) {
            this.subElements.delete(this.order);
            this.el.remove(this.order.el);
            this.order = null;
        }
        super.onSelectedEnd();
    }

    addEdge(edge: EdgeElement) {
        this.edgeMap.set(edge.id, edge);
    }

    addHistory(history: HistoryElement) {
        this.historyMap.set(history.id, history);
    }

    moveTo({ x, y }: MoveToParams) {
        if (x === undefined || y === undefined || isNaN(x) || isNaN(y)) {
            return;
        }
        const { data } = this
        const originX = x! + LIGAND_WIDTH_HALF;
        const originY = y! + LIGAND_WIDTH_HALF;
        this.position = { x: x!, y: y!, originX, originY };

        // const ligandName = this.data.name;
        // const hasName = this.info.includes('name');
        // const info = hasName ? this.info.slice(1) : this.info;
        // const [exp, calc] = info;
        const name = (this.info.includes('name') || this.info.includes(data.name)) ? data.name : '';
        const exp = this.info.includes('expDG') ? data.expDG : '';
        const calc_data = this.info.includes('predDG') ? data.predDG : '';
        const calc_error = this.info.includes('predDGErr') ? data.predDGErr : '';
        this.subElements.forEach(element => {
            (element as LigandSubElement).moveTo({ x, y, originX, originY, exp, calc_data, calc_error, name, info: this.info });
        });
    }

    updateInfo(info: Array<string>) {
        this.info = info;
        this.moveTo(this.position);
    }

    updateProps(props: LigandElementProps) {
        this.data = props;
        this.moveTo(this.position);
    }

    constructor(props: LigandElementProps) {
        super();
        const { id, firstAdd = false, info, status, img } = props;
        this.id = id;
        this.state.firstAdd = firstAdd;
        this.data = props;
        this.info = info!;
        this.status = status
        // console.log(props, 'LigandElementProps')
        const bgRect = new LigandBgRectElement();
        const rect = new LigandRectElement();
        const name = new LigandNameElement();
        const exp = new LigandExpTextElement();
        const calc = new LigandCalcTextElement();
        // const image = new LigandImageElement(`data:image/png;base64,MWIKICAgICBSREtpdCAgICAgICAgICAzRAoKIDMxIDMzICAwICAwICAxICAwICAwICAwICAwICAwOTk5IFYyMDAwCiAgLTE1LjM1MjQgIC0xOS4yMjA2ICAtMjUuOTY4NCBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNC42NTI2ICAtMTkuNzA4MSAgLTI3LjA4MjMgQyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTUuODU1NSAgLTIwLjEyMzUgIC0yNS4wMjQxIEMgICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE0LjQ1NDEgIC0yMS4wNjM2ICAtMjcuMjQ4NSBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNS42MzU3ICAtMjEuNDg1NCAgLTI1LjE4NDAgQyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTUuMDUyNiAgLTE2Ljk0NDUgIC0yNi42ODcxIE4gICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE0LjkzNDcgIC0yMS45NjMxICAtMjYuMjk4OCBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNS4yMTYyICAtMTUuNTYxMCAgLTI2LjU5MjkgQyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTUuOTAzMSAgLTE1LjAwNTkgIC0yNS41MDM3IEMgICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE1LjQ0NjIgIC0xMi44MTg3ICAtMjYuMzU5OSBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNC43NzczICAtMTMuMzU1MiAgLTI3LjQ1MjUgQyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTYuMDIwMyAgLTEzLjYyMzUgIC0yNS4zODE1IEMgICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE0LjY3NjggIC0xNC43MzU5ICAtMjcuNTkzNCBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNi41MzEzICAtMTUuOTM5MiAgLTI0LjQ4OTUgQyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTYuMjU4NCAgLTE3LjI0MzUgIC0yNC43NjcxIE4gICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE1LjUzMTcgIC0xNy43NjY5ICAtMjUuODIwMyBDICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNy4yNDA2ICAtMTUuNjA5OCAgLTIzLjUzNzQgTyAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTQuMjUyNSAgLTE5LjA0NjQgIC0yNy44MzgyIEggICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE2LjM5ODEgIC0xOS43OTQzICAtMjQuMTUxMCBIICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xMy44OTM4ICAtMjEuNDA3OCAgLTI4LjEwNDkgSCAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTUuOTkwMyAgLTIyLjE2MzUgIC0yNC40MjA5IEggICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE0LjM2MDQgIC0xMi42ODkxICAtMjguMTk2NCBIICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNi41NDU4ICAtMTMuMTcxMyAgLTI0LjU0OTQgSCAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTYuNzM1MiAgLTE3Ljg5MTUgIC0yNC4xNTQwIEggICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE0LjE5NDEgIC0xNS4xNzU1ICAtMjguNDUzNyBIICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNS41MzE5ICAtMTEuNzQ3NiAgLTI2LjI1MjAgSCAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTQuNzIxNiAgLTIzLjMwMTAgIC0yNi40NTc0IE8gICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE1LjMzMzkgIC0yNC4wNDUzICAtMjUuMzA4MCBDICAgMCAgMCAgMSAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIC0xNS4xNjM2ICAtMjUuMTE0NCAgLTI1LjQzNDggSCAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAgIDAKICAtMTQuODc3OSAgLTIzLjcxMzMgIC0yNC4zNzUzIEggICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwICAwCiAgLTE2LjQwNTggIC0yMy44NDk4ICAtMjUuMjc3NiBIICAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMCAgMAogIDEgIDIgIDIgIDAKICAxICAzICAxICAwCiAgMSAxNiAgMSAgMAogIDIgIDQgIDEgIDAKICAyIDE4ICAxICAwCiAgMyAgNSAgMiAgMAogIDMgMTkgIDEgIDAKICA0ICA3ICAyICAwCiAgNCAyMCAgMSAgMAogIDUgIDcgIDEgIDAKICA1IDIxICAxICAwCiAgNiAgOCAgMSAgMAogIDYgMTYgIDIgIDAKICA3IDI3ICAxICAwCiAgOCAgOSAgMiAgMAogIDggMTMgIDEgIDAKICA5IDEyICAxICAwCiAgOSAxNCAgMSAgMAogMTAgMTEgIDEgIDAKIDEwIDEyICAyICAwCiAxMCAyNiAgMSAgMAogMTEgMTMgIDIgIDAKIDExIDIyICAxICAwCiAxMiAyMyAgMSAgMAogMTMgMjUgIDEgIDAKIDE0IDE1ICAxICAwCiAxNCAxNyAgMiAgMAogMTUgMTYgIDEgIDAKIDE1IDI0ICAxICAwCiAyNyAyOCAgMSAgMAogMjggMjkgIDEgIDYKIDI4IDMwICAxICAwCiAyOCAzMSAgMSAgMApNICBFTkQK`);

        this.subElements.add(bgRect);
        this.subElements.add(rect);
        this.subElements.add(name);
        this.subElements.add(exp);
        this.subElements.add(calc);
        // this.subElements.add(image);

        this.subElements.forEach(element => {
            this.el.add(element.el);
        });
        // 生成2D图
        // getLigand2DImage([id.toString()]).then(rep => {
        //     const image = new LigandImageElement(`data:image/png;base64,${rep.data[0].img}`);
        //     this.subElements.add(image);
        //     this.el.add(image.el);
        //     image.moveTo(this.position);
        // })
        const image = new LigandImageElement(`data:image/png;base64,${img}`);
        this.subElements.add(image);
        this.el.add(image.el);
        image.moveTo(this.position);
        this.updateStyle();

        this.el.on('click', ev => emitter.emit('click', this, ev));
        this.el.on('mouseover', ev => emitter.emit('mouseover', this, ev));
        this.el.on('mouseout', ev => emitter.emit('mouseout', this, ev));
        this.el.on('mousedown', ev => emitter.emit('mousedown', this, ev));
    }
}
