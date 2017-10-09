import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServerSideDealingsComponent } from './server-side-dealings.component';

describe('ServerSideDealingsComponent', () => {
  let component: ServerSideDealingsComponent;
  let fixture: ComponentFixture<ServerSideDealingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServerSideDealingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServerSideDealingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
