//@ts-check

export class MissingPropertyError extends Error {
  /**
   * Constructor.
   *
   * @param {string} propertyName
   */
  constructor(propertyName) {
    super(`The object does not contain '${propertyName}' property.`);
    this.name = 'MissingPropertyError';
  }
}
