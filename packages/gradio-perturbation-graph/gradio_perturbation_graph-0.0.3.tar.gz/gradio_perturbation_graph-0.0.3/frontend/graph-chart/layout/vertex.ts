import Vector from './vector';

class Vertex {
    edgeNum = 0;
    pos!: Vector;
    disp = new Vector(0, 0);

    equals(v: Vertex) {
        return this.id === v.id;
    }

    constructor(public id: string, x: number = 0, y: number = 0) {
        this.pos = new Vector(x, y);
    }
}

export default Vertex;
