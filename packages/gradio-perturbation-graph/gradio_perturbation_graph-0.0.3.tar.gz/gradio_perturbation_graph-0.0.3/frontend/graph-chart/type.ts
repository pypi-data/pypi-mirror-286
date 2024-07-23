export interface FEPLigand {
    id: number;
    img: string;
    fileId?: number;
    expDG?: number;
    predDG?: number;
    predDGErr?: number;
    status?: ProjectFileStatus;
    name: string;
    molPath?: string;
    imgPath?: string;
    createTime?: string;
    jobId?: number;
}

export interface FEPPair {
    id: number;
    uniqueId: string;
    status?: FEPPairStatus;
    simScore: number;
    coreHop?: 0 | 1;
    expDDG?: number;
    predDDG?: number;
    predDDGErr?: number;
    predDDGCycle?: number;
    predDDGCycleErr?: number;
    // ligandIds: number[];
    ligandA: number;
    // ligandAId?: number;
    ligandB: number;
    // ligandBId?: number;
    source: FEPLigand;
    target: FEPLigand;
    jobId?: number;
    confidence?: number;
    show?: boolean;
    createTime?: string;
    updateTime?: string;
    order?: number;
    calculated?: boolean;
    latestMappingJobId?: number;
    latestAnalysisJobId?: number;
    chargeChange?: number;
    proteinId?: number;
}

export interface FEPCycle {
    confidence: FepCalcConfidence;
    cycleErr: number;
    cycleSize: number;
    cycles: number[];
    id: number;
}

export enum FEPPairStatus {
    Failed = -2,
    Deleted,
    Success,
    Running,
    Stopped,
    Paused,
    NotMapping,
}

export enum FepCalcConfidence {
    Fail = 0,
    Good,
    OK,
    Bad,
}

export enum ProjectFileStatus {
    NotReady = 0, // 后端枚举
    Valid = 3,
    Invalid = -3,
    Running = -99, // 前端自己加的枚举
    Failed, // 前端自己加的枚举
}