import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HowPSLWorksComponent } from './how-pslworks.component';

describe('HowPSLWorksComponent', () => {
  let component: HowPSLWorksComponent;
  let fixture: ComponentFixture<HowPSLWorksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HowPSLWorksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HowPSLWorksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
