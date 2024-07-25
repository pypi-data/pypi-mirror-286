import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import {ForumDashboardWidget} from './forumdashboard';
import { PageConfig } from '@jupyterlab/coreutils';


const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_forum:plugin',
  description: 'A JupyterLab extension for databrix forum frontend',
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate
};

function activate(app: JupyterFrontEnd, palette: ICommandPalette) {
  console.log('JupyterLab extension forum is activated!');


  //get current User
  const user = app.serviceManager.user;
  const baseUrl = PageConfig.getBaseUrl()  // e.g., /jupyterhub/user/xxx/
  // Use URL object to extract the path
  const urlObj = new URL(baseUrl);
  const path = urlObj.pathname;


  const fullUrl = window.location.origin;   // e.g., https://example.org

  let jupyterhubBaseUrl: string;

  // Check if the baseUrl contains '/user/'
  if (path.includes('/user/')) {
    // Extract everything before '/user/'
    jupyterhubBaseUrl = `${fullUrl}${path.split('/user/')[0]}`;
  } else {
    // If '/user/' is not present, use the baseUrl directly
    jupyterhubBaseUrl = `${fullUrl}`;
  }
  const forumEndpointUrl = `${jupyterhubBaseUrl}/services/forum/`;
  console.log('JupyterHub Base URL:', forumEndpointUrl);

  // Define a widget creator function
  const newWidget = () => {
    const content = new ForumDashboardWidget(user.identity ? user.identity.name : 'Unknown User', forumEndpointUrl);
    const widget = new MainAreaWidget({content});
    widget.id = 'forum-jupyterlab';
    widget.title.label = 'Forum';
    widget.title.closable = true;
    return widget;
  }

  // Create a single widget
  let widget = newWidget();

  // Add an application command
  const command: string = 'forum:open';
  app.commands.addCommand(command, {
    label: 'Databrix Forum',
    execute: () => {
      // Regenerate the widget if disposed
      if (widget.isDisposed) {
        widget = newWidget();
      }
      if (!widget.isAttached) {
        // Attach the widget to the main work area if it's not there
        app.shell.add(widget, 'main');
      }

      // Activate the widget
      app.shell.activateById(widget.id);
    }
  });

  // Add the command to the palette.
  palette.addItem({ command, category: 'Forum' });
}

export default plugin;
