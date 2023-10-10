//@ts-check

import { MissingPropertyError } from '../errors/missingPropertyError.js';
import { MessageParticipant } from './messageParticipant.js';

class MessageUpdate {
  /**
   * Constructor.
   *
   * @param {string} message Message.
   * @param {MessageParticipant} sender Sender.
   * @param {MessageParticipant} receiver Receiver.
   */
  constructor(message, sender, receiver) {
    this.message = message;
    this.sender = sender;
    this.receiver = receiver;
  }

  /**
   * Create.
   *
   * @param {string} arg1 Arg 1.
   * @param {object} arg2 Arg 2.
   * @param {object} arg3 Arg 3.
   * @returns {MessageUpdate} Message update object.
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
   * Create with params.
   *
   * @param {string} message Message.
   * @param {object} sender Sender.
   * @param {object} receiver Receiver.
   * @returns {MessageUpdate} Message update object.
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
   * @param {object} obj Object.
   * @returns {boolean} Boolean.
   */
  static hasMessageParticipantProps = (obj) =>
    obj.hasOwnProperty('id') && obj.hasOwnProperty('username');

  /**
   * Create with string.
   *
   * @param {string} data Data.
   * @returns {MessageUpdate} Message update object.
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
