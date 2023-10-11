//@ts-check

import { MissingPropertyError } from '../errors/missingPropertyError.js';
import { MessageParticipant } from './messageParticipant.js';

export class MessageUpdate {
  /**
   * Constructor.
   *
   * @param {string} message
   * @param {MessageParticipant} sender
   * @param {MessageParticipant} receiver
   */
  constructor(message, sender, receiver) {
    this.message = message;
    this.sender = sender;
    this.receiver = receiver;
  }

  /**
   * Creates new `MessageUpdate` object.
   *
   * @param {string} arg1
   * @param {object} arg2
   * @param {object} arg3
   * @returns {MessageUpdate}
   */
  static Create = (arg1, arg2 = null, arg3 = null) => {
    if (typeof arg1 === 'string' && arg2 !== null && arg3 !== null) {
      return this.createWithParams(arg1, arg2, arg3);
    }

    if (typeof arg1 === 'string') {
      return this.createWithString(arg1);
    }

    throw new Error('Invalid arguments.');
  };

  /**
   * Creates new `MessageUpdate` object with params.
   *
   * @param {string} message
   * @param {object} sender
   * @param {object} receiver
   * @returns {MessageUpdate}
   */
  static createWithParams = (message, sender, receiver) => {
    if (!this.hasMessageParticipantProps(sender)) {
      throw new Error('Sender object has no message participant properties.');
    }

    if (!this.hasMessageParticipantProps(receiver)) {
      throw new Error('Receiver object has no message participant properties.');
    }

    const senderConverted = MessageParticipant.Create(sender);
    const receiverConverted = MessageParticipant.Create(receiver);

    return new MessageUpdate(message, senderConverted, receiverConverted);
  };

  /**
   * Has message participant properties.
   *
   * @param {object} obj
   * @returns {boolean}
   */
  static hasMessageParticipantProps = (obj) =>
    obj.hasOwnProperty('id') && obj.hasOwnProperty('username');

  /**
   * Creates new `MessageUpdate` object with string.
   *
   * @param {string} data
   * @returns {MessageUpdate}
   */
  static createWithString = (data) => {
    if (typeof data === 'string') {
      var parsed = JSON.parse(data);

      if (!parsed.hasOwnProperty('message')) {
        throw new MissingPropertyError('message');
      }

      if (!parsed.hasOwnProperty('sender')) {
        throw new MissingPropertyError('sender');
      }

      if (!parsed.hasOwnProperty('receiver')) {
        throw new MissingPropertyError('receiver');
      }

      return MessageUpdate.createWithParams(
        parsed['message'],
        parsed['sender'],
        parsed['receiver']
      );
    } else {
      throw new Error('Invalid data format.');
    }
  };
}

window.MessageUpdate = MessageUpdate;
