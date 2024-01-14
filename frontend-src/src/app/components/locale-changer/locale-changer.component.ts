import { Component, Inject, LOCALE_ID, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-locale-changer',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './locale-changer.component.html',
  styleUrl: './locale-changer.component.scss'
})
export class LocaleChangerComponent implements OnInit {
  selectedLocale: FormControl

  constructor(@Inject(LOCALE_ID) protected localeId: string, private router: Router) {
    this.selectedLocale = new FormControl(localeId);
  }

  ngOnInit() {
    this.selectedLocale.valueChanges.subscribe((newValue) => {
      let prefix = ''
      if (newValue !== 'en-US') {
        prefix = `/${newValue}`
      }
      window.location.href = `${prefix}${this.router.url}`
    })
  }
}
