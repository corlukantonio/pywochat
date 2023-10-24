//@ts-check

const searchBarHandlerInstance = Symbol('searchBarHandlerInstance');

export class SearchBarHandler {
  /**
   * Gets instance.
   *
   * @returns {SearchBarHandler}
   */
  static getInstance = () => {
    if (SearchBarHandler[searchBarHandlerInstance] === undefined) {
      SearchBarHandler[searchBarHandlerInstance] = new SearchBarHandler();
    }

    return SearchBarHandler[searchBarHandlerInstance];
  };

  /**
   * Is clicked outside.
   *
   * @param {EventTarget} eSrc
   * @returns {boolean}
   */
  isClickedOutside = (eSrc) =>
    $('#searchBar').has(eSrc).length === 0 && !$('#searchBar').is(eSrc);
}

window.SearchBarHandler = SearchBarHandler;
