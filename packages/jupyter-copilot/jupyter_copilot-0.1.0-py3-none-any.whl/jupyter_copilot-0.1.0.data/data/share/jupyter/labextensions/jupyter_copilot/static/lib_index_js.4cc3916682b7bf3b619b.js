"use strict";
(self["webpackChunkjupyter_copilot"] = self["webpackChunkjupyter_copilot"] || []).push([["lib_index_js"],{

/***/ "./lib/commands/authentication.js":
/*!****************************************!*\
  !*** ./lib/commands/authentication.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LoginExecute: () => (/* binding */ LoginExecute),
/* harmony export */   SignOutExecute: () => (/* binding */ SignOutExecute)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils */ "./lib/utils.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);



const defaultWidgetCSS = `
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
      color: #333;
      background-color: #fff;
      padding: 30px;
      max-width: 400px;
      margin: 0 auto;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
`;
const signWidget = (authData) => {
    const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    const messageElement = document.createElement('div');
    messageElement.style.cssText = defaultWidgetCSS;
    messageElement.innerHTML = `
            <h2 style="font-size: 24px; margin-bottom: 20px; color: #0366d6;">GitHub Copilot Authentication</h2>
            <p style="margin-bottom: 10px;">Enter this code on GitHub:</p>
            <div style="font-size: 32px; font-weight: bold; background-color: #f6f8fa; color: #0366d6; padding: 15px; border-radius: 5px; margin: 20px 0; letter-spacing: 2px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">${authData.userCode}</div>
            <p style="margin-bottom: 10px;">Go to: <a href="${authData.verificationUri}" target="_blank" style="color: #0366d6; text-decoration: none;">${authData.verificationUri}</a></p>
            <p style="font-size: 14px; color: #666;">This code will expire in <span id="timer" style="font-weight: bold;">${authData.expiresIn}</span> seconds.</p>
          `;
    content.node.appendChild(messageElement);
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
    widget.id = 'apod-jupyterlab';
    widget.title.label = 'Sign In';
    widget.title.closable = true;
    return widget;
};
const alreadySignedInWidget = (username) => {
    const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    const messageElement = document.createElement('div');
    messageElement.style.cssText = defaultWidgetCSS;
    messageElement.innerHTML = `
            <h2 style="font-size: 24px; margin-bottom: 20px;">Copilot already signed in as: <span style="color: #2366d6;">${username}</span></h2>
          `;
    content.node.appendChild(messageElement);
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
    widget.id = 'apod-jupyterlab';
    widget.title.label = 'Already Signed In';
    widget.title.closable = true;
    return widget;
};
const SignedOutWidget = () => {
    const content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
    const messageElement = document.createElement('div');
    messageElement.style.cssText = defaultWidgetCSS;
    messageElement.innerHTML = `
            <h2 style="font-size: 24px; margin-bottom: 20px; color: #2366d6;">Successfully signed out with GitHub!</h2>
          `;
    content.node.appendChild(messageElement);
    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
    widget.id = 'apod-jupyterlab';
    widget.title.label = 'Sign Out Successful';
    widget.title.closable = true;
    return widget;
};
// function to execute whenever the login command is called
const LoginExecute = (app) => {
    (0,_utils__WEBPACK_IMPORTED_MODULE_2__.makePostRequest)('login', {}).then(data => {
        // data is a string turned into a json object
        const res = JSON.parse(data);
        // handle this branch later
        if (res.status === 'AlreadySignedIn') {
            let widget = alreadySignedInWidget(res.user);
            if (!widget.isDisposed) {
                widget.dispose();
                widget = alreadySignedInWidget(res.user);
            }
            if (!widget.isAttached) {
                app.shell.add(widget, 'main');
            }
            return;
        }
        let widget = signWidget(res);
        if (!widget.isDisposed) {
            widget.dispose();
            widget = signWidget(res);
        }
        if (!widget.isAttached) {
            app.shell.add(widget, 'main');
        }
        // countdown timer for expires in the this code will expire in {expiresin seconds}
        let timeRemaining = res.expiresIn;
        const interval = setInterval(() => {
            if (timeRemaining <= 0) {
                clearInterval(interval);
                widget.dispose();
                return;
            }
            const timerElement = widget.node.querySelector('#timer');
            if (timerElement) {
                timerElement.textContent = timeRemaining.toString();
            }
            timeRemaining--;
        }, 1000);
        app.shell.activateById(widget.id);
    });
};
// function to execute when the signout command is called
const SignOutExecute = (app) => {
    (0,_utils__WEBPACK_IMPORTED_MODULE_2__.makePostRequest)('signout', {}).then(data => {
        const res = JSON.parse(data);
        if (res.status === 'NotSignedIn') {
            let widget = SignedOutWidget();
            if (!widget.isDisposed) {
                widget.dispose();
                widget = SignedOutWidget();
            }
            if (!widget.isAttached) {
                app.shell.add(widget, 'main');
            }
        }
    });
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lsp__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./lsp */ "./lib/lsp.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _commands_authentication__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./commands/authentication */ "./lib/commands/authentication.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);








let ENABLED_FLAG = true;
let COMPLETION_BIND = 'Ctrl J';
class CopilotInlineProvider {
    constructor(notebookClients) {
        this.name = 'GitHub Copilot';
        this.identifier = 'jupyter_copilot:provider';
        this.rank = 1000;
        this.lastRequestTime = 0;
        this.timeout = null;
        this.lastResolved = () => { };
        this.requestInProgress = false;
        this.notebookClients = notebookClients;
    }
    async fetch(request, context) {
        if (!ENABLED_FLAG) {
            return { items: [] };
        }
        const now = Date.now();
        // debounce mechanism
        // if a request is made within 90ms of the last request, throttle the request
        // but if it is the last request, then make the request
        if (this.requestInProgress || now - this.lastRequestTime < 150) {
            this.lastRequestTime = now;
            // this request was made less than 90ms after the last request
            // so we resolve the last request with an empty list then clear the timeout
            this.lastResolved({ items: [] });
            clearTimeout(this.timeout);
            return new Promise(resolve => {
                this.lastResolved = resolve;
                // set a timeout that will resolve the request after 200ms
                // if no calls are made within 90ms then this will resolve and fetch
                // if a call comes in < 90ms then this will be cleared and the request will be solved to empty list
                this.timeout = setTimeout(async () => {
                    this.requestInProgress = true;
                    this.lastRequestTime = Date.now();
                    const items = await this.fetchCompletion(request, context);
                    resolve(items);
                }, 200);
            });
        }
        else {
            // if request is not throttled, just get normally
            this.requestInProgress = true;
            this.lastRequestTime = now;
            return await this.fetchCompletion(request, context);
        }
    }
    // logic to actually fetch the completion
    async fetchCompletion(_request, context) {
        const editor = context.editor;
        const cell = context.widget._content._activeCellIndex;
        const client = this.notebookClients.get(context.widget.id);
        const cursor = editor === null || editor === void 0 ? void 0 : editor.getCursorPosition();
        const { line, column } = cursor;
        client === null || client === void 0 ? void 0 : client.sendUpdateLSPVersion();
        const items = [];
        const completions = await (client === null || client === void 0 ? void 0 : client.getCopilotCompletion(cell, line, column));
        completions === null || completions === void 0 ? void 0 : completions.forEach(completion => {
            items.push({
                // sometimes completions have ``` in them, so we remove it
                insertText: completion.displayText.replace('```', ''),
                isIncomplete: false
            });
        });
        this.requestInProgress = false;
        return { items };
    }
}
/**
 * Initialization data for the jupyter_copilot extension.
 */
const plugin = {
    id: 'jupyter_copilot:plugin',
    description: 'GitHub Copilot for Jupyter',
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker,
        _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_4__.ICompletionProviderManager,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.ICommandPalette,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry
    ],
    activate: (app, notebookTracker, providerManager, palette, settingRegistry) => {
        console.log('Jupyter Copilot Extension Activated');
        Promise.all([app.restored, settingRegistry.load(plugin.id)]).then(([, settings]) => {
            const loadSettings = () => {
                ENABLED_FLAG = settings.get('flag').composite;
                console.log('Settings loaded:', ENABLED_FLAG, COMPLETION_BIND);
            };
            COMPLETION_BIND = settings.get('keybind').composite;
            loadSettings();
            settings.changed.connect(loadSettings);
            const command = 'jupyter_copilot:completion';
            app.commands.addCommand(command, {
                label: 'Copilot Completion',
                execute: () => {
                    var _a, _b;
                    // get id of current notebook panel
                    const notebookPanelId = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.id;
                    (_b = providerManager.inline) === null || _b === void 0 ? void 0 : _b.accept(notebookPanelId || '');
                }
            });
            app.commands.addKeyBinding({
                command,
                keys: [COMPLETION_BIND],
                selector: '.jp-GhostText'
            });
            const SignInCommand = 'Copilot: Sign In';
            app.commands.addCommand(SignInCommand, {
                label: 'Copilot: Sign In With GitHub',
                iconClass: 'cpgithub-icon',
                execute: () => (0,_commands_authentication__WEBPACK_IMPORTED_MODULE_6__.LoginExecute)(app)
            });
            const SignOutCommand = 'Copilot: Sign Out';
            app.commands.addCommand(SignOutCommand, {
                label: 'Copilot: Sign Out With GitHub',
                iconClass: 'cpgithub-icon',
                execute: () => (0,_commands_authentication__WEBPACK_IMPORTED_MODULE_6__.SignOutExecute)(app)
            });
            // make them pop up at the top of the palette first items on the palleete commands and update rank
            palette.addItem({
                command: SignInCommand,
                category: 'GitHub Copilot',
                rank: 0
            });
            palette.addItem({
                command: SignOutCommand,
                category: 'GitHub Copilot',
                rank: 1
            });
        });
        const notebookClients = new Map();
        const provider = new CopilotInlineProvider(notebookClients);
        providerManager.registerInlineProvider(provider);
        const serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        // notebook tracker is used to keep track of the notebooks that are open
        // when a new notebook is opened, we create a new LSP client and socket connection for that notebook
        notebookTracker.widgetAdded.connect(async (_, notebook) => {
            var _a;
            await notebook.context.ready;
            const wsURL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(serverSettings.wsUrl, 'jupyter-copilot', 'ws');
            const client = new _lsp__WEBPACK_IMPORTED_MODULE_7__.NotebookLSPClient(notebook.context.path, wsURL);
            notebookClients.set(notebook.id, client);
            notebook.sessionContext.ready.then(() => {
                var _a, _b;
                (_b = (_a = notebook.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.info.then(info => {
                    client.setNotebookLanguage(info.language_info.name);
                });
                notebook.sessionContext.kernelChanged.connect(async (_, kernel) => {
                    var _a;
                    const info = await ((_a = kernel.newValue) === null || _a === void 0 ? void 0 : _a.info);
                    client.setNotebookLanguage(info === null || info === void 0 ? void 0 : info.language_info.name);
                });
            });
            // run whenever a notebook cell updates
            // types are of ISharedCodeCell and CellChange
            // i cannot import them and i cannot find where they are supposed to be
            const onCellUpdate = (update, change) => {
                // only change if it is a source change
                if (change.sourceChange) {
                    const content = update.source;
                    client.sendCellUpdate(notebook.content.activeCellIndex, content);
                }
            };
            // keep the current cell so when can clean up whenever this changes
            let current_cell = notebook.content.activeCell;
            current_cell === null || current_cell === void 0 ? void 0 : current_cell.model.sharedModel.changed.connect(onCellUpdate);
            // run cleanup when notebook is closed
            notebook.disposed.connect(() => {
                client.dispose();
                notebookClients.delete(notebook.id);
            });
            // notifies the extension server when a cell is added or removed
            // swapping consists of an add and a remove, so this should be sufficient
            (_a = notebook.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect((_, change) => {
                if (change.type === 'remove') {
                    client.sendCellDelete(change.oldIndex);
                }
                else if (change.type === 'add') {
                    const content = change.newValues[0].sharedModel.getSource();
                    client.sendCellAdd(change.newIndex, content);
                }
            });
            notebook.context.pathChanged.connect((_, newPath) => {
                client.sendPathChange(newPath);
            });
            // whenever active cell changes remove handler then add to new one
            notebook.content.activeCellChanged.connect((_, cell) => {
                current_cell === null || current_cell === void 0 ? void 0 : current_cell.model.sharedModel.changed.disconnect(onCellUpdate);
                current_cell = cell;
                current_cell === null || current_cell === void 0 ? void 0 : current_cell.model.sharedModel.changed.connect(onCellUpdate);
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/lsp.js":
/*!********************!*\
  !*** ./lib/lsp.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookLSPClient: () => (/* binding */ NotebookLSPClient)
/* harmony export */ });
/*
    This class is responsible for communicating with the LSP server and
    the notebook frontend. It establishes a WebSocket connection with the
    LSP server and listens for messages. It also sends messages to the LSP
    server when a cell is updated in the notebook frontend.
*/
class NotebookLSPClient {
    constructor(notebookPath, wsUrl) {
        this.pendingCompletions = new Map();
        wsUrl = `${wsUrl}?path=${encodeURI(notebookPath)}`;
        this.socket = new WebSocket(wsUrl);
        this.socket.onmessage = this.handleMessage.bind(this);
        this.socket.onopen = () => this.sendMessage('sync_request', {});
    }
    // Handle messages from the extension server
    handleMessage(event) {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case 'sync_response':
                break;
            case 'completion':
                const pendingCompletion = this.pendingCompletions.get(data.req_id);
                if (pendingCompletion) {
                    pendingCompletion.resolve(data.completions);
                    this.pendingCompletions.delete(data.req_id);
                }
                break;
            case 'connection_established':
                console.log('Copilot connected to extension server...');
                break;
            default:
                console.log('Unknown message type:', data);
        }
    }
    // Send a message to the LSP server to update the cell content
    // we don't want to update the entire file every time something is changed
    // so we specify a cell id and the now content so we can modify just that single cell
    sendCellUpdate(cellId, content) {
        this.sendMessage('cell_update', { cell_id: cellId, content: content });
    }
    sendCellDelete(cellID) {
        this.sendMessage('cell_delete', { cell_id: cellID });
    }
    sendCellAdd(cellID, content) {
        this.sendMessage('cell_add', { cell_id: cellID, content: content });
    }
    // sends a message to the server which will then send the updated code to the lsp server
    sendUpdateLSPVersion() {
        this.sendMessage('update_lsp_version', {});
    }
    async getCopilotCompletion(cell, line, character) {
        return new Promise((resolve, reject) => {
            const requestId = `${cell}-${line}-${character}-${Date.now()}`;
            this.pendingCompletions.set(requestId, { resolve, reject });
            this.sendMessage('get_completion', {
                req_id: requestId,
                cell_id: cell,
                line: line,
                character: character
            });
            // add a timeout to reject the promise if no response is received
            setTimeout(() => {
                if (this.pendingCompletions.has(requestId)) {
                    this.pendingCompletions.delete(requestId);
                    reject(new Error('Completion request timed out'));
                }
            }, 10000); // 10 seconds timeout
        });
    }
    sendMessage(type, payload) {
        this.socket.send(JSON.stringify({ type, ...payload }));
    }
    sendPathChange(newPath) {
        this.sendMessage('change_path', { new_path: newPath });
    }
    setNotebookLanguage(language) {
        this.sendMessage('set_language', { language: language });
    }
    // cleans up the socket connection
    dispose() {
        this.socket.close();
        console.log('socket connection closed');
    }
}



/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   makePostRequest: () => (/* binding */ makePostRequest)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


// takes in the route and body of the request (json object)
const makePostRequest = async (route, body) => {
    try {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter-copilot', route);
        const init = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                Authorization: `token ${settings.token}`
            }
        };
        const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
        if (!response.ok) {
            console.error('Response not OK:', response.status, response.statusText);
            const errorData = await response.text();
            console.error('Error data:', errorData);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.text();
        return data;
    }
    catch (reason) {
        console.error(`The jupyter_copilot server extension appears to be missing or the request failed.\n${reason}`);
        throw reason;
    }
};


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4cc3916682b7bf3b619b.js.map