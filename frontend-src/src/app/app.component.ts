import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { LocaleChangerComponent } from './components/locale-changer/locale-changer.component';
import { IdentityStore } from './stores/indentityStore';
import { HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, LocaleChangerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
  isAuthenticated: boolean = false
  authenticatedSubscription: Subscription | undefined

  constructor(private httpClient: HttpClient, private router: Router, private identityStore: IdentityStore) { }

  ngOnInit() {
    this.identityStore.restoreUserSession();
    this.authenticatedSubscription = this.identityStore.user$.subscribe(next => {
      this.isAuthenticated = (next !== null)
    })
  }

  ngOnDestroy() {
    // This is not really necessary since this is the root component and it never gets destroyed
    this.authenticatedSubscription?.unsubscribe()
  }

  submitLogout(e: SubmitEvent) {
    e.preventDefault();

    const req = this.httpClient.post("/api/auth/session/logout", null)
    req.subscribe(() => {
      this.identityStore.logout()
      this.router.navigate(["/login"])
    })
  }
}
