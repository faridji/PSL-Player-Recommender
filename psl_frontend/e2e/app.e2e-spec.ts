import { PslPage } from './app.po';

describe('psl App', () => {
  let page: PslPage;

  beforeEach(() => {
    page = new PslPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
