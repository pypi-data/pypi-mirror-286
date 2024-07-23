import { Line } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_WIDTH, LIGAND_EXP_CALC_LINEHEIGHT, LIGAND_TEXT_STYLE } from '../../constant';

class LigandTextElement extends LigandSubElement {
    type = 'ligandText';
    el = new Line({
        style: {},
        z2: LIGAND_TEXT_STYLE.INITIAL.ZLEVEL_THIRD,
    });

    style = {
        selected: {
            stroke: LIGAND_TEXT_STYLE.SELECTED.BACKGROUNDCOLOR,
        },
        hover: {
            stroke: LIGAND_TEXT_STYLE.HOVER.BACKGROUNDCOLOR,
        },
        relatedHover: {
            stroke: LIGAND_TEXT_STYLE.RELATEDHOVER.BACKGROUNDCOLOR,
        },
        firstAdd: {
            stroke: LIGAND_TEXT_STYLE.FIRSTADD.BACKGROUNDCOLOR,
        },
        default: {
            stroke: LIGAND_TEXT_STYLE.DEFAULT.BACKGROUNDCOLOR,
        },
    };

    moveTo({ x, y, originX, originY, info }: MoveToParams) {
        const lineHeight = LIGAND_EXP_CALC_LINEHEIGHT;
        if (info?.length) {
            this.el.show();
        } else {
            this.el.hide();
        }
        this.el.attr({
            originX,
            originY,
            shape: {
                x1: x!,
                y1: y! + LIGAND_WIDTH - lineHeight,
                x2: x! + LIGAND_WIDTH,
                y2: y! + LIGAND_WIDTH - lineHeight,
            },
        });
    }
}

export default LigandTextElement;
