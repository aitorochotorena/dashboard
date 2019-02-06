import "isomorphic-fetch";

// first
Object.defineProperty(window, 'MutationObserver', { value: class {
    constructor(callback: any) {}
    disconnect() {}
    observe(element: any, initObject: any) {}
}});

import {main} from '../../ts/src/main';

describe('Checks exports', () => {
    test("Check import", () => {
        console.log(main);
    });
});

