//@ts-check

export class EventManager {
  /**
   * Adds event.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static addEvent = (obj, type, callback) =>
    (() => {
      if (typeof addEventListener === 'function') {
        return EventManager.addEventListenerExtension(obj, type, callback);
      } else {
        return EventManager.attachEventExtension(obj, type, callback);
      }
    })();

  /**
   * Removes event.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static removeEvent = (obj, type, callback) =>
    (() => {
      if (typeof removeEventListener === 'function') {
        return EventManager.removeEventListenerExtension(obj, type, callback);
      } else {
        return EventManager.detachEventExtension(obj, type, callback);
      }
    })();

  /**
   * Gets target.
   *
   * @param {Event} event
   * @returns {EventTarget | null}
   */
  static getTarget = (event) =>
    (() => {
      if (typeof addEventListener !== 'undefined') {
        return EventManager.getEventTarget(event);
      } else {
        return EventManager.getEventSrcElement(event);
      }
    })();

  /**
   * Prevents default.
   *
   * @param {Event} event
   */
  static preventDefault = (event) =>
    (() => {
      if (typeof addEventListener !== 'undefined') {
        return EventManager.preventDefaultExtension(event);
      } else {
        return EventManager.setReturnValueToFalse(event);
      }
    })();

  /**
   * Add event listener extension.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static addEventListenerExtension = (obj, type, callback) => {
    obj.addEventListener(type, callback, false);
  };

  /**
   * Attach event extension.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static attachEventExtension = (obj, type, callback) => {
    // @ts-ignore
    obj.attachEvent('on' + type, callback);
  };

  /**
   * Remove event listener extension.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static removeEventListenerExtension = (obj, type, callback) => {
    obj.removeEventListener(type, callback, false);
  };

  /**
   * Detach event extension.
   *
   * @param {EventTarget} obj
   * @param {string} type
   * @param {EventListenerOrEventListenerObject | null} callback
   */
  static detachEventExtension = (obj, type, callback) => {
    // @ts-ignore
    obj.detachEvent('on' + type, callback);
  };

  /**
   * Gets event target.
   *
   * @param {Event} event
   * @returns {EventTarget | null}
   */
  static getEventTarget = (event) => event.target;

  /**
   * Gets event source element.
   *
   * @param {Event} event
   * @returns {EventTarget | null}
   */
  static getEventSrcElement = (event) => event.srcElement;

  /**
   * Prevent default extension.
   *
   * @param {Event} event
   */
  static preventDefaultExtension = (event) => {
    event.preventDefault();
  };

  /**
   * Sets return value to false.
   *
   * @param {Event} event
   */
  static setReturnValueToFalse = (event) => {
    event.returnValue = false;
  };
}

// @ts-ignore
window.EventManager = EventManager;
