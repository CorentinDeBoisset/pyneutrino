import { Router, Routes, mapToCanActivate } from '@angular/router';
import { Injectable } from '@angular/core';
import { IdentityStore } from './stores/indentityStore';
import { HomePageComponent } from './components/home-page/home-page.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ConversationPageComponent } from './components/conversation-page/conversation-page.component';


@Injectable({ providedIn: 'root' })
class RequiresAuthGuard {
  constructor(private router: Router, private identityStore: IdentityStore) { }

  async canActivate() {
    const isAuth = await this.identityStore.isAuthenticated()
    if (isAuth) {
      return true
    }

    return this.router.parseUrl("/login");
  }
}

@Injectable({ providedIn: 'root' })
class RejectsAuthGuard {
  constructor(private router: Router, private identityStore: IdentityStore) { }

  async canActivate() {
    const isAuth = await this.identityStore.isAuthenticated()
    if (!isAuth) {
      return true
    }

    return this.router.parseUrl("/");
  }
}

export const routes: Routes = [
  {
    path: "",
    component: HomePageComponent,
    title: "Neutrino - Send your passwords securely",
    canActivate: mapToCanActivate([RequiresAuthGuard]),
  },
  {
    path: "login",
    component: LoginPageComponent,
    title: "Neutrino - Send your passwords securely",
    canActivate: mapToCanActivate([RejectsAuthGuard]),
  },
  {
    path: "register",
    component: RegistrationComponent,
    title: "Register - Neutrino",
    canActivate: mapToCanActivate([RejectsAuthGuard]),
  },
  {
    path: "conversation/:id",
    component: ConversationPageComponent,
    title: "Conversation - Neutrino",
    // The creator must be logged in, the receiver can unlogged (if they're a guest)
  },
];
