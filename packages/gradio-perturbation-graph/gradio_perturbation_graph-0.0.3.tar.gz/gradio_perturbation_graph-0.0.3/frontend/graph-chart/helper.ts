import { vector } from 'zrender';

interface Point {
    x: number;
    y: number;
}
export const superscriptOffset = -5;
export const subscriptOffset = 3;
/*
 * 公式列表
 */
export const formulaList: { [key: string]: any } = {
    expDG: {
        content: 'ΔG',
        subscript: 'Exp',
        style: {
            contentLength: 20,
            scriptLength: 15,
            padding: [0, 0, 0, 25]
        }
    },
    predDG: {
        content: 'ΔG',
        subscript: 'FEP',
        style: {
            contentLength: 20,
            scriptLength: 15,
            padding: [0, 0, 0, 25]
        }
    },
    predDGErr: {
        content: 'Calc.Error',
        style: {
            contentLength: 50,
            scriptLength: 0,
            padding: [0, 0, 0, 25]
        }
    },
    simScore: {
        content: 'Similarity Score',
        style: {
            contentLength: 65,
            scriptLength: 0,
        }
    },
    expDDG: {
        content: 'ΔΔG',
        subscript: 'Exp',
        style: {
            contentLength: 20,
            scriptLength: 38,
        }
    },
    predDDG: {
        content: 'ΔΔG',
        subscript: 'FEP',
        superscript: '(raw)',
        style: {
            contentLength: 23,
            scriptLength: 55,
        }
    },
    predDDGCycleClosure: {
        content: 'ΔΔG',
        subscript: 'FEP',
        superscript: '(corrected)',
        style: {
            contentLength: 20,
            scriptLength: 50,
        }
    },
};
/*
 * 获取公式对应的数值
 */
export const getFormulaText = (key: string, data: any) => {
    switch (key) {
        case 'expDG':
            return `${data.expDG.toFixed(3)}`;
        case 'predDG':
            return `${data.predDG.toFixed(3)}`;
        case 'predDGErr':
            return `${data.predDGErr.toFixed(3)}`;
        case 'simScore':
            return `${data.simScore.toFixed(3)}`;
        case 'expDDG':
            return `${data.expDDG.toFixed(3)}`;
        case 'predDDG':
            return `${data.predDDG.toFixed(3)}±${data.predDDGErr.toFixed(3)}`;
        case 'predDDGCycleClosure':
            return `${data.predDDGCycleClosure.toFixed(3)}±${data.predDDGCycleClosureErr.toFixed(3)}`;
        default:
            return ''
    }
}
/*
 * 位置偏移
 */
export const skew = (x: number, y: number, skewVecX: { x: number, y: number }, skewVecY: { x: number, y: number }, skewXDistance: number, skewYDistance: number) => {
    return {
        x: x + skewXDistance * skewVecX.x + skewYDistance * skewVecY.x,
        y: y + skewXDistance * skewVecX.y + skewYDistance * skewVecY.y,
    }
};
/**
 * 将十六进制颜色转换为相同色值的rgba格式，并赋予透明度
 * @param color 十六进制的颜色
 * @param opacity 透明度
 * @returns rgba格式的颜色
 */
export function getOpacityColor(color: string, opacity: number): string {
    let theColor = color.toLowerCase();
    //十六进制颜色值的正则表达式
    const r = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;
    // 如果是16进制颜色
    if (theColor && r.test(theColor)) {
        if (theColor.length === 4) {
            let sColorNew = '#';
            for (let i = 1; i < 4; i += 1) {
                sColorNew += theColor.slice(i, i + 1).concat(theColor.slice(i, i + 1));
            }
            theColor = sColorNew;
        }
        //处理六位的颜色值
        const sColorChange = [];
        for (let i = 1; i < 7; i += 2) {
            sColorChange.push(parseInt('0x' + theColor.slice(i, i + 2)));
        }
        return 'rgba(' + sColorChange.join(',') + ',' + opacity + ')';
    }
    return theColor;
}

/**
 * 根据两个矩形的中心点与边长，获取中心店连线与两个矩形边的交点
 * @param sLigand 起点矩形的中心坐标
 * @param tLigand 终点矩形的中心坐标
 * @param width 矩形的边长
 * @returns 两个交点的坐标值
 */
