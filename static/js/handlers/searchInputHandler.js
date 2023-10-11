//@ts-check

export class SearchInputHandler {
  /**
   * Gets searched value.
   *
   * @returns {string}
   */
  getSearchedValue = () => $('#searchedValue').val().toUpperCase();
}

window.SearchInputHandler = SearchInputHandler;
