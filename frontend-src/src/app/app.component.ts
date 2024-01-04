import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { LocaleChangerComponent } from './components/locale-changer/locale-changer.component';
import { IdentityStore } from './stores/indentityStore';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, LocaleChangerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  constructor(private identityStore: IdentityStore) { }

  ngOnInit() {
    this.identityStore.restoreUserSession();
  }
}
