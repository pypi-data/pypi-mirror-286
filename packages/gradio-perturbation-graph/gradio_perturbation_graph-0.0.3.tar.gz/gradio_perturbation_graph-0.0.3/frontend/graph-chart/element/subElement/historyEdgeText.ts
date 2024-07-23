import { Vec2 } from '../../vec2';
import { Text as ZrText, Group } from 'zrender';
import { EDGE_TEXT_STYLE } from '../../constant';
import { formulaList, getFormulaText, reliabilityColorFill, rotateLineItem, skew, subscriptOffset, superscriptOffset } from '../../helper';
import { EdgeSubElement, DrawParams } from './subElement';

class HistoryEdgeTextElement extends EdgeSubElement {
    type = 'historyText';
    el = new Group();

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

    draw({ x1, y1, x2, y2, order, rotation, offsetVec, data, confidence }: DrawParams) {
        const verticalVec1 = Vec2.create(-(y2! - y1!), x2! - x1!);

        // const stroke = reliabilityColorFill(confidence!);
        const oVec = Vec2.create(offsetVec!.x, offsetVec!.y);
        Vec2.normalize(oVec, oVec);
        if (offsetVec!.x === 0 && verticalVec1[1] > 0) {
            Vec2.scale(oVec, oVec, -1);
        }
        if (offsetVec!.y === 0 && verticalVec1[0] > 0) {
            Vec2.scale(oVec, oVec, -1);
        }
        Vec2.scale(oVec, oVec, 5);
        const xPoint = Vec2.create(x1!, y1!);
        const yPoint = Vec2.create(x2! + order! * oVec[0], y2! + order! * oVec[1]);
        const lineVec = Vec2.create(0, 0);
        Vec2.sub(lineVec, yPoint, xPoint);
        Vec2.normalize(lineVec, lineVec);
        const midPoint = Vec2.create(0, 0);
        Vec2.add(midPoint, yPoint, xPoint);
        Vec2.scale(midPoint, midPoint, 0.5);
        const verticalVec = Vec2.create(-lineVec[1], lineVec[0]);
        const reg = [Math.tan(Math.PI * 85 / 90), Math.tan(Math.PI * 80 / 90), Math.tan(Math.PI * 75 / 90), Math.tan(Math.PI * 70 / 90)];
        Vec2.scale(verticalVec, verticalVec, Vec2.distance(midPoint, xPoint) * reg[order!]);
        const cpy = Vec2.create(0, 0);
        Vec2.add(cpy, midPoint, verticalVec);

        const res = rotateLineItem(cpy[0]!, cpy[1]!, rotation!, ['simScore', 'expDDG', 'predDDG', 'predDDGCycleClosure'].filter(item => data[item] !== undefined)!.length * 12);

        if (isNaN(res.rotation)) return;
        let num = 0;
        ['simScore', 'expDDG', 'predDDG', 'predDDGCycleClosure'].forEach(key => {
            if (data[key]) {
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
                            // stroke,
                        },
                        name: `${key}_content`,
                        invisible: true,
                        silent: true,
                    }));
                } else {
                    (this.el.childOfName(`${key}_content`) as any).attr({
                        ...skew(res.x, res.y, vecX, vecY, 0, num * 18),
                        rotation: res.rotation,
                        style: {
                            text: formula.content,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                            // stroke,
                        },
                        name: `${key}_content`,
                        invisible: true,
                        silent: true,
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
                                // stroke,
                            },
                            name: `${key}_superscript`,
                            invisible: true,
                            silent: true,
                        }));
                    } else {
                        (this.el.childOfName(`${key}_superscript`) as ZrText).attr({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, superscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.superscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                                // stroke,
                            },
                            name: `${key}_superscript`,
                            invisible: true,
                            silent: true,
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
                                // stroke,
                            },
                            name: `${key}_subscript`,
                            invisible: true,
                            silent: true,
                        }));
                    } else {
                        (this.el.childOfName(`${key}_subscript`) as ZrText).attr({
                            ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength, subscriptOffset + num * 18),
                            rotation: res.rotation,
                            style: {
                                text: formula.subscript,
                                align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                                fontSize: 8,
                                // stroke,
                            },
                            name: `${key}_subscript`,
                            invisible: true,
                            silent: true,
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
                            // stroke,
                        },
                        name: `${key}_value`,
                        invisible: true,
                        silent: true,
                    }));
                } else {
                    (this.el.childOfName(`${key}_value`) as ZrText).attr({
                        ...skew(res.x, res.y, vecX, vecY, formula.style.contentLength + formula.style.scriptLength, 0 + num * 18),
                        rotation: res.rotation,
                        style: {
                            text: `=${formula.text}`,
                            align: EDGE_TEXT_STYLE.INITIAL.ALIGN,
                            // stroke,
                        },
                        name: `${key}_value`,
                        invisible: true,
                        silent: true,
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

export default HistoryEdgeTextElement;
