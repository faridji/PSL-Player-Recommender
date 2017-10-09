import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnerProfileComponent } from './owner-profile.component';

describe('OwnerProfileComponent', () => {
  let component: OwnerProfileComponent;
  let fixture: ComponentFixture<OwnerProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OwnerProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OwnerProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
