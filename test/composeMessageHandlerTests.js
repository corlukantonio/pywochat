import { ComposeMessageHandler } from '../static/js/handlers/composeMessageHandler.js';

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
});
