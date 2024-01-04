import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { catchError, throwError } from 'rxjs';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss'
})
export class RegistrationComponent {
  email = new FormControl('');
  username = new FormControl('');
  password = new FormControl('');
  registrationError = "";
  registrationSuccess = false;

  constructor(private httpClient: HttpClient) { }

  submitRegistration(e: SubmitEvent) {
    e.preventDefault()

    // TODO: call identityStore and generate a key pair

    const body = {
      email: this.email.value,
      password: this.password.value,
      username: this.username.value,
      public_key: "",
      private_key: "",
    };

    const req = this.httpClient
      .post("/api/register/new-account", body)
      .pipe(catchError(err => this.handleRegistrationError(err)));

    req.subscribe(() => {
      this.registrationError = "";
      this.registrationSuccess = true
    });
  }

  handleRegistrationError(err: HttpErrorResponse) {
    let errMsg: string = ""
    if (err.status === 0) {
      errMsg = $localize`:request-network-error:The request failed to be sent`
    } else if (err.status === 400) {
      errMsg = $localize`:register-invalid-request:The login request is invalid`
    } else if (err.status === 409) {
      if (err.error.description === "registration_email_conflict") {
        errMsg = $localize`:registrer-email-conflict:Another user with this email already exists`
      } else if (err.error.description === "registration_username_conflict") {
        errMsg = $localize`:registrer-username-conflict:Another user with this username already exists`
      } else {
        console.warn("The server sent an unexpected conflict error")
      }
    } else {
      errMsg = $localize`:server-error:An error occured`
    }
    this.registrationError = errMsg;
    this.registrationSuccess = false;

    return throwError(() => new Error(`An error occured logging in: ${errMsg}`));
  }
}
