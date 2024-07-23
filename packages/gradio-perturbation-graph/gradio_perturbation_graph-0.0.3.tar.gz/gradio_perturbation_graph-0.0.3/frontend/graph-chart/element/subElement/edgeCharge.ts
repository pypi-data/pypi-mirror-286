import { Image as ZrImage} from 'zrender';
import { EdgeSubElement, DrawParams } from './subElement';
import { rotateLineItem, skew } from '../../helper';

class EdgeChargeElement extends EdgeSubElement {
    type = 'edgeCharge';
    el = new ZrImage()

    style = {
        virtual: {},
        selected: {},
        hover: {},
        relatedHover: {},
        default: {},
    };

    draw({ x, y, rotation, info }: DrawParams) {
        const res = rotateLineItem(x!, y!, rotation!, (info!.length > 0 ? info!.length : 1) * 12);
        const vecX = { x: Math.cos(rotation!), y: -Math.sin(rotation!) };
        const vecY = { x: Math.cos(rotation! + Math.PI / 2), y: -Math.sin(rotation! + Math.PI / 2) };
        if (vecX.x < 0) {
            vecX.x = -vecX.x;
            vecX.y = -vecX.y;
        }
        // if (vecY.y < 0) {
        //     vecY.x = -vecY.x;
        //     vecY.y = -vecY.y;
        // }
        const position = skew(res.x, res.y, vecX, vecY, (info?.length || 0) > 0 ? -60 : 0, (info?.length || 0) <= 0 ? 16 : 0);
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

export default EdgeChargeElement;
