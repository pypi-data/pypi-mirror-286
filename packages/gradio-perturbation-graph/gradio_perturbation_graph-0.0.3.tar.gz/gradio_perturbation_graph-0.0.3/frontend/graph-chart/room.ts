import emitter, { EVENT_NAME } from './events/emitter';

// 每个分子需要使用的面积 => 1000px * 1000px 的尺寸下容纳 20 个分子
const baseMolNum = 20;
const baseArea = (1000 * 1000) / baseMolNum;

interface TransformParams {
    translateX?: number;
    translateY?: number;
    scale?: number;
}

class Room {
    parentWidth = 0;
    parentHeight = 0;
    width = 0;
    height = 0;
    scale = 1;
    maxScale = 2;
    minScale = 1;
    otx = 0;
    oty = 0;
    translateX = 0;
    translateY = 0;

    init(len: number) {
        this.parentWidth = this.parent.offsetWidth;
        this.parentHeight = this.parent.offsetHeight;
        const parentArea = this.parentWidth * this.parentHeight;
        const molNum = Math.floor(parentArea / baseArea);
        const molScale = len / molNum;

        if (molScale < 1) {
            this.width = this.parentWidth;
            this.height = this.parentHeight;
            this.scale = 1;
        } else {
            const edgeScale = Math.sqrt(molScale);
            this.scale = 1 / edgeScale;
            this.minScale = 1 / edgeScale;
            this.width = this.parentWidth * edgeScale;
            this.height = this.parentHeight * edgeScale;
        }

        this.otx = -this.width / 2;
        this.oty = -this.height / 2;
        this.dom.style.width = this.width + 'px';
        this.dom.style.height = this.height + 'px';
        this.transform({ translateX: this.otx, translateY: this.oty });
    }

    // 放大
    zoomIn(delta: number) {
        if (this.scale === this.maxScale) return;
        this.scale += delta / 100;
        if (this.scale > this.maxScale) this.scale = this.maxScale;
        this.transform();
        this.onZoomChange();
    }

    // 缩小
    zoomOut(delta: number) {
        if (this.scale <= this.minScale) return;
        this.scale += delta / 100;
        if (this.scale < this.minScale) this.scale = this.minScale;
        this.checkTransPosition();
        this.transform();
        this.onZoomChange();
    }

    move(x: number, y: number) {
        if (this.scale <= this.minScale) return;
        this.translateX -= x;
        this.translateY -= y;
        this.checkTransPosition();
        this.transform();
    }

    checkTransPosition() {
        const width = this.width * this.scale;
        const height = this.height * this.scale;
        const disX = (width - this.parentWidth) / 2;
        const disY = (height - this.parentHeight) / 2;
        const maxX = this.otx + disX;
        const minX = this.otx - disX;
        const maxY = this.oty + disY;
        const minY = this.oty - disY;
        if (this.translateX < minX) this.translateX = minX;
        if (this.translateX > maxX) this.translateX = maxX;
        if (this.translateY < minY) this.translateY = minY;
        if (this.translateY > maxY) this.translateY = maxY;
    }

    onZoomChange() {
        emitter.emit(EVENT_NAME.ZOOM_CHANGE, this.scale, this.minScale, this.maxScale);
    }

    transform(params: TransformParams = {}) {
        const { translateX = this.translateX, translateY = this.translateY, scale = this.scale } = params;
        this.translateX = translateX;
        this.translateY = translateY;
        this.scale = scale;
        this.dom.style.transform = `translate(${this.translateX}px, ${this.translateY}px) scale(${this.scale})`;
    }

    constructor(public parent: HTMLElement, public dom: HTMLElement) {}
}

export default Room;