export function getEdgePoint(sLigand: Point, tLigand: Point, width: number) {
    const sAngle = getAngle(sLigand, tLigand);
    const tAngle = getAngle(tLigand, sLigand);
    const { edge: sEdge, approachEdge: sApproachEdge } = getEdge(sAngle, sLigand, width);
    const { edge: tEdge, approachEdge: tApproachEdge } = getEdge(tAngle, tLigand, width);
    const { start, end } = edgeMove(sLigand, tLigand);
    const sPoint =
        segmentsIntr(start, end, sEdge!.start, sEdge!.end) ||
        segmentsIntr(start, end, sApproachEdge!.start, sApproachEdge!.end);
    let offsetVec = { x: tEdge!.end.x - tEdge!.start.x, y: tEdge!.end.y - tEdge!.start.y };
    let tPoint = segmentsIntr(start, end, tEdge!.start, tEdge!.end)
    if (!tPoint) {
        tPoint = segmentsIntr(start, end, tApproachEdge!.start, tApproachEdge!.end);
        offsetVec = { x: tApproachEdge!.end.x - tApproachEdge!.start.x, y: tApproachEdge!.end.y - tApproachEdge!.start.y }
    }
    const { x: x1, y: y1 } = sPoint as Point;
    const { x: x2, y: y2 } = tPoint as Point;
    return { x1, y1, x2, y2, offsetVec };
}

/**
 * 获取一条线上文字的位置与旋转信息
 * @param x1 起点x
 * @param y1 起点y
 * @param x2 终点x
 * @param y2 终点y
 * @param n 文字所在的行数
 * @returns 文字的坐标点与旋转值
 */
export function getTextPosition(x1: number, y1: number, x2: number, y2: number, n: number) {
    const vecX = x2 - x1;
    const vecY = y2 - y1;
    const move = 14;
    const dis = vecMove(vecX, vecY, move);
    // const dis = { x: 0, y: 0 };
    const x = (x2 - x1) / 2 + x1;
    const y = (y2 - y1) / 2 + y1;
    const rotation = getRotation({ x: x1, y: y1 }, { x: x2, y: y2 });
    return {
        x: x + dis.x * n,
        y: y - dis.y * n,
        rotation,
    };
}

/**
 * 获取画布中的一个随机坐标值
 * @param width 画布的宽度
 * @param height 画布的高度
 * @param isCenter 是否需要在出现在画布中间
 * @returns 位置坐标
 */
export function getInitialPos(width: number, height: number, isCenter: boolean) {
    const startX = width / 6;
    const midX = startX * 3;
    const endX = startX * 5;
    const startY = height / 6;
    const midY = startY * 3;
    const endY = startY * 5;
    if (isCenter) {
        return {
            x: random(startX, endX),
            y: random(startY, endY),
        };
    }
    let x = random(0, width);
    let y = random(0, height);
    if (x > startX && x < midX) x -= startX;
    if (x > midX && x < endX) x += startX;
    if (y > startY && y < midY) y -= startY;
    if (y > midY && y < endY) y += startY;
    return {
        x,
        y,
    };
}

/**
 * 获取两点的旋转值
 * @param start 起点
 * @param end 终点
 * @returns 旋转值
 */
export function getRotation(start: Point, end: Point) {
    const radian = Math.atan2(start.y - end.y, start.x - end.x);
    const rotation = Math.PI - radian;
    return rotation;
}

/**
 * 获取两点的角度
 * @param start 起点
 * @param end 终点
 * @returns 角度
 */
function getAngle(start: Point, end: Point) {
    const radian = Math.atan2(start.y - end.y, start.x - end.x) || 0;
    const angle = 180 - radian * (180 / Math.PI);

    return angle;
}

/**
 * 获取两个矩形之间可能会相交的边
 * @param angel 角度
 * @param pos 起点位置
 * @param width 矩形边长
 * @returns 最可能会相交的边与次可能会相交的边
 */
function getEdge(angel: number, pos: Point, width: number) {
    const edgeArea = Math.floor(angel / 45);
    const edgeList = [
        ['right', 'up'],
        ['up', 'right'],
        ['up', 'left'],
        ['left', 'up'],
        ['left', 'down'],
        ['down', 'left'],
        ['down', 'right'],
        ['right', 'down'],
    ];
    const resEdge = edgeList[edgeArea];
    return {
        edge: getSpecificEdge(pos, width, resEdge[0]),
        approachEdge: getSpecificEdge(pos, width, resEdge[1]),
    };
}

/**
 * 获取矩形指定的边
 * @param pos 中心点
 * @param width 边长
 * @param type 类型
 * @returns 边的起点与终点
 */
