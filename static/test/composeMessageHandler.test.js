import { ComposeMessageHandler } from '../js/handlers/composeMessageHandler.mjs';

jest.mock('jquery', () => {
  return {
    val: jest.fn(),
  };
});

describe('ComposeMessageHandler', () => {
  let composeMessageHandler;

  beforeEach(() => {
    composeMessageHandler = new ComposeMessageHandler();
  });

  afterEach(() => {
    // Clear the mock after each test
    jest.clearAllMocks();
  });

  it('should getInputMessage return input value', () => {
    // Mock the jQuery.val() function
    $.fn.val = jest.fn(() => 'Test message');

    const result = composeMessageHandler.getInputMessage();

    expect($.fn.val).toHaveBeenCalled();
    expect(result).toBe('Test message');
  });
});
