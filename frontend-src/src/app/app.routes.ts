import { CanActivateFn, Router, Routes } from '@angular/router';
import { inject } from '@angular/core';
import { IdentityStore } from './stores/indentityStore';
import { HomePageComponent } from './components/home-page/home-page.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ConversationPageComponent } from './components/conversation-page/conversation-page.component';

const requiresAuth: CanActivateFn = () => {
  if (inject(IdentityStore).isAuthenticated()) {
    return true
  }
  return inject(Router).parseUrl("/login");
}

const rejectsAuth: CanActivateFn = () => {
  if (!inject(IdentityStore).isAuthenticated()) {
    return true
  }
  return inject(Router).parseUrl("/");
}

export const routes: Routes = [
  {
    path: "",
    component: HomePageComponent,
    title: "Neutrino - Send your passwords securely",
    canActivate: [requiresAuth],
  },
  {
    path: "login",
    component: LoginPageComponent,
    title: "Neutrino - Send your passwords securely",
    canActivate: [rejectsAuth],
  },
  {
    path: "register",
    component: RegistrationComponent,
    title: "Register - Neutrino",
    canActivate: [rejectsAuth],
  },
  {
    path: "conversation/:id",
    component: ConversationPageComponent,
    title: "Conversation - Neutrino",
    // The creator must be logged in, the receiver can be either logged or anonymous
  },
];
