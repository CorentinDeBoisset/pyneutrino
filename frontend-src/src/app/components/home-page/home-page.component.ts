import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { catchError, EMPTY, Observable } from 'rxjs';
import { Conversation, UserEntity } from '../../stores/types';
import { CommonModule } from '@angular/common';
import { TimeFromNowPipe } from '../../services/timeFromNowPipe';
import { IdentityStore } from '../../stores/indentityStore';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule, TimeFromNowPipe, RouterLink],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  currentUser$: Observable<UserEntity|null>;
  conversations: Conversation[];
  conversationFetchError!: string | null;
  newConversationError!: string | null;

  constructor(private router: Router, private httpClient: HttpClient, private identityStore: IdentityStore) {
    this.currentUser$ = this.identityStore.user$;
    this.conversations = [];
  }

  ngOnInit(): void {
   const req = this.httpClient.get<Conversation[]>("/api/messaging/conversations/own")
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
      .pipe(catchError(() => this.handleNewConversationError()))

    req.subscribe(data => {
      this.conversations.unshift(data)
      this.router.navigate(["/conversation", data.id ])
    })
  }

  handleNewConversationError() {
    this.newConversationError = $localize`:create-conversation-error:There was an error when creating a new conversation`
    return EMPTY
  }
}
