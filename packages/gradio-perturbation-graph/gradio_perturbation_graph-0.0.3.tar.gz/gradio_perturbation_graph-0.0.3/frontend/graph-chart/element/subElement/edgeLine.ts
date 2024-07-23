import { Line as ZrLine } from 'zrender';
import { DisplayableProps } from 'zrender/lib/graphic/Displayable';
import { EdgeSubElement, DrawParams } from './subElement';
import { EDGE_LINE_STYLE } from '../../constant';

class EdgeLineElement extends EdgeSubElement {
    type = 'edgeLine';
    el = new ZrLine();

    style = {
        virtual: {
            stroke: EDGE_LINE_STYLE.VIRTUAL.STROKE,
        },
        selected: {
            stroke: EDGE_LINE_STYLE.SELECTED.STROKE,
        },
        hover: {
            stroke: EDGE_LINE_STYLE.HOVER.STROKE,
        },
        relatedHover: {
            stroke: EDGE_LINE_STYLE.RELATEDHOVER.STROKE,
        },
        default: {
            stroke: EDGE_LINE_STYLE.DEFAULT.STROKE,
        },
    };

    draw({ x1, y1, x2, y2, virtual }: DrawParams) {
        const style: DisplayableProps['style'] = {
            lineWidth: EDGE_LINE_STYLE.INITIAL.LINEWIDTH,
            lineDash: EDGE_LINE_STYLE.INITIAL.LINEDASH,
        };
        if (virtual) {
            style.lineDash = EDGE_LINE_STYLE.INITIAL.VISUAL_LINEDASH;
        }
        this.el.attr({
            style,
            shape: {
                x1,
                y1,
                x2,
                y2,
            },
        });
    }
}

export default EdgeLineElement;
