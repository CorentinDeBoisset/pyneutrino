import { Routes } from '@angular/router';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { RegistrationComponent } from './components/registration/registration.component';

export const routes: Routes = [
  {
    path: "login",
    component: LoginPageComponent,
    title: "Neutrino - Send your passwords securely",
  },
  {
    path: "register",
    component: RegistrationComponent,
    title: "Register - Neutrino",
  }
];
