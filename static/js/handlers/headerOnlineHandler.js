//@ts-check

const headerOnlineHandlerInstance = Symbol('headerOnlineHandlerInstance');

export class HeaderOnlineHandler {
  /**
   * Gets instance.
   *
   * @returns {HeaderOnlineHandler}
   */
  static getInstance = () => {
    if (HeaderOnlineHandler[headerOnlineHandlerInstance] === undefined) {
      HeaderOnlineHandler[headerOnlineHandlerInstance] =
        new HeaderOnlineHandler();
    }

    return HeaderOnlineHandler[headerOnlineHandlerInstance];
  };

  getLoggedInUserUsername = async () => $('#loggedInUserUsername').text();
}

window.HeaderOnlineHandler = HeaderOnlineHandler;
