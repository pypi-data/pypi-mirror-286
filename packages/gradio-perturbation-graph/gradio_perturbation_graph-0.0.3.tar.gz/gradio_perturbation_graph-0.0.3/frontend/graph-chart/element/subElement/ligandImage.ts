import { Image as ZrImage } from 'zrender';
import { LigandSubElement, MoveToParams } from './subElement';
import { LIGAND_IMAGE_STYLE } from '../../constant';

class LigandImageElement extends LigandSubElement {
    type = 'ligandImage';

    el = new ZrImage();

    style = {
        selected: {},
        hover: {},
        relatedHover: {},
        firstAdd: {},
        default: {},
    };

    moveTo({ x, y, originX, originY }: MoveToParams) {
        this.el.attr({
            originX,
            originY,
            style: {
                x: x! + LIGAND_IMAGE_STYLE.POSITION.OFFSET,
                y: y! + LIGAND_IMAGE_STYLE.POSITION.OFFSET,
            },
        });
    }

    constructor(img: string) {
        super();

        this.el.attr({
            style: {
                image: img,
                width: LIGAND_IMAGE_STYLE.INITIAL.WIDTH,
                height: LIGAND_IMAGE_STYLE.INITIAL.HEIGHT,
            },
            z2: LIGAND_IMAGE_STYLE.INITIAL.ZLEVEL_THIRD,
        });
    }
}

export default LigandImageElement;
