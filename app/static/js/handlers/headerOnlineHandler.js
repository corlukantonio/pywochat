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

  /**
   * Gets logged in user username.
   *
   * @returns {Promise<string>}
   */
  getLoggedInUserUsername = async () => {
    return $('#loggedInUserUsername').text();
  };
}

globalThis.HeaderOnlineHandler = HeaderOnlineHandler;
