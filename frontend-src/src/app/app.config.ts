import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { importProvidersFrom, LOCALE_ID, isDevMode } from '@angular/core';
import { APP_BASE_HREF, DatePipe } from '@angular/common';


import { routes } from './app.routes';
import { AuthenticationInterceptor } from './services/authenticationInterceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    importProvidersFrom(HttpClientModule),
    DatePipe,
    { provide: HTTP_INTERCEPTORS, useClass: AuthenticationInterceptor, multi: true },
    {
      provide: APP_BASE_HREF,
      useFactory: (locale: string) => {
        if (isDevMode()) {
          return '/'
        }
        return `/${locale === 'en-US' ? '' : locale}`
      },
      deps: [LOCALE_ID],
    },
  ]
};
