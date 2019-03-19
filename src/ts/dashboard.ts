import {BoxPanel, DockPanel} from "@phosphor/widgets";
import {NotebookWidget} from "./notebook";

export
class DashboardWidget extends DockPanel {
    constructor() {
        super();
        this.id = "dock";
        this.title.label = "Dashboard";
        BoxPanel.setStretch(this, 1);
    }

    public add(result: {[key: string]: string}): void {
        const name = result.name;
        const id = result.id;
        const port = result.port;
        const widget = new NotebookWidget(name, id, port);
        this.addWidget(widget);
        this.selectWidget(widget);
    }

}
