import { DisplayableProps, Path } from 'zrender';
import { EdgeSubElement, DrawParams, ElementStateEnum } from './subElement';
import { EDGE_ARROW_STYLE, EDGE_LINE_STYLE } from '../../constant';
import { Vec2 } from '../../vec2';
import { getRotation, reliabilityColorFill } from '../../helper';

const Arrow = Path.extend({
    type: 'Arrow',
    shape: {
        x: 0,
        y: 0,
        width: 0,
        height: 0,
    },
    buildPath: function (ctx, shape) {
        const height = shape.height;
        const width = shape.width;
        const x = shape.x;
        const y = shape.y;
        const dx = (width / 3) * 2;
        ctx.moveTo(x, y);
        ctx.lineTo(x + dx, y + height);
        ctx.lineTo(x, y + (height / 4) * 3);
        ctx.lineTo(x - dx, y + height);
        ctx.lineTo(x, y);
        ctx.closePath();
    },
});

class HistoryEdgeArrowElement extends EdgeSubElement {
    type = 'jobArrow';
    el = new Arrow({
        shape: {
            x: 0,
            y: 0,
            width: EDGE_ARROW_STYLE.INITIAL.WIDTH,
            height: EDGE_ARROW_STYLE.INITIAL.HEIGHT,
        },
    });

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

    draw({ x1, y1, x2, y2, confidence, order, offsetVec, historyForce }: DrawParams): void {
        const style: DisplayableProps['style'] = {
            opacity: historyForce ? 1 : 0.4,
            stroke: EDGE_LINE_STYLE.DEFAULT.STROKE,
            fill: EDGE_LINE_STYLE.DEFAULT.STROKE,
            // stroke: reliabilityColorFill(confidence!),
            // fill: reliabilityColorFill(confidence!),
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
        const yPoint = Vec2.create(x2! + (order!) * oVec[0], y2! + (order!) * oVec[1]);
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
        const rotation = getRotation({x: cpy[0], y: cpy[1]}, {x: yPoint[0], y: yPoint[1]});
        // const direction = Vec2.create(0, 0);
        // Vec2.sub(direction, yPoint, cpy);
        // Vec2.normalize(direction, direction);
        // Vec2.scale(direction, direction, 10);
        this.el.attr({
            style,
            rotation: rotation - Math.PI * 0.5,
            originX: yPoint[0],
            originY: yPoint[1],
            shape: {
                x: yPoint[0],
                y: yPoint[1],
            },
        });
    }
}

export default HistoryEdgeArrowElement;
