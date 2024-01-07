/// <reference types="@angular/localize" />

import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

// Add properties to window. These are sent by the backend in the index.html
declare global {
  interface Window {
    hasSession: boolean;
    baseUrl: string;
  }
}

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
