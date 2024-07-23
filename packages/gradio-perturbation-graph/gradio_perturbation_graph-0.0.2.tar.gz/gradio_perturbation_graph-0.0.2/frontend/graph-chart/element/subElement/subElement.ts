import { Element, Group } from 'zrender';
import { DisplayableProps } from 'zrender/lib/graphic/Displayable';

import { FADEOUT_OPACITY, NORMAL_OPACITY, ANIMATE_CONFIG, SCALE_X, SCALE_1 } from '../../constant';

export interface DrawParams {
    x?: number;
    y?: number;
    x1?: number;
    y1?: number;
    x2?: number;
    y2?: number;
    confidence?: number;
    rotation?: number;
    info?: Array<string>;
    virtual?: boolean;
    order?: number;
    offsetVec?: {
        x: number;
        y: number;
    };
    historyForce?: boolean;
    data?: any;
}

export interface MoveToParams {
    x?: number;
    y?: number;
    originX?: number;
    originY?: number;
    info?: Array<string>;
    exp?: string;
    calc_data?: string;
    calc_error?: string;
    name?: string;
}

export enum ElementStateEnum {
    Selected = 'selected',
    Hover = 'hover',
    RelatedHover = 'relatedHover',
    Default = 'default',
}

export enum LigandStateEnum {
    FirstAdd = 'firstAdd',
}

export enum EdgeStateEnum {
    Virtual = 'virtual',
}

export type LigandStateType = {
    [state in ElementStateEnum | LigandStateEnum]?: boolean;
};

export type EdgeStateType = {
    [state in ElementStateEnum | EdgeStateEnum]?: boolean;
};

export type LigandElementStyle = {
    [type in ElementStateEnum | LigandStateEnum]?: DisplayableProps['style'];
};

export type EdgeElementStyle = {
    [type in ElementStateEnum | EdgeStateEnum]?: DisplayableProps['style'];
};

export interface SubElement {
    el: Element<DisplayableProps>;
    style: LigandElementStyle | EdgeElementStyle;
    state: ElementStateEnum | LigandStateEnum | EdgeStateEnum;
    type: string;
    toScale1(): void;
    toScaleX(): void;
    fadeout(): void;
    fadein(): void;
    updateStyle(state: ElementStateEnum): void;
}

export abstract class SubElement {
    fadeout(): void {
        if (this.el?.isGroup) {
            (this.el as Group).eachChild(child => {
                child.animateTo(
                    {
                        style: {
                            opacity: FADEOUT_OPACITY,
                        },
                    } as any,
                    ANIMATE_CONFIG
                );
            })
            return;
        }
        this.el!.animateTo(
            {
                style: {
                    opacity: FADEOUT_OPACITY,
                },
            },
            ANIMATE_CONFIG
        );
    }
    fadein(): void {
        const style = { ...this.style[ElementStateEnum.Default] };
        if (this.el?.isGroup) {
            (this.el as Group).eachChild(child => {
                child.animateTo(
                    {
                        style: {
                            opacity: style.opacity || NORMAL_OPACITY,
                        },
                    } as any,
                    ANIMATE_CONFIG
                );
            })
            return;
        }
        this.el!.animateTo(
            {
                style: {
                    opacity: style.opacity || NORMAL_OPACITY,
                },
            },
            ANIMATE_CONFIG
        );
    }
    updateStyle(state = ElementStateEnum.Default): void {
        this.state = state;
        const style = { ...this.style[state] };
        if (this.el?.isGroup) {
            (this.el as Group).eachChild(child => {
                child.animateTo(
                    {
                        style: {...style, ...((child.name.startsWith('expDG') && child.name !== 'expDG_content') || (child.name.startsWith('predDG') && child.name !== 'predDG_content') ? {
                            backgroundColor: 'rgba(0,0,0,0)'
                        } : {})},
                      
                    } as any,
                    ANIMATE_CONFIG
                );
            })
            return;
        }
        if (!style.stroke && (this.el as any).style.stroke) {
            style.stroke = (this.el as any).style.stroke
        }
        if (!style.fill && (this.el as any).style.fill) {
            style.fill = (this.el as any).style.fill
        }
        this.el!.animateTo(
            {
                style,
            },
            ANIMATE_CONFIG
        );
    }
}

export interface LigandSubElement extends SubElement {
    style: LigandElementStyle;
    moveTo(params: MoveToParams): void;
}

export abstract class LigandSubElement extends SubElement {
    state: ElementStateEnum | LigandStateEnum = ElementStateEnum.Default;
    toScale1(): void {
        if (this.el.isGroup) {
            (this.el as Group).eachChild(child => {
                child.animateTo(
                    {
                        scaleX: SCALE_1,
                        scaleY: SCALE_1,
                    },
                    ANIMATE_CONFIG
                );
            })
            return;
        }
        this.el!.animateTo(
            {
                scaleX: SCALE_1,
                scaleY: SCALE_1,
            },
            ANIMATE_CONFIG
        );
    }
    toScaleX(): void {
        if (this.el.isGroup) {
            (this.el as Group).eachChild(child => {
                child.animateTo(
                    {
                        scaleX: SCALE_X,
                        scaleY: SCALE_X,
                    },
                    ANIMATE_CONFIG
                );
            })
            return;
        }
        this.el!.animateTo(
            {
                scaleX: SCALE_X,
                scaleY: SCALE_X,
            },
            ANIMATE_CONFIG
        );
    }
}

export interface EdgeSubElement extends SubElement {
    style: EdgeElementStyle;
    draw(params: DrawParams): void;
}

export abstract class EdgeSubElement extends SubElement {
    state: ElementStateEnum | EdgeStateEnum = ElementStateEnum.Default;
    toScale1(): void { }
    toScaleX(): void { }
}
