import { Group, Text as ZrText } from 'zrender';
import { EdgeSubElement, DrawParams } from './subElement';
import { EDGE_TEXT_STYLE } from '../../constant';
import { formulaList, getFormulaText, rotateLineItem, skew, subscriptOffset, superscriptOffset } from '../../helper';

class EdgeTextElement extends EdgeSubElement {
    type = 'edgeTextNew';
    el = new Group({
        silent: true,
    })

    style = {
        virtual: {
            fill: EDGE_TEXT_STYLE.VIRTUAL.Fill,
        },
        selected: {
            fill: EDGE_TEXT_STYLE.SELECTED.Fill,
        },
        hover: {
            fill: EDGE_TEXT_STYLE.HOVER.Fill,
        },
        relatedHover: {
            fill: EDGE_TEXT_STYLE.RELATEDHOVER.Fill,
        },
        default: {
            fill: EDGE_TEXT_STYLE.DEFAULT.Fill,
        },
    };

    draw({ x, y, rotation, info, data }: DrawParams) {
        const res = rotateLineItem(x!, y!, rotation!, info!.length * 12);
        if (isNaN(res.rotation)) return;
        let num = 0;
        ['simScore', 'expDDG'].forEach(key => {
            if (info?.includes(key) && data[key]) {
                const formula = {
                    ...formulaList[key],
                    text: getFormulaText(key, data),
                }
                const vecX = { x: Math.cos(rotation!), y: -Math.sin(rotation!) };
                const vecY = { x: Math.cos(rotation! + Math.PI / 2), y: -Math.sin(rotation! + Math.PI / 2) };
                if (vecX.x < 0) {
                    vecX.x = -vecX.x;
                    vecX.y = -vecX.y;
                }
                if (vecY.y < 0) {
                    vecY.x = -vecY.x;
                    vecY.y = -vecY.y;
                }
                if (!this.el.childOfName(`${key}_content`)) {
                    this.el.add(new ZrText({
                        ...skew(res.x, res.y, vecX, vecY, 0, num * 18),
                        rotation: res.rotation,
                        style: {
                            text: formula.content,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                            ...this.style.default,
                        },
                        name: `${key}_content`
                    }));
                } else {
                    (this.el.childOfName(`${key}_content`) as any).attr({
                        ...skew(res.x, res.y, vecX, vecY, 0, num * 18),
                        rotation: res.rotation,
                        style: {
                            text: formula.content,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                        },
                        name: `${key}_content`
                    })
                }
                if (formula.superscript) {
                    if (!this.el.childOfName(`${key}_superscript`)) {
                        this.el.add(new ZrText({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, superscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.superscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                                ...this.style.default,
                            },
                            name: `${key}_superscript`
                        }));
                    } else {
                        (this.el.childOfName(`${key}_superscript`) as ZrText).attr({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, superscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.superscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                            },
                            name: `${key}_superscript`
                        })
                    }
                }
                if (formula.subscript) {
                    if (!this.el.childOfName(`${key}_subscript`)) {
                        this.el.add(new ZrText({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, subscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.subscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                                ...this.style.default,
                            },
                            name: `${key}_subscript`
                        }));
                    } else {
                        (this.el.childOfName(`${key}_subscript`) as ZrText).attr({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, subscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.subscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                            },
                            name: `${key}_subscript`
                        })
                    }
                }
                if (!this.el.childOfName(`${key}_value`)) {
                    this.el.add(new ZrText({
                        ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength + formula.style.scriptLength, 0 + num * 18),
                        rotation: res.rotation,
                        style: {
                            text: `=${formula.text}`,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                            ...this.style.default,
                        },
                        name: `${key}_value`
                    }));
                } else {
                    (this.el.childOfName(`${key}_value`) as ZrText).attr({
                        ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength + formula.style.scriptLength, 0 + num * 18),
                        rotation: res.rotation,
                        style: {
                            text: `=${formula.text}`,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                        },
                        name: `${key}_value`
                    });
                }
                num++;
            } else {
                if (this.el.childOfName(`${key}_content`)) {
                    this.el.remove(this.el.childOfName(`${key}_content`));
                }
                if (this.el.childOfName(`${key}_superscript`)  ) {
                    this.el.remove(this.el.childOfName(`${key}_superscript`)  );
                }
                if (this.el.childOfName(`${key}_subscript`)) {
                    this.el.remove(this.el.childOfName(`${key}_subscript`));
                }
                if (this.el.childOfName(`${key}_value`)) {
                    this.el.remove(this.el.childOfName(`${key}_value`));
                }
            }
        });
    }
}

export default EdgeTextElement;
