import {SplitPanel, TabPanel} from "@phosphor/widgets";
import {DashboardWidget} from "./dashboard";
import {showLoader} from "./loader";
import {IRequestResult, request} from "./request";
import {baseUrl} from "./utils";

function autocomplete(input: string): Promise<Array<{[key: string]: string}>> {
    return new Promise<Array<{[key: string]: string}>>((resolve, reject) => {
        request("get", baseUrl() + "api/v1/search?val=" + input).then((res: IRequestResult) => {
            if (res.ok) {
                resolve((res.json() as {[key: string]: Array<{[key: string]: string}>}).values);
            } else {
                reject();
            }
        });
    });
}

function launch(input: string): Promise<{[key: string]: string}> {
    showLoader();
    return new Promise<{[key: string]: string}>((resolve, reject) => {
        request("get", baseUrl() + "api/v1/launch?val=" + input).then((res: IRequestResult) => {
            if (res.ok) {
                resolve((res.json() as {[key: string]: string}));
            } else {
                reject();
            }
        });
    });
}

export
class LauncherWidget extends SplitPanel {
    // tslint:disable: variable-name
    private _dashboard: DashboardWidget;

    constructor(dashboard: DashboardWidget) {
        super();
        this.id = "home";
        this.title.label = "Home";
        this._dashboard = dashboard;

        /* Construct controls module */
        const div = document.createElement("div");
        div.classList.add("home-controls");

        /* Construct selector */
        const context = document.createElement("select");
        const option1 = document.createElement("option");
        const option2 = document.createElement("option");
        const option3 = document.createElement("option");
        option1.text = "notebook";
        option2.text = "paste";
        option3.text = "upload";
        context.add(option1);
        context.add(option2);
        context.add(option3);
        div.appendChild(context);

        /* Display appropriate input area for selected option */
        context.addEventListener("change", (e: Event) => {
            if (context.value === "paste") {
                (div.querySelector(".notebook-paste") as HTMLDivElement).style.display = "flex";
                (div.querySelector(".notebook-upload") as HTMLDivElement).style.display = "none";
                (div.querySelector(".notebook-search") as HTMLDivElement).style.display = "none";
            } else if (context.value === "upload") {
                (div.querySelector(".notebook-paste") as HTMLDivElement).style.display = "none";
                (div.querySelector(".notebook-upload") as HTMLDivElement).style.display = "flex";
                (div.querySelector(".notebook-search") as HTMLDivElement).style.display = "none";
            } else {
                (div.querySelector(".notebook-paste") as HTMLDivElement).style.display = "none";
                (div.querySelector(".notebook-upload") as HTMLDivElement).style.display = "none";
                (div.querySelector(".notebook-search") as HTMLDivElement).style.display = "flex";
            }
        });

        /* Visualizers */

        /* Search */
        const search = this._getNotebookSearch();
        search.addEventListener("input", () => {
            const input = search.querySelector("input");
            if (!input || !input.value) {
                return;
            }
            autocomplete(input.value).then((res: Array<{[key: string]: string}>) => {
                const datalist = search.querySelector("datalist");
                if (!datalist) {
                    return;
                }
                while (datalist.lastChild) {datalist.removeChild(datalist.lastChild); }
                for (const val of res) {
                    const option = document.createElement("option");
                    option.value = val.id + " - " + val.name;
                    option.innerText = val.created;
                    datalist.appendChild(option);
                }
            });
        });
        div.appendChild(search);

        /* Paste */
        const paste = this._getPaste();
        div.appendChild(paste);

        /* Upload */
        const upload = this._getUpload();
        div.appendChild(upload);
        (div.querySelector(".notebook-search") as HTMLDivElement).style.display = "flex";

        /* Submit/Launch */
        const but = document.createElement("button");
        but.type = "submit";
        but.textContent = ">>";
        but.addEventListener("click", () => {
            this._save(context, search, paste, upload).then((res: {[key: string]: string}) => {
                this._launch(context, search, paste, upload).then((res2: {[key: string]: string}) => {
                    this._dashboard.add(res2);
                    if (this.parent) {
                        const parent = this.parent.parent as TabPanel; // 2 levels up
                        parent.currentWidget = this._dashboard;  // set to dashboard
                    }
                });
            });
        });
        div.appendChild(but);
        this.node.append(div);
    }

    private _save(context: HTMLSelectElement,
                  search: HTMLDivElement,
                  paste: HTMLDivElement,
                  upload: HTMLDivElement): Promise<{[key: string]: string}> {
        if (context.value === "notebook") {
            return new Promise((resolve) => {resolve({}); });
        } else {
            // tslint:disable-next-line: no-console
            console.warn("Not Implemented");
            return new Promise((resolve) => {resolve({}); });
        }
    }

    private _launch(context: HTMLSelectElement,
                    search: HTMLDivElement,
                    paste: HTMLDivElement,
                    upload: HTMLDivElement): Promise<{[key: string]: string}> {
        if (context.value === "notebook") {
            return new Promise((resolve, reject) => {
                const input = search.querySelector("input");
                if (!input || !input.value) {
                    reject({});
                    return;
                }
                launch(input.value).then((res: {[key: string]: string}) => {
                    resolve(res);
                });
            });
        } else {
            // tslint:disable-next-line: no-console
            console.warn("Not Implemented");
            return new Promise((resolve) => {resolve({}); });
        }
    }

    private _getNotebookSearch(): HTMLDivElement {
        const div = document.createElement("div");
        div.classList.add("notebook-search");

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = "search...";

        const datalist = document.createElement("datalist");
        datalist.id = "search-datalist";
        input.setAttribute("list", "search-datalist");

        div.appendChild(input);
        div.appendChild(datalist);
        div.style.display = "none";
        return div;
    }

    private _getPaste(): HTMLDivElement {
        const div = document.createElement("div");
        div.classList.add("notebook-paste");

        const input = document.createElement("textarea");
        input.placeholder = "paste notebook json here...";
        input.style.height = "300px";
        input.style.width = "100%";

        div.appendChild(input);
        div.style.display = "none";
        return div;
    }

    private _getUpload(): HTMLDivElement {
        const div = document.createElement("div");
        div.classList.add("notebook-upload");

        const input = document.createElement("input");
        input.type = "file";
        input.multiple = false;
        input.style.marginLeft = "auto";
        input.style.marginRight = "auto";

        div.appendChild(input);
        div.style.display = "none";
        return div;
    }
}
