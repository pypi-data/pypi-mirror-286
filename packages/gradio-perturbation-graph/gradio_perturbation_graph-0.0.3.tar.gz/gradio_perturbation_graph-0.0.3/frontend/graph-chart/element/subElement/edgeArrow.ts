import { Path } from 'zrender';
import { EdgeSubElement, DrawParams } from './subElement';
import { EDGE_ARROW_STYLE } from '../../constant';

const Arrow = Path.extend({
    type: 'arrow',
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

class EdgeArrowElement extends EdgeSubElement {
    type = 'edgeArrow';
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
            fill: EDGE_ARROW_STYLE.VIRTUAL.FILL,
        },
        selected: {
            fill: EDGE_ARROW_STYLE.SELECTED.FILL,
        },
        hover: {
            fill: EDGE_ARROW_STYLE.HOVER.FILL,
        },
        relatedHover: {
            fill: EDGE_ARROW_STYLE.RELATEDHOVER.FILL,
        },
        default: {
            fill: EDGE_ARROW_STYLE.DEFAULT.FILL,
        },
    };

    draw({ x2, y2, rotation }: DrawParams): void {
        this.el.attr({
            rotation: rotation! - Math.PI * 0.5,
            originX: x2,
            originY: y2,
            shape: {
                x: x2,
                y: y2,
            },
        });
    }
}

export default EdgeArrowElement;
