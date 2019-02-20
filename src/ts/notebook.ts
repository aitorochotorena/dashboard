import {Widget} from '@phosphor/widgets';
import {showLoader, hideLoader} from './loader';

export
class NotebookWidget extends Widget {
    constructor(name: string, id: string, port: string) {
        super();
        this.id = id;
        this.title.label = name;
        this.title.closable = true;

        this.node.classList.add('notebook-widget');
        let iframe = document.createElement('iframe');
        iframe.setAttribute('referrerpolicy', 'no-referrer')

        showLoader();
        setTimeout(() => {
            hideLoader();
            iframe.src = 'http://localhost:' + port
        }, 2000);
        this.node.appendChild(iframe);
    }
}