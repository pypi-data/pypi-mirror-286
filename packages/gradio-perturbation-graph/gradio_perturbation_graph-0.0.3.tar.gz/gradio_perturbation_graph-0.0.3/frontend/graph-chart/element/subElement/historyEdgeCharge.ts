import { Image as ZrImage} from 'zrender';
import { EdgeSubElement, DrawParams } from './subElement';
import { rotateLineItem, skew } from '../../helper';
import { Vec2 } from '../../vec2';

class HistoryEdgeChargeElement extends EdgeSubElement {
    type = 'historyEdgeCharge';
    el = new ZrImage()

    style = {
        virtual: {},
        selected: {},
        hover: {},
        relatedHover: {},
        default: {},
    };

    draw({ x1, y1, x2, y2, order, rotation, offsetVec, data, confidence }: DrawParams) {
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
        const yPoint = Vec2.create(x2!, y2!);
        const lineVec = Vec2.create(0, 0);
        Vec2.sub(lineVec, yPoint, xPoint);
        Vec2.normalize(lineVec, lineVec);
        const midPoint = Vec2.create(0, 0);
        Vec2.add(midPoint, yPoint, xPoint);
        Vec2.scale(midPoint, midPoint, 0.5);
        const verticalVec = Vec2.create(-lineVec[1], lineVec[0]);
        Vec2.scale(verticalVec, verticalVec, Vec2.distance(midPoint, xPoint) * Math.tan(Math.PI * 87 / 90));
        const cpy = Vec2.create(0, 0);
        Vec2.add(cpy, midPoint, verticalVec);

        const res = rotateLineItem(cpy[0]!, cpy[1]!, rotation!, -2);

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
        const position = skew(res.x, res.y, vecX, vecY, 0, 0)
        this.el.attr({
            rotation: res.rotation,
            originX: position.x,
            originY: position.y,
            style: {
                ...position,
            },
        });
    }

    constructor(img: string) {
        super();

        this.el.attr({
            style: {
                image: img,
                width: 8,
                height: 10,
            },
        });
    }
}

export default HistoryEdgeChargeElement;
