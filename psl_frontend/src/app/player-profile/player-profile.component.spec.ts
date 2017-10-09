import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerProfileComponent } from './player-profile.component';

describe('PlayerProfileComponent', () => {
  let component: PlayerProfileComponent;
  let fixture: ComponentFixture<PlayerProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PlayerProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayerProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
