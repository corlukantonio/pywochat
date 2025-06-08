//@ts-check

import { Message } from '../models/message.js';
import { TargetUser } from '../models/targetUser.js';
import { Utils } from '../utils.js';
import { ComposeMessageHandler } from './composeMessageHandler.js';
import { HeaderOnlineHandler } from './headerOnlineHandler.js';

export class MessagesHandler {
  /**
   * Constructor.
   *
   * @param {Socket} socket
   */
  constructor(socket) {
    this.composeMessageHandler = ComposeMessageHandler.getInstance();
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
   * Sends message.
   */
  sendMessage = () => {
    let messageContent = this.composeMessageHandler.getInputMessage();

    if (messageContent) {
      let targetUser = TargetUser.create(this.getTargetUser());
      let message = Message.create(
        messageContent,
        this.loggedInUserUsername,
        targetUser
      );

      this.socket.send(message);
      this.composeMessageHandler.emptyInputMessage();
    }
  };

  /**
   * Gets target user.
   *
   * @returns {Array<string>}
   */
  getTargetUser = () =>
    $('#targetUser span').text().replace('(', '').replace(')', '').split(' ');

  /**
   * Appends message.
   *
   * @param {string} messageUpdate
   */
  appendMessage = (messageUpdate) => {
    let userMatch =
      messageUpdate['sender']['username'] === this.loggedInUserUsername;

    $('#msgsView').append(
      (userMatch
        ? "<div style='display: block;' class='sent_msgs sender'>"
        : "<div style='display: block;' class='sent_msgs receiver'>") +
        "<span class='msg_info' style='display: none;'>" +
        messageUpdate['sender']['username'] +
        ' ' +
        messageUpdate['receiver']['username'] +
        '</span>' +
        "<div class='msg_wrapper'>" +
        '<span>' +
        messageUpdate['message'] +
        '</span>' +
        '</div>' +
        "<span class='sent_time'>" +
        Utils.getDateAsString() +
        '</span>' +
        '</div>'
    );
  };

  /**
   * Displays message.
   */
  displayMessages = () => {
    let targetUser = this.getTargetUser();
    let sentMessages = this.getSentMessages();
    let firstMessage = true;

    sentMessages.forEach((elem, i) => {
      let messageInfo = this.getMessageInfo(i).text().split(' ');

      if (this.isMessageBetweenUsers(messageInfo, targetUser)) {
        $(elem).css('display', 'block');

        if (firstMessage) {
          $(elem).addClass('first_message');
          firstMessage = false;
        }
      } else {
        $(elem).css('display', 'none');
      }
    });

    this.scrollToLatest();
  };

  /**
   * Is message between users.
   *
   * @param {Array<string>} messageInfo
   * @param {Array<string>} targetUser
   * @returns {boolean}
   */
  isMessageBetweenUsers = (messageInfo, targetUser) => {
    let isMessageFromLoggedInUser = messageInfo[0] == this.loggedInUserUsername;
    let isMessageForTargetUser = messageInfo[1] == targetUser[2];
    let isMessageFromTargetUser = messageInfo[0] == targetUser[2];
    let isMessageForLoggedInUser = messageInfo[1] == this.loggedInUserUsername;

    return (
      (isMessageFromLoggedInUser && isMessageForTargetUser) ||
      (isMessageFromTargetUser && isMessageForLoggedInUser)
    );
  };

  /**
   * Gets sent messages.
   *
   * @returns {Array<HTMLElement>}
   */
  getSentMessages = () => $('.sent_msgs').toArray();

  /**
   * Gets messages content.
   *
   * @returns {Array<HTMLElement>}
   */
  getMessagesContent = () => $('.msg_content').toArray();

  /**
   * Gets messages info.
   *
   * @returns {Array<HTMLSpanElement>}
   */
  getMessagesInfo = () => $('.msg_info').toArray();

  /**
   * Gets message info.
   *
   * @param {number} index
   * @returns {JQuery<HTMLSpanElement>}
   */
  getMessageInfo = (index) => $(this.getMessagesInfo()[index]);

  /**
   * Sets target user.
   *
   * @param {string} targetUser
   * @returns {JQuery<HTMLElement>}
   */
  setTargetUser = (targetUser) => $('#targetUser span').text(targetUser);

  /**
   * Scrolls to latest.
   *
   * @returns {JQuery<HTMLElement>}
   */
  scrollToLatest = () =>
    $('#msgsView').scrollTop($('#msgsView')[0].scrollHeight);
}

globalThis.MessagesHandler = MessagesHandler;
