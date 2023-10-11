//@ts-check

export class SearchBarHandler {
  /**
   * Is clicked outside.
   *
   * @param {*} eSrc
   * @returns {boolean}
   */
  isClickedOutside = (eSrc) =>
    $('#searchBar').has(eSrc).length === 0 && !$('#searchBar').is(eSrc);
}

window.SearchBarHandler = SearchBarHandler;
