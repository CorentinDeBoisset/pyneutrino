import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConversationPageComponent } from './conversation-page.component';

describe('ConversationPageComponent', () => {
  let component: ConversationPageComponent;
  let fixture: ComponentFixture<ConversationPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConversationPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ConversationPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
