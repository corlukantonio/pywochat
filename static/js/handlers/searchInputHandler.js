//@ts-check

const searchInputHandlerInstance = Symbol('searchInputHandlerInstance');

export class SearchInputHandler {
  /**
   * Gets instance.
   *
   * @returns {SearchInputHandler}
   */
  static getInstance = () => {
    if (SearchInputHandler[searchInputHandlerInstance] === undefined) {
      SearchInputHandler[searchInputHandlerInstance] = new SearchInputHandler();
    }

    return SearchInputHandler[searchInputHandlerInstance];
  };

  /**
   * Gets searched value.
   *
   * @returns {string | undefined}
   */
  getSearchedValue = () => $('#searchedValue').val()?.toString().toUpperCase();
}
