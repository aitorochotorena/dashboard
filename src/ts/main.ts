import {TabPanel, Widget} from "@phosphor/widgets";

import {DashboardWidget} from "./dashboard";
import {Header} from "./header";
import {LauncherWidget} from "./launcher";
import {hideLoader, showLoader} from "./loader";

import "../src/style/index.css";

export
function main(): void {
  /* Title bar */
  const header = new Header();
  Widget.attach(header, document.body);

  showLoader();
  hideLoader(1000);

  // tslint:disable-next-line: no-shadowed-variable
  const main = new TabPanel();
  main.id = "main";

  const dock = new DashboardWidget();
  const home = new LauncherWidget(dock);
  // home.setRelativeSizes([.3, .7]);

  main.addWidget(home);
  main.addWidget(dock);
  window.onresize = () => { main.update(); };
  Widget.attach(main, document.body);
}
