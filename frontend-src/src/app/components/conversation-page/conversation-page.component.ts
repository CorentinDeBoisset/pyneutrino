import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { EMPTY, switchMap, catchError, Observable, of } from 'rxjs';
import { Conversation } from '../../stores/types';
import { CommonModule } from '@angular/common';
import { Location } from '@angular/common';

@Component({
  selector: 'app-conversation-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './conversation-page.component.html',
  styleUrl: './conversation-page.component.scss'
})
export class ConversationPageComponent implements OnInit {
  conversation$!: Observable<Conversation|null>
  conversationFetchError!: string|null;

  constructor(private httpClient: HttpClient, private route: ActivatedRoute, private router: Router, private location: Location) { }

  ngOnInit() {
    this.conversation$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        const conversationId = params.get('id');
        if (conversationId === null) {
          return of(null)
        }

        return this.httpClient.get<Conversation>(`/api/messaging/conversations//${conversationId}`)
          .pipe(catchError(err => this.handleGetConversationError(err)))
      })
    )
  }

  handleGetConversationError(err: HttpErrorResponse) {
    if (err.status === 404) {
      this.conversationFetchError = $localize`:non-existent-conversation:The requested conversation does not exist`
      return EMPTY
    }

    this.conversationFetchError = $localize`:get-conversation-error:There was an error when fetching the conversation`
    return EMPTY
  }

  calculateInviteLink(conversationId: string, inviteCode: string) {
    const path = this.router.serializeUrl(this.router.createUrlTree(
      ["/conversation", conversationId],
      { queryParams: { invite_code: inviteCode }}
    ))

    const baseUrl = window.baseUrl.replace(/\/*$/, '') // Remove trailing slashes

    return `${baseUrl}${path.toString()}`;
  }
}
