//@ts-check

import { Utils } from '../utils.js';
import { HeaderOnlineHandler } from './headerOnlineHandler.js';

export class ContactsHandler {
  /**
   * Constructor.
   *
   * @param {object} messagesHandler
   * @param {object} socket
   */
  constructor(messagesHandler, socket) {
    this.messagesHandler = messagesHandler;
    this.socket = socket;
    this.loggedInUserUsername = null;

    this.assignLoggedInUserUsername();
  }

  /**
   * Assigns logged in user username.
   */
  async assignLoggedInUserUsername() {
    try {
      this.loggedInUserUsername =
        await HeaderOnlineHandler.getInstance().getLoggedInUserUsername();
    } catch (error) {}
  }

  /**
   * Loads messages.
   */
  loadMessages = async () => {
    let targetUser = Utils.getTargetUsername();

    this.messagesHandler.setTargetUser(targetUser);

    targetUser = targetUser.replace('(', '').replace(')', '').split(' ');

    let sentMessages = await this.messagesHandler.getSentMessages();
    let firstMessage = true;

    sentMessages.forEach(async (elem, i) => {
      let messageInfo = (await this.messagesHandler.getMessageInfo(i))
        .text()
        .split(' ');

      if (
        (messageInfo[0] == this.loggedInUserUsername &&
          messageInfo[1] == targetUser[2]) ||
        (messageInfo[0] == targetUser[2] &&
          messageInfo[1] == this.loggedInUserUsername)
      ) {
        this.showMessage(sentMessages[i]);

        if (firstMessage) {
          $(sentMessages[i]).addClass('first_message');
          firstMessage = false;
        }
      } else this.hideMessage(sentMessages[i]);
    });

    this.messagesHandler.scrollToLatest();

    let payload = {
      loggedInUserUsername: this.loggedInUserUsername,
      targetUser: targetUser,
    };

    this.socket.emit('choose_contact', payload);
  };

  /**
   * Shows message.
   *
   * @param {string} sentMessage
   */
  showMessage = async (sentMessage) => $(sentMessage).css('display', 'block');

  /**
   * Hides message.
   *
   * @param {string} sentMessage
   * @returns
   */
  hideMessage = async (sentMessage) => $(sentMessage).css('display', 'none');

  /**
   * Loads latest message.
   */
  loadLatestMessage = async () => {
    let sentMessages = await this.messagesHandler.getSentMessages();
    let messagesContent = await this.messagesHandler.getMessagesContent();
    let inboxUsers = await this.getInboxUsers();
    let inboxLastMessages = await this.getInboxLastMessages();

    sentMessages.forEach(async (elem, i) => {
      let messageInfo = (await this.messagesHandler.getMessageInfo(i))
        .text()
        .split(' ');

      inboxUsers.forEach(async (elem, j) => {
        let isInboxUserSenderOrReceiver =
          $(elem).text().indexOf(messageInfo[0]) > -1 ||
          $(elem).text().indexOf(messageInfo[1]) > -1;

        if (isInboxUserSenderOrReceiver)
          $(inboxLastMessages[j]).text($(messagesContent[i]).text());
      });
    });
  };

  /**
   * Updates last message.
   *
   * @param {object} messageUpdate
   */
  updateLastMessage = async (messageUpdate) => {
    let inboxUsers = await this.getInboxUsers();
    let userMatch = messageUpdate.sender.username === this.loggedInUserUsername;
    let newMsgSound = new Audio(
      Flask.url_for('static', { filename: 'stairs.mp3' })
    );

    inboxUsers.forEach((elem) => {
      let inboxUserInfo = $($(elem).children()[0]);
      let inboxLastMessage = $($(elem).children()[1]);
      let senderUsername = messageUpdate.sender.username;
      let receiverUsername = messageUpdate.receiver.username;

      if (userMatch && inboxUserInfo.text().indexOf(receiverUsername) > -1)
        inboxLastMessage.text(messageUpdate.message);
      else if (
        !userMatch &&
        inboxUserInfo.text().indexOf(senderUsername) > -1 &&
        this.loggedInUserUsername.indexOf(receiverUsername) > -1
      ) {
        inboxLastMessage.text(messageUpdate.message);
        newMsgSound.play();
      }
    });
  };

  /**
   * Gets inbox users.
   *
   * @returns {Promise<HTMLSpanElement>}
   */
  getInboxUsers = async () => $('.inbox_user').toArray();

  /**
   * Gets inbox user informations.
   *
   * @returns {Promise<HTMLSpanElement>}
   */
  getInboxUserInfos = async () => $('.inbox_user_info').toArray();

  /**
   * Gets inbox last messages.
   *
   * @returns {Promise<HTMLSpanElement>}
   */
  getInboxLastMessages = async () => $('.inbox_last_msg').toArray();
}

globalThis.ContactsHandler = ContactsHandler;
