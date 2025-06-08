//@ts-check

export class TargetUserLengthError extends Error {
  /**
   * Constructor.
   */
  constructor() {
    super(
      'The specified array does not contain exactly 3 elements. Also note that the order of elements should be: first name, last name, username.'
    );
    this.name = 'TargetUserLengthError';
  }
}
