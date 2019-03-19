import {Widget} from "@phosphor/widgets";
import {hideLoader, showLoader} from "./loader";

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

        showLoader();
        setTimeout(() => {
            iframe.src = "http://localhost:" + port;
            hideLoader(500);
        }, 2000);
        this.node.appendChild(iframe);
    }
}
