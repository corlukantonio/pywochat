import { ComposeMessageHandler } from '../js/handlers/composeMessageHandler.js';

jest.mock('jquery', () => {
  return {
    val: jest.fn(),
  };
});

// Create a function to set up the DOM environment using jsdom
function setupDOM() {
  const div = document.createElement('div');
  div.innerHTML = '<input id="inputMsg" value="Test Value" />';
  document.body.appendChild(div);
}

describe('ComposeMessageHandler', () => {
  beforeEach(() => {
    setupDOM();
  });

  describe('getInputMessage', () => {
    it('should get the input message', () => {
      const composeMessageHandler = new ComposeMessageHandler();
      const inputMessage = composeMessageHandler.getInputMessage();
      expect(inputMessage).toBe('Test Value');
    });
  });
});
