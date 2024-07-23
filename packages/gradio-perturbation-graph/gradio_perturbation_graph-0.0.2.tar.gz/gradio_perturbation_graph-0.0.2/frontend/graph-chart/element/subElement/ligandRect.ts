import { Rect } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_RECT_STYLE } from '../../constant';

class LigandRectElement extends LigandSubElement {
    type = 'ligandRect';
    el = new Rect({
        style: {
            fill: LIGAND_RECT_STYLE.INITIAL.FILL,
            lineWidth: LIGAND_RECT_STYLE.INITIAL.LINEWIDTH,
        },
        shape: {
            r: LIGAND_RECT_STYLE.INITIAL.RADIUS,
            width: LIGAND_RECT_STYLE.INITIAL.WIDTH,
            height: LIGAND_RECT_STYLE.INITIAL.HEIGHT,
        },
        z2: LIGAND_RECT_STYLE.INITIAL.ZLEVEL_THIRD,
    });

    style = {
        selected: {
            stroke: LIGAND_RECT_STYLE.SELECTED.STROKE,
        },
        hover: {
            stroke: LIGAND_RECT_STYLE.HOVER.STROKE,
        },
        relatedHover: {
            stroke: LIGAND_RECT_STYLE.RELATEDHOVER.STROKE,
        },
        firstAdd: {
            stroke: LIGAND_RECT_STYLE.FIRSTADD.STROKE,
        },
        default: {
            stroke: LIGAND_RECT_STYLE.DEFAULT.STROKE,
        },
    };

    moveTo({ x, y, originX, originY }: MoveToParams) {
        this.el.attr({
            originX,
            originY,
            shape: {
                x,
                y,
            },
        });
    }
}

export default LigandRectElement;
