import {TabPanel, Widget} from '@phosphor/widgets';

import {Header} from './header';
import {LauncherWidget} from './launcher';
import {DashboardWidget} from './dashboard';
import {showLoader, hideLoader} from './loader';

import '../src/style/index.css';

export
function main(): void {
  /* Title bar */
  let header = new Header();
  Widget.attach(header, document.body);

  showLoader();
  hideLoader(1000);

  let main = new TabPanel();
  main.id = 'main';

  let dock = new DashboardWidget();
  let home = new LauncherWidget(dock);
  // home.setRelativeSizes([.3, .7]);

  main.addWidget(home);
  main.addWidget(dock);
  window.onresize = () => { main.update(); };
  Widget.attach(main, document.body);
}
