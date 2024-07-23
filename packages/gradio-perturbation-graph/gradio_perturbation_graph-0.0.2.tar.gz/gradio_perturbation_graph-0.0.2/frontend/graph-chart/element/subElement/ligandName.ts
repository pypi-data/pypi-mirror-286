import { Text as ZrText } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_WIDTH, LIGAND_WIDTH_HALF, LIGAND_TEXT_STYLE } from '../../constant';

class LigandNameElement extends LigandSubElement {
    type = 'ligandText';
    el = new ZrText({
        style: {
            align: LIGAND_TEXT_STYLE.INITIAL.ALIGN,
            fontSize: LIGAND_TEXT_STYLE.INITIAL.FONT_SIZE,
            lineHeight: LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT,
        },
        z2: LIGAND_TEXT_STYLE.INITIAL.ZLEVEL_THIRD,
    });

    style = {
        selected: {
            fill: LIGAND_TEXT_STYLE.SELECTED.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.SELECTED.BACKGROUNDCOLOR,
        },
        hover: {
            fill: LIGAND_TEXT_STYLE.HOVER.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.HOVER.BACKGROUNDCOLOR,
        },
        relatedHover: {
            fill: LIGAND_TEXT_STYLE.RELATEDHOVER.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.RELATEDHOVER.BACKGROUNDCOLOR,
        },
        firstAdd: {
            fill: LIGAND_TEXT_STYLE.FIRSTADD.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.FIRSTADD.BACKGROUNDCOLOR,
        },
        default: {
            fill: LIGAND_TEXT_STYLE.DEFAULT.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.DEFAULT.BACKGROUNDCOLOR,
        },
        selectedSecond: {
            fill: LIGAND_TEXT_STYLE.SELECTED.FILL,
            backgroundColor: LIGAND_TEXT_STYLE.SELECTED.BACKGROUNDCOLOR,
        },
    };

    moveTo({ x, y, originX, originY, name }: MoveToParams) {
        this.el.attr({
            originX,
            originY,
            style: {
                text: name,
                x: x! + LIGAND_WIDTH_HALF,
                y: y!,
                width: LIGAND_WIDTH,
            },
        });
    }
}

export default LigandNameElement;
