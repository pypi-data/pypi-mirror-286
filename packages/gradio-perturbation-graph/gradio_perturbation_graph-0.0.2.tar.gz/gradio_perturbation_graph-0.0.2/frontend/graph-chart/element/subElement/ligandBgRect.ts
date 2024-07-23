import { Rect } from 'zrender';
import { DisplayableProps } from 'zrender/lib/graphic/Displayable';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_BGRECT_STYLE, ANIMATE_CONFIG, FADEOUT_OPACITY } from '../../constant';
import { getOpacityColor } from '../../helper';

class LigandBgRectElement extends LigandSubElement {
    type = 'ligandBgRect';

    el = new Rect({
        style: {
            fill: LIGAND_BGRECT_STYLE.INITIAL.FILL,
            lineWidth: LIGAND_BGRECT_STYLE.INITIAL.LINEWIDTH,
        },
        shape: {
            r: LIGAND_BGRECT_STYLE.INITIAL.RADIUS,
            width: LIGAND_BGRECT_STYLE.INITIAL.WIDTH,
            height: LIGAND_BGRECT_STYLE.INITIAL.HEIGHT,
        },
        z2: LIGAND_BGRECT_STYLE.INITIAL.ZLEVEL_THIRD,
    });

    style = {
        selected: {
            shadowColor: LIGAND_BGRECT_STYLE.SELECTED.SHADOWCOLOR,
            shadowBlur: LIGAND_BGRECT_STYLE.SELECTED.SHADOWBLUR,
        },
        hover: {
            shadowColor: LIGAND_BGRECT_STYLE.HOVER.SHADOWCOLOR,
            shadowBlur: LIGAND_BGRECT_STYLE.HOVER.SHADOWBLUR,
        },
        relatedHover: {
            shadowBlur: LIGAND_BGRECT_STYLE.RELATEDHOVER.SHADOWBLUR,
        },
        firstAdd: {
            shadowColor: LIGAND_BGRECT_STYLE.FIRSTADD.SHADOWCOLOR,
            shadowBlur: LIGAND_BGRECT_STYLE.FIRSTADD.SHADOWBLUR,
        },
        default: {
            shadowBlur: LIGAND_BGRECT_STYLE.DEFAULT.SHADOWBLUR,
        },
    };

    fadein() {
        const style: DisplayableProps['style'] = this.style[this.state];
        this.el.animateTo(
            {
                style,
            },
            ANIMATE_CONFIG
        );
    }
    fadeout() {
        const style: DisplayableProps['style'] = this.style[this.state];
        if (!style.shadowBlur) return;

        style.shadowColor = getOpacityColor(style.shadowColor, FADEOUT_OPACITY);
        this.el.animateTo(
            {
                style,
            },
            ANIMATE_CONFIG
        );
    }

    moveTo({ x, y, originX, originY }: MoveToParams): void {
        this.el.attr({
            originX,
            originY,
            shape: {
                x,
                y,
            },
        });
    }
}

export default LigandBgRectElement;
