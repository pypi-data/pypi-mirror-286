import { BezierCurve } from 'zrender';
import { DisplayableProps } from 'zrender/lib/graphic/Displayable';
import { EdgeSubElement, DrawParams, ElementStateEnum } from './subElement';
import { EDGE_LINE_STYLE } from '../../constant';
import { Vec2 } from '../../vec2';
// import { reliabilityColorFill } from '../../helper';

class HistoryEdgeLineElement extends EdgeSubElement {
    type = 'jobLine';
    el = new BezierCurve();

    style = {
        virtual: {
            opacity: 0.4,
        },
        selected: {
            opacity: 0.4,
        },
        hover: {
            opacity: 0.4,
        },
        relatedHover: {
            opacity: 0.4,
        },
        default: {
            opacity: 0.4,
        },
    };

    draw({ x1, y1, x2, y2, confidence, order, offsetVec, historyForce }: DrawParams) {
        const style: DisplayableProps['style'] = {
            lineWidth: EDGE_LINE_STYLE.INITIAL.LINEWIDTH,
            lineDash: historyForce && confidence !== 0 ? null : 4,
            opacity: historyForce ? 1 : 0.4,
            stroke: EDGE_LINE_STYLE.DEFAULT.STROKE,
            // stroke: reliabilityColorFill(confidence!),
        };

        Object.keys(this.style).forEach((key) => {
            if (historyForce) {
                this.style[key as ElementStateEnum].opacity = 1;
            }
        })

        const verticalVec1 = Vec2.create(-(y2! - y1!), x2! - x1!);

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
        this.el.attr({
            style,
            shape: {x1: xPoint[0], y1: xPoint[1], x2: yPoint[0], y2: yPoint[1], cpx1: cpy[0], cpy1: cpy[1] },
        });
    }
}

export default HistoryEdgeLineElement;
