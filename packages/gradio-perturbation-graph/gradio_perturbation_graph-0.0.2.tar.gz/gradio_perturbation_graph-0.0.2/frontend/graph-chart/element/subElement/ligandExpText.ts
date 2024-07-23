import { Group, Text as ZrText } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import {
    LIGAND_WIDTH,
    LIGAND_WIDTH_HALF,
    LIGAND_TEXT_STYLE,
    LIGAND_EXP_TEXT_STYLE,
    LIGAND_EXP_CALC_DIS,
    LIGAND_EXP_CALC_LINEHEIGHT, LIGAND_CALC_TEXT_STYLE,
} from '../../constant';
import { formulaList, getFormulaText, skew, subscriptOffset, superscriptOffset } from '../../helper';

class LigandExpTextElement extends LigandSubElement {
    type = 'ligandExpText';
    el = new Group({});
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
    };

    moveTo({ x, y, originX, originY, calc_data, exp, calc_error, info }: MoveToParams) {
        const lineHeight = LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT;
        const twoLines = calc_data && exp && info?.includes('predDG') && info.includes('expDG');
        const key = 'expDG';
        const position = { x: -LIGAND_WIDTH_HALF, y: LIGAND_WIDTH_HALF - lineHeight };
        const vecX = { x: 1, y: 0 };
        const vecY = { x: 0, y: 3 };
        if (info?.includes(key) && exp) {
            const formula = {
                ...formulaList[key],
                text: (+exp).toFixed(3),
            }
            if (!this.el.childOfName(`${key}_content`)) {
                this.el.add(new ZrText({
                    x: x! + LIGAND_WIDTH_HALF,
                    y: y! + LIGAND_WIDTH_HALF,
                    style: {
                        text: formula.content,
                        ...position,
                        width: LIGAND_WIDTH - formula.style.padding[3] + formula.style.padding[1],
                        lineHeight: LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT,
                        ...this.style.default,
                        padding: formula.style.padding,
                        fontSize: '11px',
                    },
                    name: `${key}_content`,
                    zlevel: 5,
                }));
            } else {
                (this.el.childOfName(`${key}_content`) as any).attr({
                    x: x! + LIGAND_WIDTH_HALF,
                    y: y! + LIGAND_WIDTH_HALF,
                    style: {
                        text: formula.content,
                        ...position,
                        width: LIGAND_WIDTH - formula.style.padding[3] + formula.style.padding[1],
                        lineHeight: LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT,
                        ...this.style.default,
                        padding: formula.style.padding,
                        fontSize: '11px',
                    },
                    name: `${key}_content`,
                    zlevel: Math.max(5, (this.el.childOfName(`${key}_content`) as any)?.zlevel || 0),
                })
            }
            if (formula.superscript) {
                if (!this.el.childOfName(`${key}_superscript`)) {
                    this.el.add(new ZrText({
                        x: x! + LIGAND_WIDTH_HALF,
                        y: y! + LIGAND_WIDTH_HALF,
                        style: {
                            ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.padding[3] - formula.style.padding[1], superscriptOffset + formula.style.padding[0] - formula.style.padding[2]),
                            text: formula.superscript,
                            fontSize: 8,
                            fill: this.style.default.fill,
                        },
                        name: `${key}_superscript`,
                        zlevel: 5,
                    }));
                } else {
                    (this.el.childOfName(`${key}_superscript`) as any).attr({
                        x: x! + LIGAND_WIDTH_HALF,
                        y: y! + LIGAND_WIDTH_HALF,
                        style: {
                            ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.padding[3] - formula.style.padding[1], superscriptOffset + formula.style.padding[0] - formula.style.padding[2]),
                            text: formula.superscript,
                            fontSize: 8,
                            fill: this.style.default.fill,
                        },
                        name: `${key}_superscript`,
                        zlevel: Math.max(5, (this.el.childOfName(`${key}_superscript`) as any)?.zlevel || 0),
                    })
                }
            }
            if (formula.subscript) {
                if (!this.el.childOfName(`${key}_subscript`)) {
                    this.el.add(new ZrText({
                        x: x! + LIGAND_WIDTH_HALF,
                        y: y! + LIGAND_WIDTH_HALF,
                        style: {
                            text: formula.subscript,
                            fontSize: 8,
                            ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.padding[3] - formula.style.padding[1], subscriptOffset + formula.style.padding[0] - formula.style.padding[2]),
                            fill: this.style.default.fill,
                        },
                        name: `${key}_subscript`,
                        zlevel: Math.max(5, (this.el.childOfName(`${key}_content`) as any)?.zlevel || 0),
                    }));
                } else {
                    (this.el.childOfName(`${key}_subscript`) as any).attr({
                        x: x! + LIGAND_WIDTH_HALF,
                        y: y! + LIGAND_WIDTH_HALF,
                        style: {
                            text: formula.subscript,
                            fontSize: 8,
                            ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.padding[3] - formula.style.padding[1], subscriptOffset + formula.style.padding[0] - formula.style.padding[2]),
                            fill: this.style.default.fill,
                        },
                        name: `${key}_subscript`,
                        zlevel: Math.max(5, (this.el.childOfName(`${key}_subscript`) as any)?.zlevel || 0),
                    })
                }
            }

            if (!this.el.childOfName(`${key}_value`)) {
                this.el.add(new ZrText({
                    x: x! + LIGAND_WIDTH_HALF,
                    y: y! + LIGAND_WIDTH_HALF,
                    style: {
                        text: `=${formula.text}`,
                        ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.scriptLength + formula.style.padding[3] - formula.style.padding[1], 0 + formula.style.padding[0] - formula.style.padding[2]),
                        fill: this.style.default.fill,
                        lineHeight: LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT,
                        fontSize: '11px',
                    },
                    name: `${key}_value`,
                    zlevel: 5,
                }));
            } else {
                (this.el.childOfName(`${key}_value`) as any).attr({
                    x: x! + LIGAND_WIDTH_HALF,
                    y: y! + LIGAND_WIDTH_HALF,
                    style: {
                        text: `=${formula.text}`,
                        ...skew(position.x, position.y, vecX, vecY, formula.style.contentLength + formula.style.scriptLength + formula.style.padding[3] - formula.style.padding[1], 0 + formula.style.padding[0] - formula.style.padding[2]),
                        fill: this.style.default.fill,
                        lineHeight: LIGAND_TEXT_STYLE.INITIAL.LINE_HEIGHT,
                        fontSize: '11px',
                    },
                    name: `${key}_value`,
                    zlevel: Math.max(5, (this.el.childOfName(`${key}_value`) as any)?.zlevel || 0),
                })
            }
        } else {
            if (this.el.childOfName(`${key}_content`)) {
                this.el.remove(this.el.childOfName(`${key}_content`));
            }
            if (this.el.childOfName(`${key}_superscript`)) {
                this.el.remove(this.el.childOfName(`${key}_superscript`));
            }
            if (this.el.childOfName(`${key}_subscript`)) {
                this.el.remove(this.el.childOfName(`${key}_subscript`));
            }
            if (this.el.childOfName(`${key}_value`)) {
                this.el.remove(this.el.childOfName(`${key}_value`));
            }
        }
    }
}

export default LigandExpTextElement;
