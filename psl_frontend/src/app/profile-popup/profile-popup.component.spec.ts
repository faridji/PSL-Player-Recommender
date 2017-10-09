import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfilePopupComponent } from './profile-popup.component';

describe('ProfilePopupComponent', () => {
  let component: ProfilePopupComponent;
  let fixture: ComponentFixture<ProfilePopupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfilePopupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilePopupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
