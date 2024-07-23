class Vector {
    setValues(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    copy() {
        return new Vector(this.x, this.y);
    }

    add(v: Vector) {
        return new Vector(this.x + v.x, this.y + v.y);
    }

    sub(v: Vector) {
        return new Vector(this.x - v.x, this.y - v.y);
    }

    multiplyConst(c: number) {
        return new Vector(this.x * c, this.y * c);
    }

    divideConst(c: number) {
        return new Vector(this.x / c, this.y / c);
    }

    dot(v: Vector) {
        return this.x * v.x + this.y * v.y;
    }

    mag() {
        return Math.sqrt(this.dot(this));
    }

    normalize() {
        return this.divideConst(this.mag());
    }

    constructor(public x: number, public y: number) {}
}

export default Vector;
