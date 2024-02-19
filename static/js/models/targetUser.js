//@ts-check

import { TargetUserLengthError } from '../errors/targetUserLengthError.js';

export class TargetUser {
  /**
   * Constructor.
   *
   * @param {string} firstname
   * @param {string} lastname
   * @param {string} username
   */
  constructor(firstname, lastname, username) {
    this.firstname = firstname;
    this.lastname = lastname;
    this.username = username;
  }

  /**
   * Creates new `TargetUser` object.
   *
   * @param {Array<string>} targetUser
   * @returns {TargetUser}
   */
  static Create(targetUser) {
    if (targetUser.length !== 3) {
      throw new TargetUserLengthError();
    }

    let firstname = targetUser.at(0);
    let lastname = targetUser.at(1);
    let username = targetUser.at(2);

    if (!firstname || !lastname || !username) {
      throw new Error('No element within the array may be empty.');
    }

    return new TargetUser(firstname, lastname, username);
  }
}

// @ts-ignore
window.TargetUser = TargetUser;
