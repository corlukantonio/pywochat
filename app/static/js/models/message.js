//@ts-check

export class Message {
  /**
   * Constructor.
   *
   * @param {string} content
   * @param {string} senderUsername
   * @param {object} receiverUser
   */
  constructor(content, senderUsername, receiverUser) {
    this.content = content;
    this.senderUsername = senderUsername;
    this.receiverUser = receiverUser;
  }

  /**
   * Creates new `Message` object.
   *
   * @param {string} content
   * @param {string} senderUsername
   * @param {object} receiverUser
   * @returns {Message}
   */
  static create = (content, senderUsername, receiverUser) => {
    if (
      typeof content !== 'string' ||
      typeof senderUsername !== 'string' ||
      !receiverUser
    ) {
      throw new Error('Invalid arguments for creating a message.');
    }

    return new Message(content, senderUsername, receiverUser);
  };
}

// @ts-ignore
window.Message = Message;
