import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { IdentityStore } from '../../stores/indentityStore';
import { catchError, throwError } from 'rxjs';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss'
})
export class RegistrationComponent {
  email = new FormControl('');
  username = new FormControl('');
  password = new FormControl('');
  registrationError = ""

  constructor(private httpClient: HttpClient, private identityStore: IdentityStore) { }

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

    const res = req.subscribe(() => {
      this.registrationError = "";
    });
  }

  handleRegistrationError(err: HttpErrorResponse) {
    let errMsg: string
    if (err.status === 0) {
      errMsg = $localize`:request-network-error:The request failed to be sent`
    } else if (err.status == 400) {
      errMsg = $localize`:register-invalid-request:The login request is invalid`
    } else {
      errMsg = $localize`:server-error:An error occured`
    }
    this.registrationError = errMsg;

    return throwError(() => new Error(`An error occured logging in: ${errMsg}`));
  }
}
