import {
  SplitPanel
} from '@phosphor/widgets';

export
class LauncherWidget extends SplitPanel {
    constructor(){
        super();
        this.id = 'home';
        this.title.label = 'Home';
        let div = document.createElement('div');
        div.classList.add('home-controls');

        let context = document.createElement('select');
        let option1 = document.createElement('option');
        let option2 = document.createElement('option');
        let option3 = document.createElement('option');
        option1.text = 'notebook';
        option2.text = 'paste';
        option3.text = 'upload';
        context.add(option1);
        context.add(option2);
        context.add(option3);
        div.appendChild(context);

        context.addEventListener('change', (e: Event) => {
            if(context.value == 'paste') {
                (div.querySelector('.notebook-paste') as HTMLDivElement).style.display = 'flex';
                (div.querySelector('.notebook-upload') as HTMLDivElement).style.display = 'none';
                (div.querySelector('.notebook-search') as HTMLDivElement).style.display = 'none';
            } else if(context.value == 'upload') {
                (div.querySelector('.notebook-paste') as HTMLDivElement).style.display = 'none';
                (div.querySelector('.notebook-upload') as HTMLDivElement).style.display = 'flex';
                (div.querySelector('.notebook-search') as HTMLDivElement).style.display = 'none';
            } else {
                (div.querySelector('.notebook-paste') as HTMLDivElement).style.display = 'none';
                (div.querySelector('.notebook-upload') as HTMLDivElement).style.display = 'none';
                (div.querySelector('.notebook-search') as HTMLDivElement).style.display = 'flex';
            }
        })

        /* Visualizers */
        div.appendChild(this._getNotebookSearch());
        div.appendChild(this._getPaste());
        div.appendChild(this._getUpload());
        (div.querySelector('.notebook-search') as HTMLDivElement).style.display = 'flex';

        let but = document.createElement('button');
        but.type = 'submit';
        but.textContent = '>>';
        div.appendChild(but);

        this.node.append(div);
    }

    private _getNotebookSearch(): HTMLDivElement {
        let div = document.createElement('div');
        div.classList.add('notebook-search');

        let input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'search...';

        div.appendChild(input);
        div.style.display = 'none';
        return div;
    }

    private _getPaste(): HTMLDivElement {
        let div = document.createElement('div');
        div.classList.add('notebook-paste');

        let input = document.createElement('textarea');
        input.placeholder = 'paste notebook json here...';
        input.style.height = '300px';
        input.style.width = '100%';

        div.appendChild(input);
        div.style.display = 'none';
        return div;
    }

    private _getUpload(): HTMLDivElement {
        let div = document.createElement('div');
        div.classList.add('notebook-upload');

        let input = document.createElement('input');
        input.type = 'file';
        input.multiple = false;
        input.style.marginLeft = 'auto';
        input.style.marginRight = 'auto';

        div.appendChild(input);
        div.style.display = 'none';
        return div;
    }
}