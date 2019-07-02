import {Widget} from "@phosphor/widgets";
import {hideLoader} from "./loader";
import {baseUrl} from "./utils";

export
class NotebookWidget extends Widget {
    constructor(name: string, id: string, port: string) {
        super();
        this.id = id;
        this.title.label = name;
        this.title.closable = true;

        this.node.classList.add("notebook-widget");
        const iframe = document.createElement("iframe");
        iframe.setAttribute("referrerpolicy", "no-referrer");

        iframe.src = baseUrl() + "voila/" + id + "/";
        iframe.addEventListener("load", () => {
            hideLoader(500);
        });
        this.node.appendChild(iframe);
    }
}
