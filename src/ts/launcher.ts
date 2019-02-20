import {SplitPanel} from '@phosphor/widgets';
import {request, RequestResult} from './request'
import {baseUrl} from './utils';

function autocomplete(input: HTMLInputElement | null): Promise<string[]> {
    if(input === undefined || !input){
        return new Promise<string[]>((resolve, reject) => {reject();});
    }

    return new Promise<string[]>((resolve, reject) => {
        request('get', baseUrl() + 'api/v1/search?val=' + input.value).then((res: RequestResult) => {
            if(res.ok){
                resolve((res.json() as {[key: string]: [string]})['values']);
            } else {
                reject();
            }
        });
    });
}


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
        let search = this._getNotebookSearch();
        search.addEventListener('input', () => {
            autocomplete(search.querySelector('input')).then((res: string[]) => {
                let datalist = search.querySelector('datalist');
                if(!datalist){
                    return;
                }
                while(datalist.lastChild){datalist.removeChild(datalist.lastChild)}
                for(let j of res){
                    let option = document.createElement('option');
                    option.value = j;
                    datalist.appendChild(option);
                }
            });
        })
        div.appendChild(search);
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

        let datalist = document.createElement('datalist');
        datalist.id = 'search-datalist';
        input.setAttribute('list', 'search-datalist');

        div.appendChild(input);
        div.appendChild(datalist);
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