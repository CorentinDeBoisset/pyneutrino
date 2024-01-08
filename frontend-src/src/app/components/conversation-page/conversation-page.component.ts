import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { tap, switchMap, catchError, Observable, EMPTY, of, combineLatest, Unsubscribable } from 'rxjs';
import { Conversation, UserEntity } from '../../stores/types';
import { CommonModule } from '@angular/common';
import { IdentityStore } from '../../stores/indentityStore';

@Component({
  selector: 'app-conversation-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './conversation-page.component.html',
  styleUrl: './conversation-page.component.scss'
})
export class ConversationPageComponent implements OnInit, OnDestroy {
  conversation$!: Observable<Conversation|null>
  conversationFetchError!: string|null
  currentUser$!: Observable<UserEntity|null>
  userAndConversationSub!: Unsubscribable

  constructor(
    private httpClient: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private identityStore: IdentityStore
  ) { }

  ngOnInit() {
    this.currentUser$ = this.identityStore.user$;

    this.conversation$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        const conversationId = params.get('id');
        if (conversationId === null) {
          return of(null)
        }

        return this.httpClient.get<Conversation>(`/api/messaging/conversations/${conversationId}`)
          .pipe(catchError(err => this.handleGetConversationError(err)))
      })
    )

    this.userAndConversationSub = combineLatest([this.conversation$, this.currentUser$])
    .pipe(tap(([conv, user]) => {
        if (
          conv !== null &&
          user !== null &&
          user.id !== conv.creator_id &&
          conv.receiver_id === null
        ) {
          const inviteCode = this.route.snapshot.queryParamMap.get('invite-code');

          // The current user is not the creator, and the receiver has not yet been set
          // So we request that this user be attached as receiver of the conversation
          this.httpClient.post(`/api/messaging/conversations/${conv.id}/join`, { "invite_code": inviteCode })
            .pipe(catchError(err => this.handleGetConversationError(err)))
            .subscribe(() => {
              // Remove the invite code query parameter
              // This will trigger a refresh of the conversation
              this.router.navigate(["/conversation", { id: conv.id }])
            })

          return
        }
      }))
      .subscribe()
  }

  ngOnDestroy() {
    this.userAndConversationSub.unsubscribe()
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
