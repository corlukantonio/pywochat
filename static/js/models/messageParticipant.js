import { MissingPropertyError } from '../errors/missingPropertyError.js';

export class MessageParticipant {
  /**
   * Constructor.
   *
   * @param {number} id ID.
   * @param {string} username Username.
   */
  constructor(id, username) {
    this.id = id;
    this.username = username;
  }

  /**
   * Create.
   *
   * @param {object} obj Object.
   * @returns {MessageParticipant} Message participant object.
   */
  static Create = (obj) => {
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
