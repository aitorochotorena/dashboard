import {BoxPanel, Widget} from "@phosphor/widgets";

export
class VoilaWidget extends Widget {
    constructor() {
        super();
        this.id = "voila";
        this.title.label = "Voila";
        BoxPanel.setStretch(this, 1);
    }
}
