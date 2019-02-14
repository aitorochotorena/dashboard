import {
  DockPanel, BoxPanel
} from '@phosphor/widgets';

export
class DashboardWidget extends DockPanel {
    constructor() {
        super();
        this.id = 'dock';
        this.title.label = 'Dashboard';
        BoxPanel.setStretch(this, 1);
    }

}