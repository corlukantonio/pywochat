//@ts-check

import { MissingPropertyError } from '../errors/missingPropertyError.js';

export class MessageParticipant {
  /**
   * Constructor.
   *
   * @param {number} id
   * @param {string} username
   */
  constructor(id, username) {
    this.id = id;
    this.username = username;
  }

  /**
   * Creates new `MessageParticipant` object.
   *
   * @param {object} obj
   * @returns {MessageParticipant}
   */
  static create = (obj) => {
    if (!obj.hasOwnProperty('id')) {
      throw new MissingPropertyError('id');
    }

    if (!obj.hasOwnProperty('username')) {
      throw new MissingPropertyError('username');
    }

    if (isNaN(obj['id'])) {
      throw new Error("The 'id' property should be a number.");
    }

    return new MessageParticipant(obj['id'], obj['username']);
  };
}
