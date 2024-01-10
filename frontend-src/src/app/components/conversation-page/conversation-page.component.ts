import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { tap, switchMap, catchError, Observable, EMPTY, of, Unsubscribable, share, BehaviorSubject, combineLatest } from 'rxjs';
import { Conversation, LoginResponse, UserEntity } from '../../stores/types';
import { CommonModule } from '@angular/common';
import { IdentityStore } from '../../stores/indentityStore';
import { ConversationContentComponent } from '../conversation-content/conversation-content.component';

@Component({
  selector: 'app-conversation-page',
  standalone: true,
  imports: [CommonModule, ConversationContentComponent],
  templateUrl: './conversation-page.component.html',
  styleUrl: './conversation-page.component.scss'
})
export class ConversationPageComponent implements OnInit, OnDestroy {
  conversation$!: Observable<Conversation|null>
  currentUser$!: Observable<UserEntity|null>
  conversationFetchError!: string|null
  conversationSub!: Unsubscribable
  refreshConv!: BehaviorSubject<void>

  constructor(
    private httpClient: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private identityStore: IdentityStore
  ) {
    this.refreshConv = new BehaviorSubject<void>(undefined)
  }

  ngOnInit() {
    this.currentUser$ = this.identityStore.user$

    // We combine this.route.paramMap with an empty Subject to be able to force a refresh of the conversation
    this.conversation$ = combineLatest([this.route.paramMap, this.refreshConv]).pipe(
      switchMap(([params]) => {
        const conversationId = params.get('id');
        if (conversationId === null) {
          return of(null)
        }

        const inviteCode = this.route.snapshot.queryParamMap.get('invite_code');
        let queryString: HttpParams|undefined
        if (inviteCode) {
          queryString = new HttpParams().set('invite_code', inviteCode)
        }

        return this.httpClient.get<Conversation>(
          `/api/messaging/conversations/${conversationId}`,
          { params: queryString }
        )
        .pipe(catchError(err => this.handleGetConversationError(err)))
      }),
      share(),
    )

    this.conversationSub = this.conversation$.pipe(
      tap((conv) => {
        const user = this.identityStore.getCurrentUser();
        if (
          conv !== null &&
          user !== null &&
          user.id !== conv.creator_id
        ) {
          if (conv.receiver_id !== null) {
            if (conv.receiver_id !== user.id) {
              // The user propably used a valid invite code, but it's already been used
              this.conversationFetchError = $localize`:conversation-already-joined:This conversation has already be joined by another user`
            }
            return
          }

          const inviteCode = this.route.snapshot.queryParamMap.get('invite_code');

          // The current user is not the creator, and the receiver has not yet been set
          // So we request that this user be attached as receiver of the conversation
          this.httpClient.post(`/api/messaging/conversations/${conv.id}/join`, { "invite_code": inviteCode })
          .pipe(catchError(err => this.handleGetConversationError(err)))
            .subscribe(() => {
              // Remove the invite code query parameter
              this.router
                .navigate(["/conversation", conv.id], { queryParams: {} })
                .then(() => this.refreshConv.next()) // Force a refresh of the conversation
            })
        }
      })
    ).subscribe()
  }

  async guestJoin(e: SubmitEvent,convId: string) {
    e.preventDefault();

    const inviteCode = this.route.snapshot.queryParamMap.get('invite_code');

    // There is no current user.
    // We call the guest-join route that will create a temporary user for us and log us in.
    const keyPair = await this.identityStore.generatePgpKeyPair("", "Anonymous Guest", "")
    this.httpClient.post<LoginResponse>(
      `/api/messaging/conversations/${convId}/guest-join`,
      { "invite_code": inviteCode, "public_key": keyPair.publicKey.armor() }
    )
    .pipe(catchError(err => this.handleGetConversationError(err)))
    .subscribe(data => {
      // We also log in the user in the frontend
      this.identityStore.initGuestSession(data.id, keyPair)

      // Remove the invite code query parameter
      this.router
        .navigate(["/conversation", convId], { queryParams: {}})
        .then(() => this.refreshConv.next()) // Force a refresh of the conversation
    })
  }

  ngOnDestroy() {
    this.conversationSub.unsubscribe()
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
