export interface Game {
    id: number;
    title: string;
    developer: string;
    desc: string;
    release_year: number;
    pos_features: Features;
    neg_features: Features;
}


export interface Features {
    [story: string]:number;
    world:number;
    graphics:number;
}