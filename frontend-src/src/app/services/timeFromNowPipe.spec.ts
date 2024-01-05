import { TestBed } from '@angular/core/testing';
import { TimeFromNowPipe } from './timeFromNowPipe';
import { DatePipe } from '@angular/common';

describe('TimeFromNowPipe', () => {
  let service: TimeFromNowPipe
  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [TimeFromNowPipe, DatePipe]})
    service = TestBed.inject(TimeFromNowPipe)

    // 2023-02-05 at 12h26 and 14s340
    service._setTimeFrom(new Date(2023, 0, 5, 12, 25, 14, 340))
  });

  it('transform() should return a value', () => {
    expect(service.transform('2023-01-01')).toBeDefined()
  })

  it('transform() should return the hour if the date is the same as today', () => {
    const sameDay = new Date(2023, 0, 5, 8, 15, 0, 0);
    expect(service.transform(sameDay)).toEqual('8:15 AM')

    const yesterday = new Date(2023, 0, 4, 15, 20, 0, 0);
    expect(service.transform(yesterday)).not.toEqual('15h20')
  })

  it('transform() should return the number of days if in the last 10 days', () => {
    // Later time than 12h25
    const oneDay = new Date(2023, 0, 4, 15, 16, 0, 0);
    expect(service.transform(oneDay)).toEqual('yesterday')

    // Earlier time than 12h25
    const twoDays = new Date(2023, 0, 3, 9, 16, 0, 0);
    expect(service.transform(twoDays)).toEqual('2 days ago')

    // Over new year's day
    const sixDays = new Date(2022, 11, 30, 15, 16, 0, 0);
    expect(service.transform(sixDays)).toEqual('6 days ago')

    // Exactly 10 days ago
    const tenDays = new Date(2022, 11, 26, 7, 5, 0, 0)
    expect(service.transform(tenDays)).toEqual('10 days ago')
  })

  it('transform() should return the date if older than 10 days', () => {
    // Exactly 11 days ago
    const elevenDays = new Date(2022, 11, 25, 15, 5, 0, 0)
    expect(service.transform(elevenDays)).toEqual('December 25, 2022')

    // A long time in the past
    const longPast = new Date(2021, 4, 2, 13, 50, 0, 0)
    expect(service.transform(longPast)).toEqual("May 2, 2021")
  })

  it('transform() should show the date if in the future', () => {
    const future = new Date(2023, 5, 1, 13, 15, 0, 0)
    expect(service.transform(future)).toEqual("Jun 1, 2023, 1:15:00 PM")
  })

  it('transform() should handle timestamps', () => {
    // Milisecond timestamp
    expect(service.transform(1672852531000)).toEqual('yesterday')

    // Second timestamp
    expect(service.transform(1672852531)).toEqual('yesterday')
  })

  it('transform() should handle strings', () => {
    expect(service.transform("Wed Jan 04 2023 17:15:31 GMT")).toEqual('yesterday')
  })
});
