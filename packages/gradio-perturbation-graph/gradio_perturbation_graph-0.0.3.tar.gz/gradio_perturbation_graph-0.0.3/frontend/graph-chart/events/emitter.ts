export enum EVENT_NAME {
    DBL_CLICK = 'dblclick',
    MOUSEDOWN = 'mousedown',
    MOUSEWHEEL = 'mousewheel',
    CLICK = 'click',
    MOUSEOVER = 'mouseover',
    MOUSEOUT = 'mouseout',
    DELETE_LIGAND = 'deleteLigand',
    ADD_EDGE = 'addEdge',
    SELECT_VIRTUAL_EDGE = 'selectVirtualEdge',
    ADD_VIRTUAL_EDGE = 'addVirtualEdge',
    DELETE_EDGE = 'deleteEdge',
    SELECTOR_CHANGE = 'selectorChange',
    SET_LIGAND_INFOLIST = 'setLigandInfolist',
    SET_EDGE_INFOLIST = 'setEdgeInfolist',
    ROW_MOUSEENTER = 'rowMouseEnter',
    CYCLE_ROW_MOUSEENTER = 'cycleRowMouseEnter',
    ADD_EDGES = 'addEdges',
    DELETE_EDGES = 'deleteEdges',
    GRAPH_DELETE_EDGE = 'graphDeleteEdge',
    GRAPH_ADD_EDGE = 'graphAddEdge',
    TABLE_ADD_LIGANDS = 'tableAddLigands',
    TABLE_DELETE_LIGANDS = 'tableDeleteLigands',
    TOOLBAR_DELETE_LIGAND = 'toolbarDeleteLigand',
    ZOOM_CHANGE = 'zoomChange',
    GRAPH_EDGE_HOVER = 'graphEdgeHover',
    GRAPH_EDGE_HOVEREND = 'graphEdgeHoverEnd',

    ADD_HISTORY = 'addHistory',
    ADD_HISTORIES = 'addHistories',
    CLICK_HISTORY = 'clickHistory',
    CLEAR = 'clear',
    SHOW_HISTORY_PARAMS = 'showHistoryParams',
    DELETE_HISTORIES = 'deleteHistories',
    ON_PAIR_MOUSEOVER = 'onPairMouseover',
    ON_PAIR_MOUSEOUT = 'onPairMouseout',
    SAVE_POSITION = 'savePosition',
    LIGAND_ROW_MOUSEENTER = 'ligandRowMouseEnter',
}

export class EventEmitter {
    events = new Map();

    on(name: string, fn: (...args: Array<any>) => any) {
        this.events.set(name, fn);
    }

    emit(name: string, ...args: Array<any>) {
        const fn = this.events.get(name);
        if (!fn) return;
        return fn(...args);
    }
}

export default new EventEmitter();
