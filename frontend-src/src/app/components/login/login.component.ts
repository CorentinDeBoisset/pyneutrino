import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { EMPTY, catchError } from 'rxjs';
import { IdentityStore } from '../../stores/indentityStore';
import { LoginResponse } from '../../stores/types';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  email = new FormControl('');
  password = new FormControl('');
  loginError = ""

  constructor(private httpClient: HttpClient, private router: Router, private identityStore: IdentityStore) { }

  submitLogin(e: SubmitEvent) {
    e.preventDefault();

    const req = this.httpClient.post<LoginResponse>(
      "/api/auth/session/login",
      { email: this.email.value, password: this.password.value }
    ).pipe(catchError(err => this.handleLoginError(err)));

    req.subscribe(data => {
      this.loginError = "";
      this.identityStore.initUserSession(this.password.value || "", data)
        .then(() => {
          this.router.navigate(["/"])
        }).catch(() => {
          this.loginError = $localize`:login-account-error:Your account could not be loaded. Please contact an administrator`;
        })
    });
  }

  handleLoginError(err: HttpErrorResponse) {
    let errMsg: string
    if (err.status === 0) {
      errMsg = $localize`:request-network-error:The request failed to be sent`
    } else if (err.status === 401) {
      errMsg = $localize`:login-failed:Invalid credentials`
    } else if (err.status == 400) {
      errMsg = $localize`:login-invalid-request:The login request is invalid`
    } else {
      errMsg = $localize`:server-error:An error occured`
    }
    this.loginError = errMsg;

    console.warn(`An error occured logging in: ${JSON.stringify(err)}`);
    return EMPTY
  }
}
