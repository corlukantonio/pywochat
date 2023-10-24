//@ts-check

// import { Socket } from 'socket.io';
import { Utils } from '../utils.js';
import { SearchInputHandler } from './searchInputHandler.js';

export class SearchResultsHandler {
  /**
   * Constructor.
   *
   * @param {*} socket
   * @param {string} loggedInUserUsername
   */
  constructor(socket, loggedInUserUsername) {
    this.searchInputHandler = SearchInputHandler.getInstance();
    this.socket = socket;
    this.loggedInUserUsername = loggedInUserUsername;
  }

  /**
   * Is add contact.
   *
   * @param {EventTarget} eSrc
   * @returns {boolean}
   */
  isAddContact = (eSrc) => $(eSrc).hasClass('add_contact');

  /**
   * Handles search results visibility.
   *
   * @param {boolean} isClickedOutside
   */
  handleSearchResultsVisibility = (isClickedOutside = false) => {
    let searchedValue = this.searchInputHandler.getSearchedValue();

    $('.search_results').each((index, elem) => {
      let searchedValueIndex = this.getSearchedValueIndex(elem, searchedValue);
      let isEmptyOrNotFound = !searchedValue || searchedValueIndex > -1;

      if (isClickedOutside) this.hideElem(elem);
      else if (isEmptyOrNotFound) this.showElem(elem);
      else this.hideElem(elem);
    });
  };

  /**
   * Gets searched value index.
   *
   * @param {HTMLElement} elem
   * @param {string | undefined} searchedValue
   * @returns {number}
   */
  getSearchedValueIndex = (elem, searchedValue) =>
    $('.found_contact', elem).text().toUpperCase().indexOf(searchedValue);

  /**
   * Shows element.
   *
   * @param {HTMLElement} elem
   */
  showElem = (elem) => $(elem).css('display', 'block');

  /**
   * Hides element.
   *
   * @param {HTMLElement} elem
   */
  hideElem = (elem) => $(elem).css('display', 'none');

  /**
   * Adds contact.
   *
   * @param {EventTarget} eSrc
   */
  addContact = (eSrc) => {
    Utils.setToAdded(eSrc);

    let foundContact = this.getFoundContact();
    let payload = {
      loggedInUserUsername: this.loggedInUserUsername,
      foundContact,
    };

    this.socket.emit('add_contact', payload);
  };

  /**
   * Gets found contact.
   *
   * @returns {string}
   */
  getFoundContact = () =>
    $($(event.target).parent().parent().children()[0])
      .text()
      .replace('\n', '')
      .replace('(', '')
      .replace(')', '')
      .split(' ')
      .map((elem) => elem.replace('\n', ''))
      .filter((elem) => elem);

  /**
   * Gets add contacts.
   *
   * @returns {Array<HTMLAnchorElement>}
   */
  getAddContacts = () => $('.add_contact').toArray();

  /**
   * Gets found contacts.
   *
   * @returns {Array<HTMLSpanElement>}
   */
  getFoundContacts = () => $('.found_contact').toArray();
}

window.SearchResultsHandler = SearchResultsHandler;
