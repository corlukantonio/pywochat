//@ts-check

export class ComposeMessageHandler {
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
