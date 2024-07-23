import Graph from './graph';
import Vector from './vector';

const MAX_ITERS = 400;

class FRLayout {
    graph!: Graph;
    width!: number;
    height!: number;
    area!: number;
    distConst = 1;
    iterStep = 0.1;
    optDist = 0;
    temp = 0;
    currIter = 0;

    attraction(d: number) {
        return Math.pow(d, 2) / this.optDist;
    }

    repulsion(d: number) {
        return Math.pow(this.optDist, 2) / d;
    }

    centerAttraction(d: number, scale = 1) {
        return (Math.pow(d, 2) / this.optDist) * scale;
    }

    calcAttraction() {
        this.graph.forEachEdge((u, v) => {
            if (!u || !v) return;
            var delta = u.pos.sub(v.pos);
            var len = delta.mag() / 3;
            var distVec = delta.normalize().multiplyConst(this.attraction(len));

            u.disp = u.disp.sub(distVec);
            v.disp = v.disp.add(distVec);
        });

        const center = new Vector(this.width / 2, this.height / 2);

        this.graph.forEachVertex(u => {
            if (!u) return;
            const cp = u.pos.copy();
            const scale = u.edgeNum ? cp.sub(center).mag() / 200 : 1;
            var delta = u.pos.sub(center),
                distVec = delta.normalize().multiplyConst(this.centerAttraction(delta.mag(), scale));

            u.disp = u.disp.sub(distVec);
        });
    }

    calcRepulsion() {
        this.graph.forEachVertex(u => {
            if (!u) return;
            u.disp.setValues(0.0, 0.0);

            this.graph.forEachVertex(v => {
                if (!v) return;
                var delta;

                if (!u.equals(v)) {
                    delta = u.pos.sub(v.pos);
                    if (!delta.x && !delta.y) return;
                    u.disp = u.disp.add(delta.normalize().multiplyConst(this.repulsion(delta.mag())));
                }
            });
        });
    }

    calcDisplacement() {
        this.graph.forEachVertex(v => {
            if (!v) return;
            v.pos = v.pos.add(v.disp.normalize().multiplyConst(Math.min(v.disp.mag() / 100, this.temp * 0.1)));
            const spare = 0.1;
            const minW = this.width * spare;
            const maxW = this.width * (1 - spare);
            const minH = this.height * spare;
            const maxH = this.height * (1 - spare);
            v.pos.x = Math.min(maxW, Math.max(minW, v.pos.x));
            v.pos.y = Math.min(maxH, Math.max(minH, v.pos.y));
        });
    }

    cool() {
        this.temp *= 1 - this.currIter / MAX_ITERS;
    }

    updatePhysics(isCalc?: boolean) {
        this.currIter += this.iterStep;
        if (isCalc) {
            this.calcRepulsion();
            this.calcAttraction();
            this.calcDisplacement();
        }

        this.cool();
    }

    isDone() {
        return this.temp < 0.1 || this.currIter > MAX_ITERS;
    }

    reset() {
        this.optDist = this.distConst * Math.sqrt(this.area / this.graph.getSize());
        this.temp = this.width / 10;
        this.currIter = 0;
    }
    
    resize(width: number, height: number, graph: Graph) {
        this.graph = graph;
        this.width = width;
        this.height = height;
        this.area = this.width * this.height;
        this.reset();
    }

    constructor(width: number, height: number, graph: Graph) {
        this.graph = graph;
        this.width = width;
        this.height = height;
        this.area = this.width * this.height;

        this.reset();
    }
}

export default FRLayout;
