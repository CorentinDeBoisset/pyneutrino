import { Component, Input, OnDestroy } from '@angular/core';
import { Conversation, SentMessage } from '../../stores/types';
import { CommonModule, DatePipe } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { IdentityStore } from '../../stores/indentityStore';
import { HttpClient, HttpParams } from '@angular/common/http';
import { EMPTY, catchError } from 'rxjs';
import { PublicKey, readKey } from 'openpgp';

@Component({
  selector: 'app-conversation-content',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, DatePipe],
  templateUrl: './conversation-content.component.html',
  styleUrl: './conversation-content.component.scss'
})
export class ConversationContentComponent implements OnDestroy {
  private _conversation!: Conversation
  messages: SentMessage[]
  newMessage: FormControl
  contactPublicKey: PublicKey|null
  loadError: string|null
  sendMessageError: string|null
  newMessageSource: EventSource|null

  constructor(private httpClient: HttpClient, private identityStore: IdentityStore) {
    this.messages = [];
    this.newMessage = new FormControl("");
    this.contactPublicKey = null
    this.loadError = null
    this.sendMessageError = null
    this.newMessageSource = null
  }

  ngOnDestroy(): void {
    if (this.newMessageSource) {
      this.newMessageSource.close();
    }
  }

  @Input()
  get conversation(): Conversation { return this._conversation}
  set conversation(conv: Conversation) {
    this._conversation = conv
    if (this.newMessageSource) {
      this.newMessageSource.close()
    }
    this.loadConversation()
  }

  loadConversation() {
    // We start by fetching the public keys of the conversations
    const req = this.httpClient.get<{ creator_public_key: string, receiver_public_key: string}>(
      `/api/messaging/conversations/${this._conversation.id}/public_keys`,
    )
    .pipe(catchError(() => this.handleGetPublicKeysError()))

    req.subscribe(async (data) => {
      const user = await this.identityStore.getCurrentUser()
      if (this._conversation.creator_id === user?.id) {
        this.contactPublicKey = await readKey({ armoredKey: data.receiver_public_key })
      } else {
        this.contactPublicKey = await readKey({ armoredKey: data.creator_public_key })
      }

      // Once the public key is loaded, fetch the messages
      this.loadMessages()
    })
  }

  loadMessages() {
    // Then we load the existing mesages
    const req = this.httpClient.get<SentMessage[]>(
      "/api/messaging/messages",
      { params: new HttpParams().set('conversation_id', this._conversation.id) },
    )
    .pipe(catchError(() => this.handleGetMessagesError()))

    req.subscribe(async data => {
      const contactPubKey = this.contactPublicKey
      if (!contactPubKey) {
        return
      }

      // We reverse the list of messages to have the earliest message last
      this.messages = await this.identityStore.decryptMessages(data.reverse(), contactPubKey)

      // Start a stream request to get new messages without making a request
      this.newMessageSource = new EventSource(`/api/messaging/messages/message-stream?conversation_id=${this._conversation.id}`)
      this.newMessageSource.addEventListener("message", (e) => this.handleNewMessageEvent(e))
    })
  }

  async handleNewMessageEvent(e: MessageEvent<string>) {
    const contactPubKey = this.contactPublicKey
    if (!contactPubKey) {
      return
    }

    const parsedData = JSON.parse(e.data)
    if (!("type" in parsedData) || parsedData.type !== "conv-message") {
      return
    }
    const newMessage: SentMessage = parsedData.data

    const user = await this.identityStore.getCurrentUser()
    if (newMessage.sender === user?.id) {
      return
    }
    const decryptedMessages = await this.identityStore.decryptMessages([newMessage], contactPubKey)
    this.messages.push(...decryptedMessages)
  }

  async handleSendMessage(e: SubmitEvent) {
    e.preventDefault()
    const contactPubKey = this.contactPublicKey
    if (!contactPubKey) {
      this.sendMessageError = $localize`:conversation-missing-metadata:The metadata of the conversation was not loaded properly`
      return
    }

    const newMessagePlain = this.newMessage.value
    const newMessageCypher = await this.identityStore.encryptMessage(newMessagePlain, contactPubKey)
    this.newMessage.setValue("")

    const req = this.httpClient.post<SentMessage>(
      "/api/messaging/messages/new",
      { message: newMessageCypher, conversation_id: this._conversation.id }
    ).pipe(catchError(() => this.handleSendMessageError()))

    req.subscribe(data => {
      this.sendMessageError = null
      data.message = newMessagePlain

      // The messages are ordered from oldest to earliest, so we push the new message at the end
      this.messages.push(data)
    })
  }

  handleGetPublicKeysError() {
    this.loadError = $localize`:conversation-fech-metadata-failed:An error occured when fetching the conversation metadata`
    return EMPTY
  }

  handleGetMessagesError() {
    this.loadError = $localize`:conversation-fetch-messages-failed:An error occured when fetching the messages`
    return EMPTY
  }

  handleSendMessageError() {
    this.sendMessageError = $localize`:conversation-send-message-failed:An error occured when sending the message`
    return EMPTY
  }


  trackMessage(idx: number, item: SentMessage) {
    return item.id
  }
}
