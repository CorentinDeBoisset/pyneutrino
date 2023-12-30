import { Component, Inject, LOCALE_ID } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-locale-changer',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './locale-changer.component.html',
  styleUrl: './locale-changer.component.scss'
})
export class LocaleChangerComponent {
  selectedLocale = new FormControl();

  constructor(@Inject(LOCALE_ID) protected localeId: string) {
    this.selectedLocale.setValue(localeId);
  }

  ngOnInit() {
    this.selectedLocale.valueChanges.subscribe(newLocale => {
      // TODO: Redirect the user to the right url
    })
  }
}
