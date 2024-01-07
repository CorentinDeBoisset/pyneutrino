import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { catchError, EMPTY } from 'rxjs';
import { Conversation } from '../../stores/types';
import { CommonModule } from '@angular/common';
import { TimeFromNowPipe } from '../../services/timeFromNowPipe';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule, TimeFromNowPipe, RouterLink],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  conversations: Array<Conversation>;
  conversationFetchError!: string | null;

  constructor(private router: Router, private httpClient: HttpClient) {
    this.conversations = [];
  }

  ngOnInit(): void {
   const req = this.httpClient.get<Array<Conversation>>("/api/messaging/conversations/own")
      .pipe(catchError(err => this.handleGetConversationError(err)))

    req.subscribe(data => {
      this.conversations = data;
      this.conversationFetchError = null;
    })
  }

  handleGetConversationError(err: HttpErrorResponse) {
    const errMsg = $localize`homepage-get-conversation-error:There was an error when fetching the list of conversations`;
    this.conversationFetchError = errMsg;

    console.warn(`An error occured when fetching the list of conversations: ${JSON.stringify(err)}`);
    return EMPTY
  }

  newConversationSubmit(e: SubmitEvent) {
    e.preventDefault()

    const req = this.httpClient.post<Conversation>("/api/messaging/conversations/new", null)
      .pipe(catchError(err => this.handleNewConversationError(err)))

    req.subscribe(data => {
      this.conversations.unshift(data)
      this.router.navigate(["/conversation", data.id ])
    })
  }

  handleNewConversationError(err: HttpErrorResponse) {
    // FIXME
    return EMPTY
  }
}
