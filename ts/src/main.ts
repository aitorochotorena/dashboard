import {TabPanel, Widget} from '@phosphor/widgets';

import {Header} from './header';
import {LauncherWidget} from './launcher';
import {DashboardWidget} from './dashboard';
import {showLoader, hideLoader} from './loader';

import '../ts/style/index.css';

export
function main(): void {
  /* Title bar */
  let header = new Header();
  Widget.attach(header, document.body);

  showLoader();
  hideLoader(1000);

  let main = new TabPanel();
  main.id = 'main';

  let home = new LauncherWidget();
  main.addWidget(home);
  // home.setRelativeSizes([.3, .7]);
  // home.addWidget(dock);

  let dock = new DashboardWidget();
  main.addWidget(dock);

  /* Reference Data Tab */
  // let input = new BoxPanel({ direction: 'top-to-bottom', spacing: 0 });

  window.onresize = () => { main.update(); };
  Widget.attach(main, document.body);
}
