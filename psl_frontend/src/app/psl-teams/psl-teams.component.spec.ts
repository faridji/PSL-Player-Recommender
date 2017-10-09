import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PslTeamsComponent } from './psl-teams.component';

describe('PslTeamsComponent', () => {
  let component: PslTeamsComponent;
  let fixture: ComponentFixture<PslTeamsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PslTeamsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PslTeamsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
