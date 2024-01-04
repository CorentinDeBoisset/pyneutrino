import { CanActivateFn, Router, Routes } from '@angular/router';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { HomePageComponent } from './components/home-page/home-page.component';
import { IdentityStore } from './stores/indentityStore';
import { inject } from '@angular/core';

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
  }
];
