import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { IdentityStore } from '../../stores/indentityStore';
import { LoginResponse } from '../../stores/types';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule],
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
      "/api/auth/login",
      { email: this.email.value, password: this.password.value }
    ).pipe(catchError(err => this.handleLoginError(err)));

    const res = req.subscribe(data => {
      this.loginError = "";
      this.identityStore.initUserSession(this.password.value || "", data)
      this.router.navigate(["/"])
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

    return throwError(() => new Error(`An error occured logging in: ${errMsg}`));
  }
}
