import { Text as ZrText } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_ORDER_STYLE, SCALE_X } from '../../constant';

interface LigandOrderProps {
    idx: number;
    x: number;
    y: number;
    hover: boolean;
    z: number;
}

class LigandOrderElement extends LigandSubElement {
    type = 'ligandRect';
    el = new ZrText();
    style = {};

    updateStyle() {}

    moveTo({ x, y }: MoveToParams) {
        this.el.attr({
            originX: LIGAND_ORDER_STYLE.POSITION.ORIGIN,
            originY: LIGAND_ORDER_STYLE.POSITION.ORIGIN,
            x: x! + LIGAND_ORDER_STYLE.POSITION.OFFSET,
            y: y! + LIGAND_ORDER_STYLE.POSITION.OFFSET,
        });
    }
    updateIdx(idx: number) {
        this.el.attr({
            style: {
                text: `{order|${idx}}`,
            },
        });
    }
    constructor({ idx, x, y, hover, z }: LigandOrderProps) {
        super();
        this.el.attr({
            style: {
                text: `{order|${idx}}`,
                rich: {
                    order: {
                        fill: LIGAND_ORDER_STYLE.INITIAL.FILL,
                        fontWeight: LIGAND_ORDER_STYLE.INITIAL.FONTWEIGHT,
                        align: LIGAND_ORDER_STYLE.INITIAL.ALIGN,
                        backgroundColor: LIGAND_ORDER_STYLE.INITIAL.BACKGROUNDCOLOR,
                        width: LIGAND_ORDER_STYLE.INITIAL.WIDTH,
                        height: LIGAND_ORDER_STYLE.INITIAL.HEIGHT,
                        borderRadius: LIGAND_ORDER_STYLE.INITIAL.BORDERRADIUS,
                    },
                },
            },
            z,
            z2: LIGAND_ORDER_STYLE.INITIAL.ZLEVEL_THIRD,
        });
        if (hover) {
            this.el.attr({
                scaleX: SCALE_X,
                scaleY: SCALE_X,
            });
        }
        this.moveTo({ x, y });
    }
}

export default LigandOrderElement;