function getSpecificEdge(pos: Point, width: number, type: string) {
    const l = width / 2;
    switch (type) {
        case 'up':
            return {
                start: {
                    x: pos.x - l,
                    y: pos.y - l,
                },
                end: {
                    x: pos.x + l,
                    y: pos.y - l,
                },
            };
        case 'left':
            return {
                start: {
                    x: pos.x - l,
                    y: pos.y - l,
                },
                end: {
                    x: pos.x - l,
                    y: pos.y + l,
                },
            };
        case 'down':
            return {
                start: {
                    x: pos.x - l,
                    y: pos.y + l,
                },
                end: {
                    x: pos.x + l,
                    y: pos.y + l,
                },
            };
        case 'right':
            return {
                start: {
                    x: pos.x + l,
                    y: pos.y - l,
                },
                end: {
                    x: pos.x + l,
                    y: pos.y + l,
                },
            };
    }
}

/**
 * 获取两条线的交点
 * @param a 第一条线的起点
 * @param b 第一条线的终点
 * @param c 第二条线的起点
 * @param d 第二条线的终点
 * @returns 交点坐标
 */
function segmentsIntr(a: Point, b: Point, c: Point, d: Point) {
    // 三角形abc 面积的2倍
    var area_abc = (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x);

    // 三角形abd 面积的2倍
    var area_abd = (a.x - d.x) * (b.y - d.y) - (a.y - d.y) * (b.x - d.x);

    // 面积符号相同则两点在线段同侧,不相交 (对点在线段上的情况,本例当作不相交处理);
    if (area_abc * area_abd >= 0) {
        return false;
    }

    // 三角形cda 面积的2倍
    var area_cda = (c.x - a.x) * (d.y - a.y) - (c.y - a.y) * (d.x - a.x);
    // 三角形cdb 面积的2倍
    // 注意: 这里有一个小优化.不需要再用公式计算面积,而是通过已知的三个面积加减得出.
    var area_cdb = area_cda + area_abc - area_abd;
    if (area_cda * area_cdb >= 0) {
        return false;
    }

    //计算交点坐标
    var t = area_cda / (area_abd - area_abc);
    var dx = t * (b.x - a.x),
        dy = t * (b.y - a.y);
    return { x: a.x + dx, y: a.y + dy };
}

function edgeMove(sLigand: Point, tLigand: Point) {
    const vecX = tLigand.x - sLigand.x;
    const vecY = tLigand.y - sLigand.y;
    const dis = vecMove(vecX, vecY, 10);
    return {
        start: {
            x: sLigand.x + dis.x,
            y: sLigand.y - dis.y,
        },
        end: {
            x: tLigand.x + dis.x,
            y: tLigand.y - dis.y,
        },
    };
}

/**
 * 矢量移动
 * @param vecX 坐标值-x
 * @param vecY 坐标值-y
 * @param move 移动的距离
 * @returns 移动后的坐标
 */
function vecMove(vecX: number, vecY: number, move: number) {
    const vecLen = vector.len([vecX, vecY]);
    const vecResX = (vecY / vecLen) * move;
    const vecResY = (vecX / vecLen) * move;
    return { x: vecResX, y: vecResY };
}

/**
 * 指定一个范围，获取范围内的一个随机值
 * @param min 最小值
 * @param max 最大值
 * @returns 随机值
 */
function random(min: number, max: number) {
    return Math.floor(Math.random() * (max - min)) + min;
}

export function moveByRotation(x: number, y: number, rotation: number, dis: number) {
    const sinVal = Math.sin(Math.PI - rotation);
    const cosVal = Math.cos(Math.PI - rotation);

    y += sinVal * dis;
    x += cosVal * dis;

    return { x, y, rotation };
}

export function rotateLineItem(x: number, y: number, rotation: number, dis: number) {
    const min = Math.PI * 0.5;
    const max = Math.PI * 1.5;
    if (rotation > min && rotation < max) {
        if (rotation > Math.PI) {
            rotation -= Math.PI;
            return {
                ...moveByRotation(x, y, rotation - Math.PI / 2, dis),
                rotation,
            };
        } else {
            rotation += Math.PI;
            return {
                ...moveByRotation(x, y, rotation - Math.PI / 2, dis),
                rotation,
            };
        }
    }
    return { x, y, rotation };
}

export const reliabilityColorFill = (confidence: number) => {
    switch(confidence) {
        case 1:
            return '#63A1FF'
        case 2:
            return '#F0AE60';
        case 3:
            return '#FA6666';
        default:
            return '#B1B4D3';
    }
}
