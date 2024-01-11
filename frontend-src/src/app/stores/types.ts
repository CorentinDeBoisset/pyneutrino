import { PrivateKey, PublicKey } from "openpgp"

export interface UserEntity {
  id: string,
  email: string
  username: string
  publicKey: PublicKey,
  privateKey: PrivateKey,
}

export interface LoginResponse {
  id: string,
  email: string,
  username: string,
  public_key: string,
  private_key: string,
  creation_date: string,
  email_verification_date: string,
}

export interface Conversation {
  id: string
  invite_code: string
  creator_id: string
  receiver_id: string
  creation_date: Date
  last_update_date: Date
}

export interface SentMessage {
  id: string
  sender: string
  creation_date: Date,
  message: string
}
