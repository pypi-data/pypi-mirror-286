import { Group } from 'zrender';
import { DisplayableProps } from 'zrender/lib/graphic/Displayable';
import { SubElement, ElementStateEnum, LigandStateType, EdgeStateType } from './subElement/subElement';
import { addElementZ } from '../constant';

export default interface Element {
    el: Group;
    type: string;
    state: LigandStateType | EdgeStateType;
    data: any;
    onHover(): void;
    onHover(): void;
    onRelatedHover(): void;
    onRelatedHoverEnd(): void;
    onSelected(idx?: number): void;
    onSelectedEnd(): void;
    toScale1(): void;
    toScaleX(): void;
    fadeout(): void;
    fadein(): void;
    updateStyle(): void;
}

export default abstract class Element {
    el = new Group();
    subElements = new Set<SubElement>();
    z = 0;
    onHover() {
        if (this.state.hover) return;
        this.z = addElementZ();
        this.el.children().forEach(item => {
            if (item.isGroup) {
                (item as Group).eachChild(child => {
                    child.attr({
                        z: this.z,
                    } as DisplayableProps);
                })
            } else {
                item.attr({
                    z: this.z,
                } as DisplayableProps);
            }
        });
        this.toScaleX();
        this.state.hover = true;
        this.updateStyle();
    }
    onHoverEnd() {
        if (!this.state.hover) return;
        this.toScale1();
        this.state.hover = false;
        this.updateStyle();
    }
    onRelatedHover() {
        if (this.state.relatedHover) return;
        this.z = addElementZ();
        this.el.children().forEach(item => {
            if (item.isGroup) {
                (item as Group).eachChild(child => {
                    child.attr({
                        z: this.z,
                    } as DisplayableProps);
                })
            } else {
                item.attr({
                    z: this.z,
                } as DisplayableProps);
            }
        });
        this.state.relatedHover = true;
        this.updateStyle();
    }
    onRelatedHoverEnd() {
        if (!this.state.relatedHover) return;
        this.state.relatedHover = false;
        this.updateStyle();
    }
    onSelected() {
        if (this.state.selected) return;
        this.el.children().forEach(item => {
            if (item.isGroup) {
                (item as Group).eachChild(child => {
                    child.attr({
                        zlevel: 101,
                    } as DisplayableProps);
                })
            } else {
                item.attr({
                    zlevel: 100,
                } as DisplayableProps);
            }
        });
        this.state.selected = true;
        this.updateStyle();
    }
    onSelectedEnd() {
        if (!this.state.selected) return;
        this.el.children().forEach(item => {
            if (item.isGroup) {
                (item as Group).eachChild(child => {
                    child.attr({
                        zlevel: 5,
                    } as DisplayableProps);
                })
            } else {
                item.attr({
                    zlevel: 0,
                } as DisplayableProps);
            }
        });
        this.state.selected = false;
        this.updateStyle();
    }

    updateStyle() {
        let state: ElementStateEnum = ElementStateEnum.Default;
        Object.keys(this.state).some(key => {
            if (this.state[key as ElementStateEnum]) {
                state = key as ElementStateEnum;
                return true;
            }
            return false;
        });
        this.subElements.forEach(element => element.updateStyle(state));
    }

    toScale1() {
        this.subElements.forEach(element => element.toScale1());
    }

    toScaleX() {
        this.subElements.forEach(element => element.toScaleX());
    }

    fadeout() {
        this.subElements.forEach(element => element.fadeout());
    }

    fadein() {
        this.subElements.forEach(element => element.fadein());
    }
}
