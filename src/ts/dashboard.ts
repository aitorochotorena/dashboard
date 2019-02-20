import {DockPanel, BoxPanel} from '@phosphor/widgets';
import {NotebookWidget} from './notebook';

export
class DashboardWidget extends DockPanel {
    constructor() {
        super();
        this.id = 'dock';
        this.title.label = 'Dashboard';
        BoxPanel.setStretch(this, 1);
    }

    add(result: {[key: string]: string}): void {
        let name = result['name'];
        let id = result['id'];
        let port = result['port'];
        let widget = new NotebookWidget(name, id, port);
        this.addWidget(widget);
        this.selectWidget(widget);
    }

}