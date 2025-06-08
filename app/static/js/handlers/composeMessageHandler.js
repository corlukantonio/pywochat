//@ts-check

const composeMessageHandlerInstance = Symbol('composeMessageHandlerInstance');

export class ComposeMessageHandler {
  /**
   * Gets instance.
   *
   * @returns {ComposeMessageHandler}
   */
  static getInstance = () => {
    if (ComposeMessageHandler[composeMessageHandlerInstance] === undefined) {
      ComposeMessageHandler[composeMessageHandlerInstance] =
        new ComposeMessageHandler();
    }

    return ComposeMessageHandler[composeMessageHandlerInstance];
  };

  /**
   * Gets input message.
   *
   * @returns {string | undefined}
   */
  getInputMessage = () => $('#inputMsg').val()?.toString();

  /**
   * Empties input message value.
   *
   * @returns {JQuery<HTMLElement>}
   */
  emptyInputMessage = () => $('#inputMsg').val('');
}
