//@ts-check

// import { Socket } from 'socket.io';
import { Utils } from '../utils.js';
import { ComposeMessageHandler } from './composeMessageHandler.mjs';

export class MessagesHandler {
  /**
   * Constructor.
   *
   * @param {ComposeMessageHandler} composeMessageHandler
   * @param {Socket} socket
   * @param {string} loggedInUserUsername
   */
  constructor(composeMessageHandler, socket, loggedInUserUsername) {
    this.composeMessageHandler = composeMessageHandler;
    this.socket = socket;
    this.loggedInUserUsername = loggedInUserUsername;
  }

  /**
   * Sends message.
   */
  sendMessage = () => {
    let input = this.composeMessageHandler.getInputMessage();

    if (input) {
      let targetUser = this.getTargetUser();

      if (targetUser.length > 1) {
        this.socket.send(input, this.loggedInUserUsername, targetUser);
        this.composeMessageHandler.emptyInputMessage();
      }
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
        $(elem).css('display', 'block');
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
    let isMessageFromLoggedInUser =
      JSON.parse(messageInfo[0])['username'] == this.loggedInUserUsername;
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

window.MessagesHandler = MessagesHandler;
