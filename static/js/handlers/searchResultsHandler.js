//@ts-check

import { SearchInputHandler } from './searchInputHandler.js';

export class SearchResultsHandler {
  /**
   * Constructor.
   *
   * @param {SearchInputHandler} searchInputHandler
   * @param {*} socket
   * @param {string} loggedInUserUsername
   */
  constructor(searchInputHandler, socket, loggedInUserUsername) {
    this.searchInputHandler = searchInputHandler;
    this.socket = socket;
    this.loggedInUserUsername = loggedInUserUsername;
  }

  /**
   * Is add contact.
   *
   * @param {*} eSrc
   * @returns {boolean}
   */
  isAddContact = (eSrc) => $(eSrc).hasClass('add_contact');

  /**
   * Handles search results visibility.
   *
   * @param {boolean} isClickedOutside
   */
  handleSearchResultsVisibility = async (isClickedOutside = false) => {
    let searchedValue = this.searchInputHandler.getSearchedValue();

    $('.search_results').each(async (elem, index) => {
      let searchedValueIndex = this.getSearchedValueIndex(index, searchedValue);
      let isEmptyOrNotFound = !searchedValue || searchedValueIndex > -1;

      console.log(elem);
      console.log(index);

      if (isClickedOutside) this.hideElem(index);
      else if (isEmptyOrNotFound) this.showElem(index);
      else this.hideElem(index);
    });
  };

  /**
   * Gets searched value index.
   *
   * @param {number} index
   * @param {string} searchedValue
   * @returns {number}
   */
  getSearchedValueIndex = (index, searchedValue) =>
    $('.found_contact', index).text().toUpperCase().indexOf(searchedValue);

  /**
   * Shows element.
   *
   * @param {number} index
   */
  showElem = (index) => $(index).css('display', 'block');

  /**
   * Hides element.
   *
   * @param {number} index
   */
  hideElem = (index) => $(index).css('display', 'none');

  /**
   * Adds contact.
   *
   * @param {*} eSrc
   */
  addContact = async (eSrc) => {
    Utils.setToAdded(eSrc);

    let foundContact = await this.getFoundContact();
    let payload = {
      loggedInUserUsername: this.loggedInUserUsername,
      foundContact,
    };

    this.socket.emit('add_contact', payload);
  };

  /**
   * Get found contact.
   *
   * @returns {Promise<string>}
   */
  getFoundContact = async () =>
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
   * @returns {Promise<Array<HTMLAnchorElement>>}
   */
  getAddContacts = async () => $('.add_contact').toArray();

  /**
   * Gets found contacts.
   *
   * @returns {Promise<Array<HTMLSpanElement>>}
   */
  getFoundContacts = async () => $('.found_contact').toArray();
}

window.SearchResultsHandler = SearchResultsHandler;
