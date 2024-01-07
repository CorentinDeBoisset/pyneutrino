import { Pipe, PipeTransform } from "@angular/core";
import { DatePipe } from "@angular/common";

@Pipe({
  standalone: true,
  name: 'timeFromNow',
})
export class TimeFromNowPipe implements PipeTransform {
  timeFrom!: Date|null; // Useful for tests

  constructor(private datePipe: DatePipe) { }

  _setTimeFrom(timeFrom: Date) {
    this.timeFrom = timeFrom
  }

  transform(value: string|number|Date): string | null {
    let now = this.timeFrom ?? new Date();
    let givenDate = new Date(value)

    // This handles the case where the value is a unix timestamp in seconds and not milliseconds
    if (givenDate.getFullYear() < 1975) {
      givenDate.setTime(givenDate.getTime()*1000)
    }


    // For short periods of time, we calculate a precise difference
    const preciseTimeDifference = now.getTime() - givenDate.getTime()
    if (preciseTimeDifference < 1000*3600*24 && now.getDay() === givenDate.getDay()) {
      return this.datePipe.transform(givenDate, "shortTime")
    }

    // manage cases where the date is in the future
    if (givenDate > now) {
      return this.datePipe.transform(givenDate, "medium")
    }

    // Now we round to a day precision
    now = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    givenDate = new Date(givenDate.getFullYear(), givenDate.getMonth(), givenDate.getDate())
    const roundedTimeDifference = now.getTime() - givenDate.getTime()

    if (roundedTimeDifference === 1000*3600*24) {
      return "yesterday"
    }

    if (roundedTimeDifference <= 1000*3600*24*10) {
      return `${Math.floor(roundedTimeDifference / (1000*3600*24))} days ago`
    }

    return this.datePipe.transform(givenDate, 'longDate');
  }
}
