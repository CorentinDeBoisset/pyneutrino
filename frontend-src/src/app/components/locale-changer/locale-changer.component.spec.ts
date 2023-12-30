import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LocaleChangerComponent } from './locale-changer.component';

describe('LocaleChangerComponent', () => {
  let component: LocaleChangerComponent;
  let fixture: ComponentFixture<LocaleChangerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LocaleChangerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LocaleChangerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
