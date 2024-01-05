import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { IdentityStore } from '../stores/indentityStore';
import { Router } from '@angular/router';

/** Pass untouched request through to the next request handler. */
@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {

  constructor(private identityStore: IdentityStore, private router: Router) { }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req)
      .pipe(
        tap({
          error: (err: HttpErrorResponse) => {
            if (err.status === 401) {
              this.identityStore.logout()
              this.router.navigate(["/login"])
              console.info("Tried to access a restricted resource... Loging out.")
            }
          },
        })
      );
  }
}
