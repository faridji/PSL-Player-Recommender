import { AdminPanelPage } from './app.po';

describe('admin-panel App', () => {
  let page: AdminPanelPage;

  beforeEach(() => {
    page = new AdminPanelPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
